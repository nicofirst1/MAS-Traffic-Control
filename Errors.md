
## Problems
This file concersgeneral errors encountered while writing the software.

### - Could not connect to TraCI

Error: ` server at localhost:58127 [Errno 61] Connection refused`

Solution: wait, as written [here](https://stackoverflow.com/questions/40362275/using-sumo-and-traci-could-not-connect-to-traci-server-61)

### - No module named 'rllab'

Error: `ModuleNotFoundError: No module named 'rllab'`

Solution: You must install [rllab](https://github.com/rll/rllab) with the following commands:

- `git clone https://github.com/rll/rllab`
- `cd rllab`
- `source activate 'YourEnvName'`
- `python setup.py install`

Check out [this](https://gist.github.com/yuanzhaoYZ/15bb640e1751da163d6a01675d54825f) for installation with conda
and [this](https://rllab.readthedocs.io/en/latest/user/installation.html) for installation with custom environment.

Update: Flow is getting rid of *rllib* so you won't need it anymore.

### - Errors with importing custom environments and/or network

If you have any errors regarding importing custom environments and/or networks remember that we have our 
[own flow](flow) directory and that your python environment must be free of other flow installations.

### - File "mtrand.pyx" ValueError: a must be non-empty

Error:
```
File "mtrand.pyx", line 1126, in mtrand.RandomState.choice
ValueError: a must be non-empty
```

__Solution:__
As written [here](https://stackoverflow.com/questions/57069566/when-test-the-grid-scenario-there-is-an-valueerror) this problem is due to the lack of routes in the Router, so:
- Replace _GridRouter_ with _ContinuousRouter_
- Add _spacing="custom"_ to _InitialConfig()_



###  IndexError:  pos = start_pos[i][1], list index out of range

Error:
```  
File "/Users/oblintosh/Desktop/dmas/flow/envs/base.py", line 279, in setup_initial_state
pos = start_pos[i][1]
IndexError: list index out of range
```

Solution:  Router problem, same as before