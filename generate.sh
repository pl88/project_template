#!/bin/bash

FILE=$PWD/pyproject.toml

if [ -f "$FILE" ]; then
    echo "Poetry already initialized"
else
    echo "Choose project name:"
    read PROJECT_NAME
    if [ -z "$PROJECT_NAME" ]; then
        echo "Project name cannot be empty"
        echo "Using default name 'my_project'"
        PROJECT_NAME="my_project"
    fi

    echo "Name project Author:"
    read AUTHOR_NAME  #fix for spacebar
    if [ -z "$AUTHOR_NAME" ]; then
        echo "Author name cannot be empty"
        echo "Using default name 'my_name'"
        AUTHOR_NAME="my_name"
    fi

    echo "Choose a Python version:"
    read VERSION
    if [ -z "$VERSION" ]; then
        echo "Python version cannot be empty"
        echo "Using default version '3.12.0'"
        VERSION="3.12.0"
    fi

    if ! pyenv versions --bare | grep -q "^$VERSION$"; then
        echo "Python version $VERSION is not installed. Installing now..."
        pyenv install $VERSION
    fi
    pyenv local $VERSION
    

    poetry init --name $PROJECT_NAME --description  "my proj" --author $AUTHOR_NAME --python ^$VERSION --dependency pytest --dev-dependency coverage -l MIT --no-interaction
    poetry env use $(pyenv which python)
    poetry add fastapi
    poetry add uvicorn
    poetry install --no-root
    poetry run python main.py $VERSION $PROJECT_NAME
fi