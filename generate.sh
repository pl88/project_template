#!/bin/bash

FILE=$PWD/pyproject.toml

if [ -f "$FILE" ]; then
    echo "Poetry already initialized"
else
    echo "Choose project name:"
    read PROJECT_NAME

    echo "Name project Author:"
    read AUTHOR_NAME  #fix for spacebar

    echo "Choose a Python version:"
    read VERSION
    poetry init --name $PROJECT_NAME --description  "my proj" --author $AUTHOR_NAME --python $VERSION --dependency pytest --dev-dependency coverage -l MIT --no-interaction
    poetry env use 3.12.8
    poetry run python main.py $VERSION $PROJECT_NAME
fi