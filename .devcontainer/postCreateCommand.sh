#!/bin/bash

# This comes up a lot with mounting stuff into stuff
git config --global --add safe.directory /workspaces/dct-campaign-resource-centre

# Install go
wget https://go.dev/dl/go1.19.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz
rm go1.19.linux-amd64.tar.gz
echo 'export PATH="$PATH:/usr/local/go/bin"' >> ~/.bashrc

# Install gitleaks
wget https://github.com/zricethezav/gitleaks/releases/download/v8.12.0/gitleaks_8.12.0_linux_x64.tar.gz
sudo tar -C /usr/local/bin -xzf gitleaks_8.12.0_linux_x64.tar.gz
rm gitleaks_8.12.0_linux_x64.tar.gz
echo 'export PATH="$PATH:/opt/poetry/bin"' >> ~/.bashrc
az config set extension.use_dynamic_install=yes_without_prompt
pre-commit install

# It's a nuisance to have to confirm this stuff
az config set extension.use_dynamic_install=yes_without_prompt

# Install requirements for operating the devcontainer
# (the application requirements will be installed in the application Dockerfile)
pip install -r ./.devcontainer/devrequirements.txt --user
# Packages that create commands need their aliases fixing in case they are factory-fitted
pipx upgrade black

# Install pre-commit hooks
pre-commit install