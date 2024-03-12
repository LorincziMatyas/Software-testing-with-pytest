#!/bin/bash

# Check if folder name is provided as a parameter
if [ -z "$1" ]; then
  echo "Usage: $0 <folder_name>"
  exit 1
fi

# Create the directory
mkdir "$1"

# Change directory to the newly created folder
cd "$1" || exit

# Set up the virtual environment
python3 -m venv "${1}-env"

# Activate the virtual environment
source "${1}-env/bin/activate"

# Install dependencies
python3 -m pip install --upgrade pip
pip3 install pytest sqlalchemy

# Run pytest
# pytest -v

# Deactivate the virtual environment
# deactivate


# test file name should be: '*_test.py' or 'test_*.py

