#!/bin/bash

# This comes up a lot with mounting stuff into stuff
git config --global --add safe.directory /workspaces/dct.crc.cms

# Install gitleaks
wget https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz
sudo tar -C /usr/local/bin -xzf gitleaks_8.30.1_linux_x64.tar.gz
rm gitleaks_8.30.1_linux_x64.tar.gz

# Install pre-commit hooks
pre-commit install

# Configure the environment
echo 'export PATH="$PATH:/opt/poetry/bin"' >> ~/.bashrc

# It's a nuisance to have to confirm this stuff
az config set extension.use_dynamic_install=yes_without_prompt

# Install requirements for operating the devcontainer
# (the application requirements will be installed in the application Dockerfile)
pip install -r ./.devcontainer/devrequirements.txt --user

# Install pre-commit hooks
pre-commit install

if ! [ -f .env ]; then
    echo ".env file does not exist. Creating new ..."
    cp .env.example .env
fi
