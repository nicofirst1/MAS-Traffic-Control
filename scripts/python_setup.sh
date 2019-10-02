#!bin/bash

# declare variables
CUR_DIR="$(pwd)"
LIBS_DIR="libs"
env_name="dmas"


if [ $DEBUG_flag ]; then
    echo "[$DEBUG_id] 3) Python setup"
fi

# create tmp folder
if [ ! -d "$LIBS_DIR/flow" ]; then
    mkdir $LIBS_DIR
fi
env="$(conda env list | grep $env_name)"

if [ ! -d "$LIBS_DIR/flow" ] || [ -z $env ]; then

    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.1) Installing flow"
    fi


    # install flow if not present
    cd $LIBS_DIR
    git clone https://github.com/flow-project/flow.git
    cd flow

    # update conda
    conda update conda -y

    # create envirnonment
    echo "Creating enviroment..."

     if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.2) Creating conda env "
    fi


    # create a conda environment
    conda env create -f environment.yml --name $env_name

    echo "...Conda environment created"

fi
    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.3) Donw with flow"
    fi


if [ ! $CONDA_DEFAULT_ENV=$env_name ] || [ -z $CONDA_DEFAULT_ENV ] ; then 

    echo "Please restart your terminal session and source the conda env with:"
    echo "'source activate $env_name'"
    echo "Then run the script again"
    exit
fi

if [ $DEBUG_flag ]; then
    echo "[$DEBUG_id] 3.4) Pip install flow"
fi


cd $LIBS_DIR/flow 
# install flow within the environment
pip install -e .

# installing other conda libs
conda install -y  -c conda-forge proj4

# call  install script for sumo 
echo "Installing SUMO..."


if [ ! -d "$HOME/sumo_binaries/bin" ]; then

    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.5) Installing sumo"
    fi

    os="$(uname)"

    if [ $os = "Darwin" ]; then
        sh scripts/sumo_setup/setup_sumo_macosx.sh

    elif [ $os = "Linux" ]; then

        sh scripts/sumo_setup/setup_sumo_ubuntu1804.sh
    fi

else

    echo "SUMO direcotry detected. Skipping installation"


fi

if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.6) Done with sumo"
fi

cd $CUR_DIR

if [ ! -d "$LIBS_DIR/ray" ]; then

    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.7) Installing ray"
    fi

    # Install flow develop
    echo "Installing ray..."

    conda install -y libgcc
    pip install cython==0.29.0

    cd $LIBS_DIR
    git clone https://github.com/ray-project/ray.git


    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.71) Installing bazel"
    fi

    # Install Bazel.
    ray/ci/travis/install-bazel.sh

    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.72) Done with bazel, installing pip devel "
    fi

    # Install Ray.
    cd ray/python
    pip install -e . --verbose  # Add --user if you see a permission denied error.
    
    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.73) Done with  pip devel "
    fi
else

    echo "Ray direcotry detected. Skipping installation"

fi


if [ $DEBUG_flag ]; then
    echo "[$DEBUG_id] 3.8) Done with ray, installin sumo tools "
fi

# install sumo tools
pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl

export SUMO_HOME="$HOME/sumo_binaries/bin"

if [ $DEBUG_flag ]; then
    echo "[$DEBUG_id] 3.9) Done with sumo tools, configuring setup "
fi


cd $CUR_DIR
# configure package
python setup.py install

if [ $DEBUG_flag ]; then
    echo "[$DEBUG_id] 4) Uninstalling flow package "
fi


# remove flow from packages
pip uninstall flow