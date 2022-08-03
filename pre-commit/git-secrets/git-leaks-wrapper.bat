:: Calls gitleaks on the current repo using local config
gitleaks --repo-config-path="./pre-commit/git-secrets/nhsd-gitleaks-config.toml" --verbose

:: Scan all files within this repo for this commit
:: gitleaks --path=. --repo-config-path="./git-secrets/nhsd-gitleaks-config.toml" --verbose