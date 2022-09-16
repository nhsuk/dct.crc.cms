#!/bin/bash

# Install go for gitleaks
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

# Install psql
sudo apt-get install -y postgresql-client
echo 'export PGUSER=campaignresourcecentre' >> ~/.bashrc
echo 'export PGPASSWORD=campaignresourcecentre' >> ~/.bashrc
echo 'export PGDATABASE=campaignresourcecentre' >> ~/.bashrc
echo 'export PGUSER=campaignresourcecentre' >> ~/.bashrc
echo 'export PGHOSTADDR=0.0.0.0' >> ~/.bashrc
