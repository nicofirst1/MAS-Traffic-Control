#!/bin/bash

echo "Installing system dependencies for SUMO"
sudo apt-get update
sudo add-apt-repository ppa:sumo/stable
sudo apt-get install -y cmake swig libgtest-dev python-pygame python-scipy
sudo apt-get install -y autoconf libtool pkg-config libgdal-dev libxerces-c-dev
sudo apt-get install -y libproj-dev libfox-1.6-dev libxml2-dev libxslt1-dev
sudo apt-get install -y build-essential curl unzip flex bison python python-dev
sudo apt-get install -y python3-dev
sudo pip3 install cmake cython

sudo apt-get install -y sumo sumo-tools sumo-doc

echo "SUMO_HOME=\"/usr/local/opt/sumo/share/sumo\"" > ~/.bashrc