#!/bin/bash 
# source bash
. ~/.bashrc


# updating apts
echo "Updating..."
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
    echo "Anaconda not detected, installing..."

    # install anaconda
    curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
    bash Anaconda3-2019.03-Linux-x86_64.sh 
    rm Anaconda3-2019.03-Linux-x86_64.sh 

    . ~/anaconda3/bin/activate
    conda init
fi


# source bash
. ~/.bashrc
