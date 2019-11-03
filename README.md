## Introduction 
This repo is about modelling the interaction between Autonomous Agents [AA] and Human Agents [HA] in a mixed traffic environment.
We simulate various scenarios such as: selfishness vs cooperativeness in AAs, behavior of AAs with varying number of HAs and other.

If you wish to learn more about the papers and the project goal refer to [project report](MarkDown/Report.pdf) or, for a quiker summary, refer to the [Project_definiton.md](MarkDown/Project_definiton.md).

# Instructions

## Download

To download the repo use

`git clone --recursive https://gitlab.com/nicofirst1/mas_traffic`

## Setup

To get install the necessary packages use:

`bash scripts/initial_config.sh`

Note that the previous will install both _git_ and _anaconda_. If you encounter any error regarding one of the two please install them separately and rerun the script.

Then configure the python package with (ensure that your conda environment is dmas):

`python setup.py install`

If you encounter an error regarding SUMO_HOME not being defined, run the appropriate sumo install script in 
[sumo_setup](scripts/sumo_setup) with:

`source ~/.bashrc`

`conda activate dmas`

Supported OS:

- Ubuntu 18.04 LTS
- macOSX Mojave

If your OS is not supported or you encounter an error check the [installation file](MarkDown/Installation.md) for more detailed installation instructions.

## Running

Once you are done you can run the first Tutorial with:

`python FlowMas/Tutorials/1_GridMapNoLights.py`

## Training

For training you can use 

`python FlowMas/train.py {args}`

The training results will be saved in the [ray_result dir](FlowMas/data/ray_results). 

To get a list of possible arguments run 

`python FlowMas/train.py --help`

A complete list of attributes will be then printed. Notice that each attribute is documented in the
[param class](FlowMas/utils/parameters.py)

__NB__: If you change some attributes of the Params class, but the changes does not seem to be working, use:

`python setup.py install`

## Visualizing results

Once you have trained your agents you can use the [flow visualization framework](https://github.com/flow-project/flow/blob/master/tutorials/tutorial04_visualize.ipynb)
to visualize your results. Use :

`tensorboard --logdir=FlowMas/data/ray_results`

To use tensorboard visualization, this will display __every__ training you have in the [ray_result dir](FlowMas/data/ray_results).
If you rather use [matplotlib](https://matplotlib.org/) you can use the following command:

`python flow/visualize/plot_ray_results.py FlowMas/data/ray_results/experiment_dir/progress.csv`

where _experiment_dir_ is the directory containing thetraining instance you would like to visualize. This will show a list of 
possible parameter to visualize. To plot them simply add them to the command as:

`python flow/visualize/plot_ray_results.py FlowMas/data/ray_results/experiment_dir/progress.csv episode_reward_max episode_reward_mean`

Moreover, for visualizing the SUMO gui with your trained agent use:

`python flow/visualize/visualizer_rllib.py FlowMas/data/ray_results/experiment_dir/result/directory 1`


### Visualizing multiple training instances

Once you have populated the [ray_result dir](FlowMas/data/ray_results) with multiple training instances you can use the 
[plot_results script](FlowMas/utils/plot_results.py) to generate plots for different training parameters such as:
- Delays: selfish, cooperative, total
- Actions:  selfish, cooperative, total
- Jerks:  selfish, cooperative, total
- Rewards:  selfish, cooperative, total

#### Usage

To use the script just run it with:

`python FlowMas/utils/plot_results.py -input_dir  path/to/your/dir [-output_dir custom/output/folder ] `

For instance if you want to plot every training instance in your [ray_result dir](FlowMas/data/ray_results), use:

`python FlowMas/utils/plot_results.py -input_dir  FlowMas/data/ray_results `

An _out_ directory will be created in the  [ray_result dir](FlowMas/data/ray_results) containing your plots.



## Repo structure

There repository is currently structured as follows:

- The [flow](flow) git [fork](https://github.com/nicofirst1/flow) for flow framework
- [FlowMas](FlowMas): the project's core containing the following dirs:
    - [maps](FlowMas/maps): a dir containing custom maps, you can follow the [readme](FlowMas/maps/README.md) for further information.
    - [Tutorials](FlowMas/Tutorials): which has an incrementing number of tutorials each being a step forward in the final implementation of the project. You can check the [tutorial readme](FlowMas/Tutorials/README.md) for more infos.
    - [utils](FlowMas/utils): contains utility scripts, check the [README](FlowMas/utils/README.md) for more infos.
    - [train.py](Flowmas/train.py): main script for training the environment.
  -   [train_osm.py](Flowmas/train_osm.py): Failed attempt to work with
      [OSM maps]((https://github.com/flow-project/flow/blob/master/tutorials/tutorial06_osm.ipynb)). If
      you're intrested in solving this problem please see
      [this](https://github.com/flow-project/flow/issues/755).
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
    