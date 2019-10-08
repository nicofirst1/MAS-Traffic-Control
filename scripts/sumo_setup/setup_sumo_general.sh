
cd libs
git clone --recursive https://github.com/eclipse/sumo
cd sumo
mkdir build
cd build
cmake ../
make -j8
export SUMO_HOME="$PWD"

echo "Please add the following to your .bashrc"
echo "export SUMO_HOME=$PWD"