#!/usr/bin/env python3
import os,sys
import subprocess

def gitleaksEnabled():
    out = subprocess.getoutput("git config --bool hooks.gitleaks")
    if out == "false":
        return False
    return True

if gitleaksEnabled():
    exitCode = os.WEXITSTATUS(os.system('gitleaks protect -v --staged'))
    if exitCode == 1:
        print('''Warning: gitleaks has detected sensitive information in your changes.
To disable the gitleaks precommit hook run the following command:
    git config hooks.gitleaks false
''')
        sys.exit(1)
else:
    print('gitleaks precommit disabled (enable with `git config hooks.gitleaks true`)')

# import subprocess

# cmd = 'gitleaks protect --config "./git-secrets/nhsd-gitleaks-config.toml" --verbose --staged'

# subprocess.run(cmd, shell=True)  # returns the exit code in unix

# #gitleaks --repo-config-path="./git-secrets/nhsd-gitleaks-config.toml" --verbose