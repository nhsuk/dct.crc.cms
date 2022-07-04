#!/usr/bin/env bash

# Note that this will be invoked by the git hook from the repo root, so cd .. isn't required

# Scan the current commit
gitleaks protect --config "./git-secrets/nhsd-gitleaks-config.toml" --verbose --staged