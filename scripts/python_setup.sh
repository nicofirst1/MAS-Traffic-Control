
python_install(){

  check_env

  #flow_requirements


  if [ ! $CONDA_DEFAULT_ENV = $env_name ] || [ -z $CONDA_DEFAULT_ENV ] ; then

      echo "Please restart your terminal session and source the conda env with:"
      echo "'source activate $env_name'"
      echo "Then run the script again"
      exit 1
  fi

  # call  install script for sumo
  sumo_install


  ray_installation


  conda install --file requirements.txt

  # install sumo tools
  pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl


  if [ $DEBUG_flag ]; then
      echo "[$DEBUG_id] 3.9) Done with sumo tools, configuring setup "
  fi


  cd $CUR_DIR
  # configure package
  python setup.py install



  # instlaling stable baseline
  pip install stable-baselines

}

ray_installation(){



  if [ ! -d "$LIBS_DIR/ray" ]; then

      if [ $DEBUG_flag ]; then
          echo "[$DEBUG_id] 3.7) Installing ray"
      fi

      # Install flow develop
      echo "Installing ray..."

      conda install -y libgcc
      pip install cython==0.29.0

      cd $LIBS_DIR
      git clone https://github.com/ray-project/ray/tree/releases/0.7.6


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

  cd $CUR_DIR

}


sumo_install(){
  echo "Installing SUMO..."


if [ $DEBUG_flag ]; then
    echo "[$DEBUG_id] 3.5) Installing sumo"
fi

os="$(uname)"

if [ $os = "Darwin" ]; then
    sh scripts/sumo_setup/setup_sumo_osx.sh

elif [ $os = "Linux" ]; then

    sh scripts/sumo_setup/setup_sumo_ubuntu1804.sh
fi


if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 3.6) Done with sumo"
fi

cd $CUR_DIR


}


flow_requirements(){


  if [ ! -d "$LIBS_DIR/flow" ]; then

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


    # install requirements
    pip install -r requirements.txt

    echo "Installed requirements for flow"

fi


if [ $DEBUG_flag ]; then
    echo "[$DEBUG_id] 3.3) Done with flow"
fi


}

check_env(){
  env="$(conda env list | grep $env_name)"

  if [ -z $env ]; then

    echo "No conda environment detected!"
    echo "Run:"
    echo "conda create -n $env_name python=3.6"
    echo "Source it with:"
    echo "conda activate $env_name"
    exit 1

  fi
}