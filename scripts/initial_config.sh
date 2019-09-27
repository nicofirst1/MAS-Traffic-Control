source ~/.bashrc

os="$(uname)"


if [ $os = "Darwin" ]; then
# mac system
    sh scripts/initial_configs/ubuntu_initial_macosx.sh

elif [ $os = "Linux" ]
    # installing for ubuntu
    sh scripts/initial_configs/ubuntu_initial_config.sh
fi

# source bash
source ~/.bashrc 

