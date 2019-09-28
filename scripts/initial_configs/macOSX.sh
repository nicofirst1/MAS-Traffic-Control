
if [ -z "$(which brew)" ]; then

    # install brew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null

fi

# Installing packages with brew
brew update
brew install wget
brew install proj


bash scripts/python_setup.sh
