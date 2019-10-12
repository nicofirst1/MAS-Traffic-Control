

if [ $DEBUG_flag ]; then
  echo "[$DEBUG_id] 2) MacOSX initial configuration"
fi


if [ -z "$(which brew)" ]; then

    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 2.5) Installing brew"
    fi

    # install brew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null

    echo "Brew has been installed. Please quit the terminal and relaunch the script"
    exit 0

fi

# Installing packages with brew
brew update
brew install wget
brew install proj

brew install cmake openmpi
bash scripts/python_setup.sh
