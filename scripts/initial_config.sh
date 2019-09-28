#!/usr/bin/env bash


export DEBUG_flag=1
export DEBUG_id="debug101"

os="$(uname)"
installation_instruction="MarkDown/Installation.md"

if [ $DEBUG_flag ]; then
  echo "[$DEBUG_id] 1) Starting configuration"
fi


if [ $os = "Darwin" ]; then
# mac system
    echo " Mac OS detected"

    sh ./scripts/initial_configs/macOSX.sh

elif [ $os = "Linux" ]; then
    echo " Ubuntu OS detected"

    # installing for ubuntu
    sh ./scripts/initial_configs/ubuntu18.sh

else
  echo "This operating system is not supported yet! Please use the installation instruction in $installation_instruction"
fi

# launching python configuration
sh ./scripts/python_setup.sh