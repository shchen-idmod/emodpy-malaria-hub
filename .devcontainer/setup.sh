#!/bin/bash
# Ensure system packages are updated
sudo apt update && sudo apt upgrade -y

# Install extra system dependencies if needed
sudo apt install -y build-essential curl git unzip zip

# Install additional Python packages
pip install --upgrade pip
pip install numpy pandas matplotlib seaborn jupyterlab ipykernel jupytext ipywidgets


# dev install emodpy-malaria (can be replace later with pip install emodpy-malaria from jfrog)
pip install -r requirements.txt --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple
pip install -e . --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple
# install idmtools
pip install idmtools[full] --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple --upgrade --force-reinstall
pip install idmtools-test --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple  --upgrade --force-reinstall
