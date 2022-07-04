# NB Installation instructions for Windows and Mac have their own sections 
# NB For Windows, ensure all script and text files related to pre-commit have Unix (LF) line endings rather than Windows (CRLF)
# This does NOT affect your code files.

# High level process:
1. Install Python if not already there
2. Download the gitleaks executable
3. Install pre-commit
4. Configure git to run precommit hooks

---------

# Setup (Mac only - once per laptop)

# Ensure Python3 is installed. Ideally only have one version of python on your Mac.
* brew install python

# Install gitleaks using homebrew
* brew install gitleaks

# Install pre-commit using homebrew
* brew install pre-commit

---------

# Setup (Windows only - once per laptop)

# Ensure Python3 is installed. 
You can install either from inside Visual Studio or as a stand alone install from https://www.python.org/downloads/windows/
Add your .../PythonXX and .../PythonXX/Scripts folders into your User windows PATH environment variable

# Install git-leaks
download the "gitleaks-windows-amd64.exe" file from here https://github.com/zricethezav/gitleaks/releases

Put it in a folder which is in your windows PATH and rename it "gitleaks.exe" .

Windows Defender may try and stop you running it - you'll have to override this.

# Install pre-commit
Instructions and download for the pre-commit framework from https://pre-commit.com/

Open a command prompt as administrator - 

* pre-commit --version (to check whether it's installed)

If not installed, run this command to install (again, open command prompt as administrator)

* pip install pre-commit (uses the python pip command to install pre-commit. You will need to ensure the "pip" executable is in a folder in your PATH)

---------

# (To be done the first time a repository is cloned to a new laptop)

* cd <root folder of your repo>
* pre-commit install (This sets up the local git precommit hook - you can see the script in .git/hooks/pre-commit)


 Pre-commit hooks for this repository on this PC should now work


--- --- --- ---


#Additional Information
a. Configure new repository with git hooks and configuration 
b. Configure gitleaks


# a. (To be done once for every repository - this configures it for all users)
If configuring a new repository or one which does not already have pre-commit and git-leaks configured:

Copy the git-secrets and scripts folders and the .pre-commit-config.yaml files from another working repo.

Ensure the .gitattributes file in the repository contains the following rules:


    *.sh eol=lf
    .pre-commit-config.yaml eol=lf
    git-secrets/**/*.* eol=lf
    .gitattributes eol=lf
    *.toml eol=lf

These rules ensure that files which match each regex do not have their line endings changed from Unix(LF) to Windows(CRLF). Script and rule files have to have LF endings or the scripts will not work.

Push branch/repository back to server so it is accessible to other users



# b. Configuration (Git Leaks)

* Add details of secrets to scan in the form of regex expressions in git-secrets/nhsd-gitleaks-config.toml

* To add a scanning rule, e.g.
 [[rules]]
    description = "Google API key"
    regex = '''AIza[0-9A-Za-z\\-_]{35}'''
    tags = ["key", "Google"]

* To avoid false positives, add file/directory/string details to the allow list within git-secrets/nhsd-gitleaks-config.toml e.g.

[allowlist]
    description = "Allowlisted files"
    files = ['''^\.?gitleaks.toml$''',
    '''(.*?)(png|jpg|gif|doc|docx|pdf|bin|xls|pyc|zip|toml)$''',
    '''(go.mod|go.sum)$''',
	'''^[0-9a-zA-Z/\\]*test[0-9a-zA-Z_-]*.key$''',
	'''^POCD[0-9a-zA-Z_]*.xml$''']

* Control full scan vs staged files scan within git-leaks-wrapper.bat by commenting/uncommenting the command to run in git-leaks-wrapper.bat e.g.:

 ```
 # Just scan the files changed in this commit
 # gitleaks --repo-config-path="./git-secrets/nhsd-gitleaks-config.toml" --verbose

 # Scan all files within this repo for this commit
 gitleaks --path=. --repo-config-path="./git-secrets/nhsd-gitleaks-config.toml" --verbose
 ```

 * File descriptions:
 git-secrets/git-leaks-wrapper.bat - contains the scripts run as part of the git pre-commit hook
 git-secrets/nhsd-gitleaks-config.toml - contains the scan rules and allowed list (exceptions) for git-leaks
 .pre-commit-config.yaml - tells pre-commit what script(s) to run when the git pre-commit hook fires
 .git/hooks/pre-commit - a script which git runs (if it exists) before each commit. This is a built in feature of git.

 * Testing
 In the root folder of the git repository, run the command:
 gitleaks --path=. --repo-config-path="./git-secrets/nhsd-gitleaks-config.toml" --verbose