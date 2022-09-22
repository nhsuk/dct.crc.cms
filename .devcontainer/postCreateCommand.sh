#!/bin/bash

echo 'export PATH="$PATH:/opt/poetry/bin"' >> ~/.bashrc

# Install go for gitleaks
wget https://go.dev/dl/go1.19.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz
rm go1.19.linux-amd64.tar.gz
echo 'export PATH="$PATH:/usr/local/go/bin"' >> ~/.bashrc

# Install gitleaks
wget https://github.com/zricethezav/gitleaks/releases/download/v8.12.0/gitleaks_8.12.0_linux_x64.tar.gz
sudo tar -C /usr/local/bin -xzf gitleaks_8.12.0_linux_x64.tar.gz
rm gitleaks_8.12.0_linux_x64.tar.gz

pre-commit install

# Install azcopy
wget -O azcopy.tar https://aka.ms/downloadazcopy-v10-linux
sudo tar -C /usr/local/bin --strip-components=1 --wildcards -zxf azcopy.tar */azcopy
rm azcopy.tar
sudo chmod a+x /usr/local/bin/azcopy

az config set extension.use_dynamic_install=yes_without_prompt