## Problems
This file concerns general errors encountered while writing the software.

### - Error 1

__Traceback:__

 ``` server at localhost:58127 [Errno 61] Connection refused```

__Solution:__ wait, as written [here](https://stackoverflow.com/questions/40362275/using-sumo-and-traci-could-not-connect-to-traci-server-61)

### -  Error 2

__Traceback:__ `ModuleNotFoundError: No module named 'rllab'`

__Solution:__ You must install [rllab](https://github.com/rll/rllab) with the following commands:

- `git clone https://github.com/rll/rllab`
- `cd rllab`
- `source activate 'YourEnvName'`
- `python setup.py install`

Check out [this](https://gist.github.com/yuanzhaoYZ/15bb640e1751da163d6a01675d54825f) for installation with conda
and [this](https://rllab.readthedocs.io/en/latest/user/installation.html) for installation with custom environment.

Update: Flow is getting rid of *rllib* so you won't need it anymore.

### - Errors with importing custom environments and/or network [3]

If you have any errors regarding importing custom environments and/or networks remember that we have our 
[own flow](../flow) directory and that your python environment must be free of other flow installations.

### -  Error 4

__Traceback:__
```
File "mtrand.pyx", line 1126, in mtrand.RandomState.choice
ValueError: a must be non-empty
```

__Solution:__
As written [here](https://stackoverflow.com/questions/57069566/when-test-the-grid-scenario-there-is-an-valueerror) this problem is due to the lack of routes in the Router, so:
- Replace _GridRouter_ with _ContinuousRouter_
- Add _spacing="custom"_ to _InitialConfig()_



### Error 5

__Traceback:__
:
```  
File "/Users/oblintosh/Desktop/dmas/flow/envs/base.py", line 279, in setup_initial_state
pos = start_pos[i][1]
IndexError: list index out of range
```

__Solution:__  Router problem, same as before

### Error 6

__Traceback:__
```
 File "/anaconda3/envs/dmas/lib/python3.6/site-packages/ray/actor.py", line 548, in _actor_method_call
    function = getattr(worker.actors[self._ray_actor_id], method_name)
AttributeError: 'PPO' object has no attribute 'set_global_vars'
```

__Solution:__

Follow [git thread](https://github.com/ray-project/ray/issues/5715) and [this](https://github.com/ray-project/ray/issues/5748), 
fix by setting _num_cpu=1_ in ray.init()

### Error 7

__Traceback__:

```
Traceback (most recent call last):
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/tune/web_server.py", line 26, in <module>
    import requests  # `requests` is not part of stdlib.
ModuleNotFoundError: No module named 'requests'
Couldn't import `requests` library. Be sure to install it on the client side.
lz4 not available, disabling sample compression. This will significantly impact RLlib performance. To install lz4, run `pip install lz4`.
Traceback (most recent call last):
  File "FlowMas/Tutorials/3_GridMapCustomRL.py", line 12, in <module>
    from flow.envs.multiagent.customRL import ADDITIONAL_ENV_PARAMS
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/envs/__init__.py", line 2, in <module>
    from flow.envs.base import Env
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/envs/base.py", line 16, in <module>
    from traci.exceptions import FatalTraCIError
ModuleNotFoundError: No module named 'traci'
```

__Solution__: Install sumotools with 


`pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl`


### Error 8

__Traceback__: 

```
ray.exceptions.RayTaskError: ray_worker (pid=30587, host=Ublion18)
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/agents/trainer_template.py", line 90, in __init__
    Trainer.__init__(self, config, env, logger_creator)
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/agents/trainer.py", line 366, in __init__
    Trainable.__init__(self, config, logger_creator)
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/tune/trainable.py", line 99, in __init__
    self._setup(copy.deepcopy(self.config))
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/agents/trainer.py", line 486, in _setup
    self._init(self.config, self.env_creator)
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/agents/trainer_template.py", line 109, in _init
    self.config["num_workers"])
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/agents/trainer.py", line 531, in _make_workers
    logdir=self.logdir)
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/evaluation/worker_set.py", line 64, in __init__
    RolloutWorker, env_creator, policy, 0, self._local_config)
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/evaluation/worker_set.py", line 220, in _make_worker
    _fake_sampler=config.get("_fake_sampler", False))
  File "/home/dizzi/.conda/envs/dmas/lib/python3.6/site-packages/ray/rllib/evaluation/rollout_worker.py", line 338, in __init__
    raise ImportError("Could not import tensorflow")
ImportError: Could not import tensorflow
```

__Solution__: Install tensorflow with
 
 `pip install --upgrade tensorflow`
 
### Error 9
__Traceback__:
```
Traceback (most recent call last):
  File "simulation.py", line 5, in <module>
    import ray
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/__init__.py", line 13, in <module>
    import ray._raylet
  File "python/ray/_raylet.pyx", line 40, in init ray._raylet
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/utils.py", line 20, in <module>
    import ray.gcs_utils
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/gcs_utils.py", line 5, in <module>
    from ray.core.generated.gcs_pb2 import (
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/core/generated/gcs_pb2.py", line 7, in <module>
    from google.protobuf.internal import enum_type_wrapper
ModuleNotFoundError: No module named 'google'
```

__Solution__: Install google api with
 
 'pip install --upgrade google-api-python-client'
 
 
 ### Error 10
 __Traceback__:
 ```
 Traceback (most recent call last):
  File "simulation.py", line 5, in <module>
    import ray
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/__init__.py", line 13, in <module>
    import ray._raylet
  File "python/ray/_raylet.pyx", line 40, in init ray._raylet
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/utils.py", line 20, in <module>
    import ray.gcs_utils
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/gcs_utils.py", line 5, in <module>
    from ray.core.generated.gcs_pb2 import (
  File "/home/ivopascal/miniconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-linux-x86_64.egg/ray/core/generated/gcs_pb2.py", line 7, in <module>
    from google.protobuf.internal import enum_type_wrapper
ModuleNotFoundError: No module named 'google.protobuf'
```

__Solution__: Install protobuf with
 
 'pip install protobuff'
 
 
### Error 11

__Traceback__:
```
Params class initialized
Tutorials/1_GridMapNoLights.py:60: PendingDeprecationWarning: The class flow.scenarios.traffic_light_grid.TrafficLightGridScenario is deprecated, use flow.networks.traffic_light_grid.TrafficLightGridNetwork instead.
  traffic_lights=TrafficLightParams())
/bin/sh: 1: netconvert: not found
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Error during start: [Errno 2] No such file or directory: '/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/grid_tutorial_20190925-1011411569420701.657424.net.xml'
Retrying in 1 seconds...
Traceback (most recent call last):
  File "Tutorials/1_GridMapNoLights.py", line 66, in <module>
    env = TestEnv(env_params, sumo_params, scenario)
  File "/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/envs/base.py", line 158, in __init__
    self.k.network.generate_network(self.network)
  File "/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/traci.py", line 145, in generate_network
    connections
  File "/home/osboxes/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/traci.py", line 521, in generate_net
    raise error
TypeError: exceptions must derive from BaseException
```


__Solution__:
source ~/.bashrc


### Error 11

__Traceback__:
```
Traceback (most recent call last):
  File "FlowMas/simulation.py", line 8, in <module>
    from FlowMas.utils.general_utils import inflow_random_edges, ppo_default_config
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/FlowMas/utils/general_utils.py", line 7, in <module>
    from flow.utils.rllib import FlowParamsEncoder
  File "/Users/giulia/InstallationPackages/flow/flow/utils/rllib.py", line 10, in <module>
    import flow.envs
  File "/Users/giulia/InstallationPackages/flow/flow/envs/__init__.py", line 2, in <module>
    from flow.envs.base import Env
  File "/Users/giulia/InstallationPackages/flow/flow/envs/base.py", line 22, in <module>
    from flow.core.util import ensure_dir
  File "/Users/giulia/InstallationPackages/flow/flow/core/util.py", line 6, in <module>
    from lxml import etree
ImportError: dlopen(/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/lxml/etree.cpython-36m-darwin.so, 2): no suitable image found.  Did find:
	/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/lxml/etree.cpython-36m-darwin.so: unknown file type, first eight bytes: 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
	/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/lxml/etree.cpython-36m-darwin.so: unknown file type, first eight bytes: 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
```

__Solution__:
As written [here](https://stackoverflow.com/questions/57898440/lxml-error-when-running-sugiyama-py-on-mac):

```
conda uninstall lxml
pip install lxml
```


### Error 12

__Traceback__:

```

Traceback (most recent call last):
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/tune/ray_trial_executor.py", line 225, in start_trial
    self._start_trial(trial)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/tune/ray_trial_executor.py", line 143, in _start_trial
    or trial._checkpoint.value is not None)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/tune/ray_trial_executor.py", line 118, in _setup_runner
    return cls.remote(config=trial.config, logger_creator=logger_creator)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/actor.py", line 282, in remote
    return self._remote(args=args, kwargs=kwargs)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/actor.py", line 354, in _remote
    *copy.deepcopy(args), **copy.deepcopy(kwargs))
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/agents/trainer_template.py", line 90, in __init__
    Trainer.__init__(self, config, env, logger_creator)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/agents/trainer.py", line 366, in __init__
    Trainable.__init__(self, config, logger_creator)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/tune/trainable.py", line 99, in __init__
    self._setup(copy.deepcopy(self.config))
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/agents/trainer.py", line 486, in _setup
    self._init(self.config, self.env_creator)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/agents/trainer_template.py", line 109, in _init
    self.config["num_workers"])
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/agents/trainer.py", line 531, in _make_workers
    logdir=self.logdir)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/evaluation/worker_set.py", line 64, in __init__
    RolloutWorker, env_creator, policy, 0, self._local_config)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/evaluation/worker_set.py", line 220, in _make_worker
    _fake_sampler=config.get("_fake_sampler", False))
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/rllib/evaluation/rollout_worker.py", line 274, in __init__
    self.env = _validate_env(env_creator(env_context))
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/utils/registry.py", line 109, in create_env
    return gym.envs.make(env_name)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/gym/envs/registration.py", line 156, in make
    return registry.make(id, **kwargs)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/gym/envs/registration.py", line 101, in make
    env = spec.make(**kwargs)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/gym/envs/registration.py", line 73, in make
    env = cls(**_kwargs)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/envs/multiagent/customRL.py", line 38, in __init__
    super().__init__(env_params, sim_params, network, simulator)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/envs/base.py", line 158, in __init__
    self.k.network.generate_network(self.network)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/traci.py", line 126, in generate_network
    self.network.net_params)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/traci.py", line 573, in generate_net_from_osm
    edges_dict, conn_dict = self._import_edges_from_net(net_params)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/traci.py", line 837, in _import_edges_from_net
    tree = ElementTree.parse(net_path, parser=parser)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/xml/etree/ElementTree.py", line 1196, in parse
    tree.parse(source, parser)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/xml/etree/ElementTree.py", line 586, in parse
    source = open(source, "rb")
FileNotFoundError: [Errno 2] No such file or directory: '/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/dmas-1.0-py3.6.egg/flow/core/kernel/network/debug/cfg/simulationRL_20190927-1501231569589283.425456.net.xml'
```
The error is actually in the netconvert command:
```
netconvert --osm-files $HOME/dmas/FlowMas/maps/GroningenOSM/osm_bbox.osm.xml --output-file $HOME/dmas/flow/core/kernel/network/debug/cfg/simulationRL_20190928-0948571569656937.4081762.net.xml --keep-edges.by-vclass passenger --remove-edges.isolated --no-warnings True
Error: Cannot import network data without PROJ-Library. Please install packages proj before building sumo
Quitting (on error).
```

__Solution__:

Check [this](https://proj.org/install.html) and then [this](https://sourceforge.net/p/sumo/mailman/message/35283626/)

### Error 13

__Traceback__:
```
Traceback (most recent call last):
  File "/Users/giulia/Desktop/dmas/FlowMas/Tutorials/4.5_ImportedScenario.py", line 81, in <module>
    network=network
  File "/Users/giulia/Desktop/dmas/flow/envs/base.py", line 158, in __init__
    self.k.network.generate_network(self.network)
  File "/Users/giulia/Desktop/dmas/flow/core/kernel/network/traci.py", line 123, in generate_network
    self.network.net_params)
  File "/Users/giulia/Desktop/dmas/flow/core/kernel/network/traci.py", line 607, in generate_net_from_template
    edges_dict, conn_dict = self._import_edges_from_net(net_params)
  File "/Users/giulia/Desktop/dmas/flow/core/kernel/network/traci.py", line 837, in _import_edges_from_net
    tree = ElementTree.parse(net_path, parser=parser)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/xml/etree/ElementTree.py", line 1196, in parse
    tree.parse(source, parser)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/xml/etree/ElementTree.py", line 586, in parse
    source = open(source, "rb")
FileNotFoundError: [Errno 2] No such file or directory: '/Users/giulia/Desktop/dmas/FlowMas/maps/LuSTScenario/scenario/lust.net.xml'
```

__Solution__: you haven't initialized the LuSTScenario repo, run:

```
cd FlowMas/maps/
git clone https://github.com/lcodeca/LuSTScenario
```

### Error 14

__Traceback__:
```
2019-10-01 21:33:26,306	INFO resource_spec.py:205 -- Starting Ray with 2.05 GiB memory available for workers and up to 1.05 GiB for objects. You can adjust these settings with ray.remote(memory=<bytes>, object_store_memory=<bytes>).
Traceback (most recent call last):
  File "/Users/giulia/Desktop/dmas/FlowMas/simulation.py", line 192, in <module>
    local_mode=Params.DEBUG,  # use local mode when debugging, remove it for performance increase
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/worker.py", line 1495, in init
    head=True, shutdown_at_exit=False, ray_params=ray_params)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/node.py", line 145, in __init__
    self.start_head_processes()
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/node.py", line 513, in start_head_processes
    self.start_redis()
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/node.py", line 368, in start_redis
    include_java=self._ray_params.include_java)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/services.py", line 613, in start_redis
    stderr_file=redis_stderr_file)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/services.py", line 782, in _start_redis_instance
    stderr_file=stderr_file)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/services.py", line 400, in start_ray_process
    stderr=stderr_file)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/subprocess.py", line 729, in __init__
    restore_signals, start_new_session)
  File "/Users/giulia/anaconda3/envs/dmas/lib/python3.6/subprocess.py", line 1364, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
PermissionError: [Errno 13] Permission denied: '/Users/giulia/anaconda3/envs/dmas/lib/python3.6/site-packages/ray-0.7.4-py3.6-macosx-10.7-x86_64.egg/ray/core/src/ray/thirdparty/redis/src/redis-server'

```

__Solution__: Workaround is the ugliest thing you can do...

`sudo chmod -R a+wxr $HOME/anaconda3/envs/dmas/lib/python3.6/site-packages/<your-ray-version>/ray`