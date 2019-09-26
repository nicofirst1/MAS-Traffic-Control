
# update conda
conda update conda -y

# create envirnonment
echo "Creating enviroment..."

conda create --name dmas python=3.6

# install requirements
echo "Installing requirements..."
pip install -y -r requirements.txt


# Install flow develop
echo "Installing ray..."

git clone https://github.com/flow-project/ray.git
python ray/python/setup.py develop

# remove ray 
rm -rf ray

# call ubuntu install script for sumo 
echo "Updating..."

sh scripts/setup_sumo_ubuntu1804.sh

# install sumo tools
pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl

# configure package
python setup.py install