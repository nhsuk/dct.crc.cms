#!/bin/bash

# It's a nuisance to have to confirm this stuff
az config set extension.use_dynamic_install=yes_without_prompt

# Install requirements for operating the devcontainer (application requirements installed in application Dockerfile)

pip install -r ./.devcontainer/devrequirements.txt --user

# Install pre-commit hooks
pre-commit install
