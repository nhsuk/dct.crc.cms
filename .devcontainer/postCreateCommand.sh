#!/bin/bash
set -euo pipefail


sudo apt-get update -y && sudo apt-get install -y openssh-client

# This comes up a lot with mounting stuff into stuff
git config --global --add safe.directory /workspaces/dct-campaign-resource-centre

# --------------------------
# Install correct ARM64 Go
# --------------------------
GO_VERSION=1.19   # stick to your project’s required version, or bump to a newer if allowed
wget "https://go.dev/dl/go${GO_VERSION}.linux-arm64.tar.gz"
sudo tar -C /usr/local -xzf "go${GO_VERSION}.linux-arm64.tar.gz"
rm "go${GO_VERSION}.linux-arm64.tar.gz"


# --------------------------
# Install correct ARM64 gitleaks
# --------------------------

sudo rm -f /usr/local/bin/gitleaks 2>/dev/null || true

GITLEAKS_VERSION=8.16.2
wget "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_arm64.tar.gz"
tar -xzf "gitleaks_${GITLEAKS_VERSION}_linux_arm64.tar.gz"
sudo mv gitleaks /usr/local/bin/
rm "gitleaks_${GITLEAKS_VERSION}_linux_arm64.tar.gz"

which gitleaks
gitleaks version



# Configure the environment

# Ensure PATH includes the new Go
if ! grep -q '/usr/local/go/bin' ~/.bashrc; then
  echo 'export PATH="$PATH:/usr/local/go/bin"' >> ~/.bashrc
fi
# Reload shell rc (or open a new terminal)
source ~/.bashrc || true

# Verify
which go
go version
go env GOARCH

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

if ! [ -f .env ]; then
    echo ".env file does not exist. Creating new ..."
    cp .env.example .env
fi
