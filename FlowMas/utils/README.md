This directory contains python scripts for utility reasons.

- [train_utils](FlowMas/utils/train_utils.py): contain various function to setup the configuration depending on the user choices.
- [maps_utils](FlowMas/utils/maps_utils.py): is for utility regarding loading, modifying and adding [maps](FlowMas/maps) 
- [parameters](FlowMas/utils/parameters.py): is a class used to store parameters for all kind of purpose
- [evaluation](FlowMas/utils/evaluation.py): contains the debugging part for the training evaluation, to add callback check [this](https://ray.readthedocs.io/en/latest/rllib-training.html#callbacks-and-custom-metrics)
- [plot_results](FlowMas/utils/plot_results.py): is a python script which can be used on a console to plot data from different training instances. 