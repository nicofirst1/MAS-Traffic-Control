

if [ $DEBUG_flag ]; then
  echo "[$DEBUG_id] 2) MacOSX initial configuration"
fi


if [ -z "$(which brew)" ]; then

    if [ $DEBUG_flag ]; then
        echo "[$DEBUG_id] 2.5) Installing brew"
    fi

    # install brew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null

fi

# Installing packages with brew
brew update
brew install wget
brew install proj


bash scripts/python_setup.sh
