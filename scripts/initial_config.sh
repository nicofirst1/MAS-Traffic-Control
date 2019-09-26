

# updating apts
sudo apt-get update    
sudo apt-get dist-upgrade 

# getting packages if not present 
sudo apt-get install git-core
sudo apt-get install build-essential


# check for conda 
conda= $(which conda)

if [ -z "$conda" ] then;
    # install anaconda
    curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
    bash Anaconda3-2019.03-Linux-x86_64.sh 
    rm Anaconda3-2019.03-Linux-x86_64.sh 

fi



# source bash
source ~/.bashrc 

# update conda
conda update conda

# create envirnonment
conda create --name dmas python=3.6

# install requirements
pip install -r requirements.txt


# Install flow develop
git clone https://github.com/flow-project/ray.git
python ray/python/setup.py develop

# remove ray 
rm -rf ray

# call ubuntu install script for sumo 
sh scripts/setup_sumo_ubuntu1804.sh

# install sumo tools
pip install https://akreidieh.s3.amazonaws.com/sumo/flow-0.4.0/sumotools-0.4.0-py3-none-any.whl

# configure package
python setup.py install