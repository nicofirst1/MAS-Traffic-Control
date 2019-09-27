source ~/.bashrc

# updating apts
echo "Updating..."
sudo apt-get update    
sudo apt-get dist-upgrade 

# getting packages if not present 
echo "Installing packages...."

sudo apt-get -y install git-core build-essential curl pkg-config zip g++ zlib1g-dev unzip python3 wget psmisc

# If you are not using Anaconda, you need the following.

sudo apt-get install python3-dev  # For Python 3.

# check for conda 
conda="$(which conda)"

if [ -z "$conda" ]; then
    echo "Anaconda not detected, installing..."

    # install anaconda
    curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
    bash Anaconda3-2019.03-Linux-x86_64.sh 
    rm Anaconda3-2019.03-Linux-x86_64.sh 

fi


# source bash
source ~/.bashrc 

bash scripts/python_setup.sh