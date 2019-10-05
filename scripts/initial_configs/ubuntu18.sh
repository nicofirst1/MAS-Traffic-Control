#!/bin/bash 
# source bash
. ~/.bashrc


 if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 2) Ubuntu initial configuration"
    fi


# updating apts
echo "Updating apt..."
sudo apt-get update    
sudo apt-get -y dist-upgrade 

# getting packages if not present 
echo "Installing packages...."

sudo apt-get -y install git-core build-essential curl pkg-config zip g++ zlib1g-dev unzip python3-dev wget psmisc
sudo apt-get -y install libproj-java libproj9 proj proj-data

# If you are not using Anaconda, you need the following.

# check for conda 
conda="$(which conda)"

if [ -z "$conda" ]; then

    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 2.5) Anaconda not detected, installing..."
    fi


    # install anaconda
    curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
    bash Anaconda3-2019.03-Linux-x86_64.sh 
    rm Anaconda3-2019.03-Linux-x86_64.sh 

    . ~/anaconda3/bin/activate
    conda init
fi

# installing stble baseline
sudo apt-get install -y cmake libopenmpi-dev python3-dev zlib1g-dev

# source bash
. ~/.bashrc
