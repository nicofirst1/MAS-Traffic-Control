

To install the required modules run the following commands:

- Install [anaconda](https://docs.anaconda.com/anaconda/install/) and update:
`conda update conda -y`

- Source the bashrc

 `source ~/.bashrc`
 
- Clone the flow repo:

```
git clone https://github.com/flow-project/flow.git
cd flow
```

- Create a custom environment with conda
 
 `conda env create -f environment.yml --name dmas`

- Source custom environment: 

 `source activate dmas`

 - Install requirements:

 `pip install -e .`
 
- Install cproj with :

`conda install -c conda-forge proj`

- Install SUMO by using the [SUMO documentation](http://sumo.sourceforge.net/userdoc/Downloads.html) (Remember to
  link the SUMO binaries in your _.bashrc_).

 - Install Ray by following [the instruction on ray](https://ray.readthedocs.io/en/latest/installation.html) and the 
 ones [on flow](https://flow.readthedocs.io/en/latest/flow_setup.html#optional-install-ray-rllib), using :
 
 ```
conda install libgcc
pip install cython==0.29.0

git clone https://github.com/ray-project/ray.git

# Install Bazel.
ray/ci/travis/install-bazel.sh


# Install Ray.
cd ray/python
pip install -e . --verbose  # Add --user if you see a permission denied error.

```

- Install baseline following [this](https://stable-baselines.readthedocs.io/en/master/guide/install.html)

- Install sumotools: 

`pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl`

- Configure packages:

`python setup.py install` 

- Lastly remove the flow package

`pip uninstall flow`