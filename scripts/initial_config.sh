#!/usr/bin/env bash


os="$(uname)"
installation_instruction="MarkDown/Installation.md"

if [ $os = "Darwin" ]; then
# mac system
    sh ./scripts/initial_configs/initial_config_macosx.sh

elif [ $os = "Linux" ]; then
    # installing for ubuntu
    sh ./scripts/initial_configs/initial_config_ubuntu.sh

else
  echo "This operating system is not supported yet! Please use the installation instruction in $installation_instruction"
fi


