#!bin/bash

CUR_DIR="$(pwd)"
LIBS_DIR="libs"
# create tmp folder

mkdir $LIBS_DIR

if [ ! -d "$LIBS_DIR/flow" ]; then
    # install flow if not present
    cd libs
    git clone https://github.com/flow-project/flow.git
    cd flow

    # update conda
    conda update conda -y

    # create envirnonment
    echo "Creating enviroment..."

    # create a conda environment
    conda env create -f environment.yml --name dmas

    source activate dmas

    # install flow within the environment
    pip install -e .

else 
    source activate dmas
fi

# call  install script for sumo 
echo "Installing SUMO..."


if [ ! -d "$HOME/sumo_binaries/bin" ]; then

    os="$(uname)"

    if [ $os = "Darwin" ]; then
        sh scripts/sumo_setup/setup_sumo_macosx.sh

    elif [ $os = "Linux" ]; then

        sh scripts/sumo_setup/setup_sumo_ubuntu1804.sh
    fi

fi

cd $CUR_DIR

if [ ! -d "$LIBS_DIR/ray" ]; then


    # Install flow develop
    echo "Installing ray..."

    conda install libgcc
    pip install cython==0.29.0


    git clone https://github.com/ray-project/ray.git

    # Install Bazel.
    ray/ci/travis/install-bazel.sh


    # Install Ray.
    cd ray/python
    pip install -e . --verbose  # Add --user if you see a permission denied error.

fi

# install sumo tools
pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl


cd $CUR_DIR
# configure package
python setup.py install

# remove flow from packages
pip uninstall flow