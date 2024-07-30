# Campaign Resource Centre Wagtail site

## Introduction

The campaign resource centre (CRC) is a government site responsible for providing resources associated with various NHS digital campaigns as well as "how to guides" to assist users planning their own marketing campaigns.

The live site can be found here:  
https://campaignresources.dhsc.gov.uk/

Online documentation for CRC can be accessed on Confluence (using your nhs.net email address) and a couple of helpful links are provided below.

Current version 'homepage':  
https://digitaltools.phe.org.uk/confluence/display/CRC/CRC+V3

Development related documentation:  
https://digitaltools.phe.org.uk/confluence/display/CRC/Dev+CRC+V3

## Table of Contents

<!-- vim-markdown-toc GitLab -->

* [Architecture](#architecture)
* [Running the project](#running-the-project)
* [Front-end testing](#front-end-testing)
* [Performance testing](#performance-testing)
* [Versioning](#versioning)
* [Development branches](#development-branches)
* [Build pipelines](#build-pipelines)
* [Release process](#release-process)

<!-- vim-markdown-toc -->

## Architecture

CRC operates using three servers:
1. Web application server:  
    * Python/ Django/ Wagtail
    * Most of this repo is devoted to this
2. Redis server:  
    * Used for caching
3. Database server (Postgres):  
    * Stores most of the persistent application data

The remaining persistent data fall into two categories:
1. File resources
    * Images, pdfs, videos, zip archives
    * Uploaded by content editors
2. Index entries
    * Each page or resource created needs an index entry which is a small JSON document
   used by the Azure search indexer

For further details, diagrams and external dependencies see the designated pages in Confluence:

https://digitaltools.phe.org.uk/confluence/display/CRC/Development+vs+Production+Architecture

#### Diagrams:
https://digitaltools.phe.org.uk/confluence/display/CRC/Technical+Architecture+Diagram  
https://digitaltools.phe.org.uk/confluence/display/CRC/Monitoring  
https://digitaltools.phe.org.uk/confluence/display/CRC/CRC+V3+sequence+diagrams  
https://digitaltools.phe.org.uk/confluence/display/CRC/CRC+V3+user+flow  

#### External Dependencies: 
https://digitaltools.phe.org.uk/confluence/display/CRC/Discovery+docs+-+Torchbox  
https://digitaltools.phe.org.uk/confluence/display/CRC/Wagtail+deployment  
https://digitaltools.phe.org.uk/confluence/display/CRC/Parkhouse+documentation+-+Solution+overview  

## Running the project

The recommended approach is to use **VSCode** and its **Dev Containers extension**. A devcontainer is a docker image encapsulating all the development requirements for a project. It overcomes the problems encountered when maintaining different applications and versions thereof on the same development machine.

### Pre-reqs

- Docker Desktop:
  - This now contains both the Docker Engine and docker-compose
  - See https://docs.docker.com/desktop/ for documentation and download links
- Visual Studio Code:
  - The IDE needed for development of this project
  - See https://code.visualstudio.com/docs for documentation and download links
- Dev Containers extension for VSCode:
  - Needed to run a docker container to be used for development
  - See https://code.visualstudio.com/docs/devcontainers/containers for documentation

### Configuration

CRCv3 uses .env files to store local configuration settings. 

```
./.env
```

This file is excluded from git and won't be included in your cloned repo because it will contain secrets. Instead, you should obtain your .env securely from a colleague.

Further details of some of the environment variables set within the .env file can be found here in Confluence:  
https://digitaltools.phe.org.uk/confluence/display/CRC/Environment+Variables+-+the+.env+file

### Dev Container setup:

First, ensure you have Docker Desktop running and the Dev Containers extension installed in VSCode.

If you already have the project open in VSCode then you can run the `'Dev Containers: Open Folder in Container...'` command from the bar (command palette) at the top of the screen.

If not, then when you do open the project folder in VSCode, it will detect the .devcontainer directory and start trying to run this same command automatically for you.

This creates and runs (or attaches to if already created) a Docker container that will be visible in your Docker Desktop app. Building the dev container for the first time will take several minutes.

Continue your setup and later development in a terminal window (or windows) you can open in the running devcontainer using the VSCode Terminal menu. Your host folder where you checked out the CRC repository is mounted into the default folder of the dev container terminal sessions.

To read further on using Dev Containers with CRC see the following Confluence page:  
https://digitaltools.phe.org.uk/confluence/display/CRC/Developing+CRCv3+with+a+devcontainer

### Local database sync 

To have the locally running website populated with pages and resources (like those you see in the live site) you will need to run the sync-db command (you can proceed without this step and you will see a very basic, empty form of the website).

This command takes the environment you want to sync with, the choices being "staging", "integration" or "review". It also requires the storage key for the "digitalcampaignsstorage" storage account which stores the database dump files.

To run this command, in the terminal made available by VSCode, enter the following command:

`fab sync-db <environment> <storage-key>`

For more details on syncing your local database see the following Confluence page:  
https://digitaltools.phe.org.uk/confluence/display/CRC/Local+Database+Sync

### Boot up the website for the first time

Starting a local build can be done by running:

```bash
fab build
fab start
fab sh
```

Then within the SSH session:

```bash
dj migrate
dj createsuperuser OR dj preparetestdata
djrun
```

preparetestdata creates a superuser username wagtail password wagtail and creates a rudimentary CRC site with the CRC taxonomy terms installed.

The site should now be available on the host machine at: http://127.0.0.1:8000/

### Front-end tooling

After starting the containers as above and running `djrun`, in a new terminal session run `fab npm start`. This will start the frontend container and the site will be available on port :3000 using browsersync, e.g. `localhost:3000`.

## Front-end testing

Containers are also used for running front-end tests locally since they too have complex dependencies. The tests are all defined in the FrontEndTests folder and get built into a docker image called "acceptancetests" that is stored in the "dctimages.azurecr.io" docker image repository. The version of the tests being run is dictated by the Image Tag the test container is using so make sure you are providing the up to date tag. The construction of the image is detailed here in  a separate GitHub repository:  
<https://github.com/nhsuk/dct-frontend-testing-framework>

### Configuration

Configuration related to testing focusses on accessing and specifying the aforementioned "acceptancetests" docker image:

* REPO_USERNAME and REPO_PASSWORD:  
credentials used to access the "dctimages.azurecr.io" docker image repository.  

* SECRETS_FILE:  
CSV file containing details of registered users of the CRC site (your email address, your CRC password).  

* IMAGE_TAG:  
The version of the "acceptancetests" build to use (e.g. 1.1.1) - leave empty to run "latest".

* TAGS:  
Used to determine which subset of tests to run (e.g. "@Smoke") - leave empty to run all tests. 

### In the build pipeline

The "smoke" tests are automatically run within this build pipeline whenever a review branch is created or modified:  
https://dev.azure.com/nhsuk/dct.campaign-resource-centre-v3/_build?definitionId=1071&_a=summary

From here you can click "Edit", then "Variables" and provide REPO_USERNAME REPO_PASSWORD and IMAGE_TAG (named FRONTEND_TEST_CONTAINER_IMAGE_TAG in the pipeline variables). The other variable secrets file and tags are specified within the pipeline itself.

The results for the front end tests run in the build pipeline can be found in the "Deploy" stage or the "Deploy Review" job under the "Run Frontend tests in Docker container" task.

### Testing locally

To run the front end tests locally you need to provide the same environment variables in a test_env.sh file.

This file is excluded from git and won't be included in your cloned repo because it will contain secrets. Instead, you should obtain the test_env.sh file securely from a colleague.

You will also need to create the CSV secrets file and provide its path as the SECRETS_FILE value, e.g. $PWD/user-details.csv

An example test_env.sh:

```
export BASE_URL=http://localhost:8000
export REPO_USERNAME=**************
export REPO_PASSWORD=************************************
# Note that secrets file requires absolute path because it will be mounted into the container
export SECRETS_FILE=$PWD/crcv3-1-user.csv
export IMAGE_TAG=1.0.0
```

To run the tests, first get your local CRC instance running in a terminal window:

```bash
fab start
fab sh
djrun
```

then start a second terminal window to run the tests:

```bash
. ./test_env.sh
./execute-frontendtests.sh
```

## Performance testing

Performance testing was required at the start of the project to demonstrate the suitability of the design but it still remains a good idea to aim to have it run monthly to ensure the high performance of the project is maintained. 

### In a pipeline

Performance testing can be run from within a pipeline found here:  
https://dev.azure.com/nhsuk/dct.campaign-resource-centre-v3/_build?definitionId=1074&_a=summary

For more information, see this page in Confluence:  
https://digitaltools.phe.org.uk/confluence/display/CRC/Performance+testing+framework

### Testing locally

* Download jmeter tool from https://jmeter.apache.org/download_jmeter.cgi and install.
* Sample jmx script is added under PerformaceTests folder.
* Start the jmeter application with interface.
* Load the jmx file and check the values for 'Number of threads(users)', 'Ramp-up period' and 'Duration' i.e currently set to 100, 10 and 60 respectively.
* Click run button and view the results on by clicking on either 'View Results Tree' or 'Summary Report'.

## Versioning

Versioning methods would ideally be standardised and consistent across projects. The common page detailing versioning methods is here in Confluence:  
https://digitaltools.phe.org.uk/confluence/display/DTB/Versioning+Standards

## Development branches

Branching would ideally be standardised and consistent across projets. The common page detailing the use of branches for development is here in Confluence:  
https://digitaltools.phe.org.uk/confluence/display/DTB/Development+branching

## Build pipelines

All of the build pipelines for this project can be found here:  
https://dev.azure.com/nhsuk/dct.campaign-resource-centre-v3/_build?view=folders

The main pipeline for building and deploying a CRC instance is here:
https://dev.azure.com/nhsuk/dct.campaign-resource-centre-v3/_build?definitionId=1071

This pipeline allows the specifying of the following variables when run manually:
* DEBUG - Django debug mode (true/y/false/n), default False
* TAGS - Tag or tags to select front-end tests to be run in the build. Defaults to 'Smoke' for smoke tests only
* PARAGON_MOCK - Mock the Paragon API (true/y/false/n) default False
* NOTIFY_DEBUG - Mock the government notification API (true/y/false/n)
default True except in production
* WEB_WORKERS - Number of concurrent Django processes per pod to handle requests default 5
* GUNICORN_CMD_ARGS - Optional parameters to pass to Gunicorn server

When DEBUG is false Django is run with the Gunicorn server, when true with the Django runserver server. Non-debug mode requires a setting for WEB_WORKERS.

## Release process

The release process would ideally be standardised and consistent across projects. The common page detailing the release process is here in Confluence:  
https://digitaltools.phe.org.uk/confluence/display/DTB/7.+Release+Process
