#!bin/bash
# update conda
conda update conda -y

# create envirnonment
echo "Creating enviroment..."

conda create --name dmas python=3.6

source activate dmas

# install requirements
echo "Installing requirements..."
pip install -r requirements.txt


# Install flow develop
echo "Installing ray..."

git clone https://github.com/flow-project/ray.git
cd ray/python/
python setup.py develop
cd ../..


# call ubuntu install script for sumo 
echo "Updating..."


os="$(uname)"



if [ $os = "Darwin" ]; then
sh scripts/setup_sumo_macosx.sh

else

sh scripts/setup_sumo_ubuntu1804.sh
fi


# install sumo tools
pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl

# configure package
python setup.py install