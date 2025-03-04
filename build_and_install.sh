#!/bin/bash

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install build dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build and install the package
pip install -e .

# Run tests
pytest tlars/tests/

# Deactivate virtual environment
deactivate 