#!/bin/bash

# This comes up a lot with mounting stuff into stuff
git config --global --add safe.directory /workspaces/dct-campaign-resource-centre

# It's a nuisance to have to confirm this stuff
az config set extension.use_dynamic_install=yes_without_prompt

# Install requirements for operating the devcontainer
# (the application requirements will be installed in the application Dockerfile)
pip install -r ./.devcontainer/devrequirements.txt --user

# Install pre-commit hooks
pre-commit install
