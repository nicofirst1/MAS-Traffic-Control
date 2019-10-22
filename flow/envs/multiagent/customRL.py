"""Environment for training multi-agent experiments."""

import random
import sys
import traceback
from copy import deepcopy

import numpy as np
import termcolor
from gym.spaces import Box,Tuple
from ray.rllib.env import MultiAgentEnv
from traci.exceptions import FatalTraCIError
from traci.exceptions import TraCIException

from FlowMas.utils.parameters import Params
from flow.core.rewards import min_delay, penalize_standstill, avg_delay_specified_vehicles
from flow.envs.base import Env
from flow.envs.env_utils import standard_observation, neighbors_observation
from flow.utils.exceptions import FatalFlowError

ADDITIONAL_ENV_PARAMS = {
    # maximum acceleration of autonomous vehicles
    'max_accel': 10,
    # maximum deceleration of autonomous vehicles
    'max_decel': 3.5,
}


class CustoMultiRL(MultiAgentEnv, Env):
    """Multi-agent version of base env. See parent class for info."""

    def __init__(self, env_params, sim_params, network, simulator='traci'):
        for p in ADDITIONAL_ENV_PARAMS.keys():
            if p not in env_params.additional_params:
                raise KeyError(
                    'Environment parameter "{}" not supplied'.format(p))

        super().__init__(env_params, sim_params, network, simulator)

        self.observation_space_dict = Box(low=(-sys.maxsize - 1), high=self.k.vehicle.num_vehicles, shape=(8,),
                                          dtype=np.float32)

        self.action_space_dict = Box(
            low=-np.abs(self.env_params.additional_params['max_decel']),
            high=self.env_params.additional_params['max_accel'],
            shape=(1,),  # (4,),
            dtype=np.float32)

    #############################
    #       UPDATE
    #############################

    def step(self, rl_actions):
        """Advance the environment by one step.

        Assigns actions to autonomous and human-driven agents (i.e. vehicles,
        traffic lights, etc...). Actions that are not assigned are left to the
        control of the simulator. The actions are then used to advance the
        simulator by the number of time steps requested per environment step.

        Results from the simulations are processed through various classes,
        such as the Vehicle and TrafficLight kernels, to produce standardized
        methods for identifying specific network state features. Finally,
        results from the simulator are used to generate appropriate
        observations.

        Parameters
        ----------
        rl_actions : array_like
            an list of actions provided by the rl algorithm

        Returns
        -------
        observation : dict of array_like
            agent's observation of the current environment
        reward : dict of floats
            amount of reward associated with the previous state/action pair
        done : dict of bool
            indicates whether the episode has ended
        info : dict
            contains other diagnostic information from the previous action
        """
        for _ in range(self.env_params.sims_per_step):
            self.time_counter += 1
            self.step_counter += 1

            # perform acceleration actions for controlled human-driven vehicles
            if len(self.k.vehicle.get_controlled_ids()) > 0:
                accel = []
                for veh_id in self.k.vehicle.get_controlled_ids():
                    accel_contr = self.k.vehicle.get_acc_controller(veh_id)
                    action = accel_contr.get_action(self)
                    accel.append(action)
                self.k.vehicle.apply_acceleration(
                    self.k.vehicle.get_controlled_ids(), accel)

            # perform lane change actions for controlled human-driven vehicles
            if len(self.k.vehicle.get_controlled_lc_ids()) > 0:
                direction = []
                for veh_id in self.k.vehicle.get_controlled_lc_ids():
                    target_lane = self.k.vehicle.get_lane_changing_controller(
                        veh_id).get_action(self)
                    direction.append(target_lane)
                self.k.vehicle.apply_lane_change(
                    self.k.vehicle.get_controlled_lc_ids(),
                    direction=direction)

            # perform (optionally) routing actions for all vehicle in the
            # network, including rl and sumo-controlled vehicles
            routing_ids = []
            routing_actions = []
            for veh_id in self.k.vehicle.get_ids():
                if self.k.vehicle.get_routing_controller(veh_id) is not None:
                    routing_ids.append(veh_id)
                    route_contr = self.k.vehicle.get_routing_controller(veh_id)
                    routing_actions.append(route_contr.choose_route(self))
            self.k.vehicle.choose_routes(routing_ids, routing_actions)


            # if the training alg is MADDPG reroute exiting vehicles
            self.reroute_if_final_edge()

            self.apply_rl_actions(rl_actions)

            self.additional_command()

            # advance the simulation in the simulator by one step
            self.k.simulation.simulation_step()

            # store new observations in the vehicles and traffic lights class
            self.k.update(reset=False)

            # update the colors of vehicles
            if self.sim_params.render:
                self.k.vehicle.update_vehicle_colors()

            # crash encodes whether the simulator experienced a collision
            crash = self.k.simulation.check_collision()

            # stop collecting new simulation steps if there is a collision
            if crash:
                break

        states = self.get_state()
        done = {key: key in self.k.vehicle.get_arrived_ids()
                for key in states.keys()}

        if crash:
            done['__all__'] = True
        else:
            done['__all__'] = False

        infos = {key: {} for key in states.keys()}

        # compute the reward
        if self.env_params.clip_actions:
            clipped_actions = self.clip_actions(rl_actions)
            reward = self.compute_reward(clipped_actions, fail=crash)
        else:
            reward = self.compute_reward(rl_actions, fail=crash)

        return states, reward, done, infos

    def reset(self, new_inflow_rate=None):
        """Reset the environment.

        This method is performed in between rollouts. It resets the state of
        the environment, and re-initializes the vehicles in their starting
        positions.

        If "shuffle" is set to True in InitialConfig, the initial positions of
        vehicles is recalculated and the vehicles are shuffled.

        Returns
        -------
        observation : dict of array_like
            the initial observation of the space. The initial reward is assumed
            to be zero.
        """
        # reset the time counter
        self.time_counter = 0

        # warn about not using restart_instance when using inflows
        if len(self.net_params.inflows.get()) > 0 and \
                not self.sim_params.restart_instance:
            print(
                "**********************************************************\n"
                "**********************************************************\n"
                "**********************************************************\n"
                "WARNING: Inflows will cause computational performance to\n"
                "significantly decrease after large number of rollouts. In \n"
                "order to avoid this, set SumoParams(restart_instance=True).\n"
                "**********************************************************\n"
                "**********************************************************\n"
                "**********************************************************"
            )

        if self.sim_params.restart_instance or \
                (self.step_counter > 2e6 and self.simulator != 'aimsun'):
            self.step_counter = 0
            # issue a random seed to induce randomness into the next rollout
            self.sim_params.seed = random.randint(0, 1e5)

            self.k.vehicle = deepcopy(self.initial_vehicles)
            self.k.vehicle.master_kernel = self.k
            # restart the sumo instance
            self.restart_simulation(self.sim_params)

        # perform shuffling (if requested)
        elif self.initial_config.shuffle:
            self.setup_initial_state()

        # clear all vehicles from the network and the vehicles class
        if self.simulator == 'traci':
            for veh_id in self.k.kernel_api.vehicle.getIDList():
                try:
                    self.k.vehicle.remove(veh_id)
                except (FatalTraCIError, TraCIException):
                    print(traceback.format_exc())

        # clear all vehicles from the network and the vehicles class
        for veh_id in list(self.k.vehicle.get_ids()):
            # do not try to remove the vehicles from the network in the first
            # step after initializing the network, as there will be no vehicles
            if self.step_counter == 0:
                continue
            try:
                self.k.vehicle.remove(veh_id)
            except (FatalTraCIError, TraCIException):
                print("Error during start: {}".format(traceback.format_exc()))

        # reintroduce the initial vehicles to the network
        for veh_id in self.initial_ids:
            type_id, edge, lane_index, pos, speed = \
                self.initial_state[veh_id]

            try:
                self.k.vehicle.add(
                    veh_id=veh_id,
                    type_id=type_id,
                    edge=edge,
                    lane=lane_index,
                    pos=pos,
                    speed=speed)
            except (FatalTraCIError, TraCIException):
                # if a vehicle was not removed in the first attempt, remove it
                # now and then reintroduce it
                self.k.vehicle.remove(veh_id)
                if self.simulator == 'traci':
                    self.k.kernel_api.vehicle.remove(veh_id)
                self.k.vehicle.add(
                    veh_id=veh_id,
                    type_id=type_id,
                    edge=edge,
                    lane=lane_index,
                    pos=pos,
                    speed=speed)

        # advance the simulation in the simulator by one step
        self.k.simulation.simulation_step()

        # update the information in each kernel to match the current state
        self.k.update(reset=True)

        # update the colors of vehicles
        if self.sim_params.render:
            self.k.vehicle.update_vehicle_colors()

        # check to make sure all vehicles have been spawned
        if len(self.initial_ids) > self.k.vehicle.num_vehicles:
            missing_vehicles = list(
                set(self.initial_ids) - set(self.k.vehicle.get_ids()))
            msg = '\nNot enough vehicles have spawned! Bad start?\n' \
                  'Missing vehicles / initial state:\n'
            for veh_id in missing_vehicles:
                msg += '- {}: {}\n'.format(veh_id, self.initial_state[veh_id])
            raise FatalFlowError(msg=msg)

        # perform (optional) warm-up steps before training
        for _ in range(self.env_params.warmup_steps):
            observation, _, _, _ = self.step(rl_actions=None)

        # render a frame
        self.render(reset=True)

        return self.get_state()

    def reroute_if_final_edge(self):
        """Checks if an edge is the final edge. If it is return the route it
        should start off at.
        """
        veh_ids =  self.k.vehicle.get_rl_ids()
        for veh_id in veh_ids:
            route = self.k.vehicle.get_route(veh_id)
            edge = self.k.vehicle.get_edge(veh_id)
            self.k.vehicle.get_position(veh_id)

            pos=self.k.vehicle.get_position(veh_id)
            length=self.k.network.edge_length(edge)

            eta=length*0.1


            # check if its on the final edge
            if edge == route[-1] and pos+eta>=length:
                type_id = self.k.vehicle.get_type(veh_id)
                # remove the vehicle
                self.k.vehicle.remove(veh_id)
                # reintroduce it at the start of the network
                self.k.vehicle.add(
                    veh_id=veh_id,
                    edge=route[0],
                    type_id=str(type_id),
                    lane="random",
                    pos="0",
                    speed="random")

    #############################
    #       REWARDS
    #############################

    def compute_reward(self, rl_actions, **kwargs):
        """Reward function for the RL agent(s).

        MUST BE implemented in new environments.
        Defaults to 0 for non-implemented environments.

        Parameters
        ----------
        rl_actions : array_like
            actions performed by rl vehicles
        kwargs : dict
            other parameters of interest. Contains a "fail" element, which
            is True if a vehicle crashed, and False otherwise

        Returns
        -------
        reward : float or list of float"""

        # in the warmup steps
        if rl_actions is None:
            return {}

        rewards = {}
        for rl_id in self.k.vehicle.get_rl_ids():
            if self.env_params.evaluate:
                # reward is speed of vehicle if we are in evaluation mode
                reward = self.k.vehicle.get_speed(rl_id)
            elif kwargs['fail']:
                # reward is 0 if a collision occurred
                reward = 0
            else:

                # Reward function used to encourage minimization of total delay.
                cost1 = min_delay(self)

                # Reward function that penalizes vehicle standstill (refer to all vehicles)
                # the higher the worst
                cost2 = penalize_standstill(self)

                # todo: add selfish penalization for current agent being still

                # Calculate the average delay for the current vehicle (Selfishness)
                cost3 = avg_delay_specified_vehicles(self, rl_id)

                # get the type of the agent (coop or not)
                rl_type = self.k.vehicle.get_type(rl_id)

                # then get the coop weight
                w = self.k.vehicle.type_parameters.get(rl_type).get('cooperative_weight')

                # estimate the coop part of the reward
                coop_reward = (cost1 + cost2) * w

                # jerk related reward factor, to penalize excessive de/acceleration behaviors
                jerk = self.k.vehicle.get_jerk(rl_id)

                # getting scaling factor for jerk
                scaling_factor = self.env_params.additional_params["max_accel"] \
                                 - self.env_params.additional_params["max_decel"]
                scaling_factor /= self.sim_params.sim_step

                # the higher the worst, tha
                jerk = - pow(jerk, 2) / pow(scaling_factor, 2)

                # maximum penalization can be 4
                reward = max(Params.baseline - coop_reward - cost3 - jerk, 0)

                if Params.debug:
                    termcolor.colored(f"\nReward for agent {rl_id} is : {reward}", "yellow")

            rewards[rl_id] = reward
        return rewards

    #############################
    #       OBSERVATIONS
    #############################

    @property
    def observation_space(self):
        """Identify the dimensions and bounds of the observation space.

        Returns
        -------
        gym Box or Tuple type
            a bounded box depicting the shape and bounds of the observation
            space
        """
        # fixme: get lowest value right (-max_speed?)
        return self.observation_space_dict

    def get_state(self):
        """Return the state of the simulation as perceived by the RL agent.
        Returns
        -------
        state : array_like
            information on the state of the vehicles, which is provided to the
            agent"""
        obs = {}

        # normalizing constants
        max_speed = self.k.network.max_speed()
        max_length = self.k.network.length()

        for rl_id in self.k.vehicle.get_rl_ids():
            standard = standard_observation(self.k.vehicle, rl_id, max_speed, max_length)
            neighbors = neighbors_observation(self.k.vehicle, rl_id, max_speed,
                                              self.env_params.additional_params["max_accel"],
                                              self.sim_step)

            observation = np.concatenate((standard, neighbors), axis=0)

            """
            Each observation should be scaled 0-1
            
            Observation
            1) agent speed
            2) difference between lead speed and agent
            3) distance from leader
            4) difference between agent speed and follower
            5) distance from follower
            6) number of neighbors (not scaled obv)
            7) average neighbors speed
            8) average neighbors acceleration
            
            
            """

            obs.update({rl_id: observation})

        return obs

    #############################
    #       ACTIONS
    #############################

    def _apply_rl_actions(self, rl_actions):
        """See class definition."""
        # in the warmup steps, rl_actions is None
        if rl_actions:
            for rl_id, actions in rl_actions.items():
                accel = actions[0]


                # lane_change_softmax = np.exp(actions[1:4])
                # lane_change_softmax /= np.sum(lane_change_softmax)
                # lane_change_action = np.random.choice([-1, 0, 1],
                #                                       p=lane_change_softmax)

                self.k.vehicle.apply_acceleration(rl_id, accel)
                # self.k.vehicle.apply_lane_change(rl_id, lane_change_action)


    def clip_actions(self, rl_actions=None):
        """Clip the actions passed from the RL agent.

        If no actions are provided at any given step, the rl agents default to
        performing actions specified by sumo.

        Parameters
        ----------
        rl_actions : array_like
            list of actions provided by the RL algorithm

        Returns
        -------
        rl_clipped : array_like
            The rl_actions clipped according to the box
        """
        # ignore if no actions are issued
        if rl_actions is None:
            return None

        # fixme: findout why the accel is close to zero before clipping

        # clip according to the action space requirements
        if isinstance(self.action_space, Box):
            for key, action in rl_actions.items():
                rl_actions[key] = np.clip(
                    action,
                    a_min=self.action_space.low,
                    a_max=self.action_space.high)
        return rl_actions

    @property
    def action_space(self):
        """Identify the dimensions and bounds of the action space.

        Returns
        -------
        gym Box or Tuple type
            a bounded box depicting the shape and bounds of the action space
        """

        # The action space is just the de/acceleration
        return self.action_space_dict
