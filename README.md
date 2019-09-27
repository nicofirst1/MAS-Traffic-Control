## Introduction 
This repo is about modelling the interaction between Autonomous Agents [AA] and Human Agents [HA] in a mixed traffic environment.
We simulate various scenarios such as: selfishness vs cooperativeness in AAs, behavior of AAs with varying number of HAs and other.

If you wish to learn more about the papers and the project goal refer to [Project_definiton.md](MarkDown/Project_definiton.md).

# Setup
This project relays on [Flow](https://github.com/flow-project/flow) a python framework which allows the interaction 
between [SUMO](http://sumo.sourceforge.net/userdoc/index.html) and various Reinforcement Learning [RL] libraries (such as [Ray](https://github.com/ray-project/ray)).

To install the required modules run the following commands:

- Install [anaconda](https://docs.anaconda.com/anaconda/install/)

- Source the bashrc

 `source ~/.bashrc`

- Create a custom environment with conda
 
 `conda create --name dmas python=3.6`

- Source custom environment: 

 `source activate dmas`

 - Install requirements:

 `pip install -r requirements.txt`
 

 - Install Ray by following [the instruction on ray](https://ray.readthedocs.io/en/latest/installation.html) and the ones[on flow](https://flow.readthedocs.io/en/latest/flow_setup.html#optional-install-ray-rllib)

- Install SUMO, either by using the [scripts](https://github.com/flow-project/flow/tree/master/scripts) in
  Flow or by using the [SUMO documentation](http://sumo.sourceforge.net/userdoc/Downloads.html) (Remember to
  link the SUMO binaries in your _.bashrc_).

- Install sumotools: 

`pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl`

- Lastly configure packages:

`python setup.py install` 

#

Once you are done you can run the first Tutorial with:

`python FlowMas/Tutorials/1_GridMapNoLights.py`

## Repo structure

There repository is currently structured as follows:

- The [flow](flow) core framework, containing modified files
- [FlowMas](FlowMas): the project's core containing the following dirs:
    - [maps](FlowMas/maps): a dir containing custom maps, you can follow the [readme](FlowMas/maps/README.md) for further information.
    - [Tutorials](FlowMas/Tutorials): which has an incrementing number of tutorials each being a step forward in the final implementation of the project. You can check the [tutorial readme](FlowMas/Tutorials/README.md) for more infos.
    - [utils](FlowMas/utils): contains utility scripts
    - [simulation.py](FlowMas/simulation.py): which is the main file for training and evaluating the RL agents
- [MarkDown](MarkDown): a directory for useful markdowns:
    - The [Error](MarkDown/Errors.md) markdown file contains common errors encountered during the project development.
    - The [Journal](MarkDown/Journal.md) markdown file has both an _useful_link_ section as well as a _todo_ section in which the project'steps are enumerated.
    - The [Project_definiton](MarkDown/Project_definiton.md) markdown file holds the project' specifications.
    