
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
[own flow](flow) directory and that your python environment must be free of other flow installations.

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

Follow [git thread](https://github.com/ray-project/ray/issues/5715)