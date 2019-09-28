#!/usr/bin/env bash


os="$(uname)"
installation_instruction="MarkDown/Installation.md"

if [ $os = "Darwin" ]; then
# mac system
    sh ./scripts/initial_configs/macOSX.sh

elif [ $os = "Linux" ]; then
    # installing for ubuntu
    sh ./scripts/initial_configs/ubuntu18.sh

else
  echo "This operating system is not supported yet! Please use the installation instruction in $installation_instruction"
fi

# launching python configuration
sh ./scripts/python_setup.sh