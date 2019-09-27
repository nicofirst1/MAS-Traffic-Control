## Introduction 
This repo is about modelling the interaction between Autonomous Agents [AA] and Human Agents [HA] in a mixed traffic environment.
We simulate various scenarios such as: selfishness vs cooperativeness in AAs, behavior of AAs with varying number of HAs and other.

If you wish to learn more about the papers and the project goal refer to [Project_definiton.md](MarkDown/Project_definiton.md).

# Setup

To get install the necessary packages use:

`sh scripts/initial_config.sh`

Then configure the python package with:

`python setup.py install`

If your OS is not supported or you encounter an error check the [installation file](MarkDown/Installation.md) for more detailed
 installation instructions.

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
    - The [Installation](MarkDown/Installation.md) markdown file holds installation instruction.
- [scripts](scripts): contains shell scripts mainly for installation purposes
    - The [initial_configs](scripts/initial_configs) dir holds package installation for both ubuntu18 and macosx
    - The [sumo_setup](scripts/sumo_setup) dir holds sumo binary installation shell scripts
    - The [initial_config.sh](scripts/initial_config.sh) shell script is used in the setup.py file to start the installation process
    - The [python_setup.sh](scripts/python_setup.sh) shell script for setting up python environment.
    - The [kill_dmas.sh](scripts/kill_dmas.sh) script can be used to kill background processes running SUMO.
    