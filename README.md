# Campaign Resource Centre Wagtail site

## Technical documentation

This project contains technical documentation written in Markdown in the `/docs` folder. This covers:

- continuous integration
- deployment
- git branching
- project conventions

You can view it using `mkdocs` by running:

```bash
mkdocs serve
```

The documentation will be available at: http://localhost:8001/

# Setting up a local build

This repository includes `docker-compose` configuration for running the project in local Docker containers,
and a fabfile for provisioning and managing this.

## Dependencies

The following are required to run the local environment. The minimum versions specified are confirmed to be working:
if you have older versions already installed they _may_ work, but are not guaranteed to do so.

- [Docker](https://www.docker.com/), version 19.0.0 or up
  - [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) installer
  - [Docker Engine for Linux](https://hub.docker.com/search?q=&type=edition&offering=community&sort=updated_at&order=desc&operating_system=linux) installers
- [Docker Compose](https://docs.docker.com/compose/), version 1.24.0 or up
  - [Install instructions](https://docs.docker.com/compose/install/) (Linux-only: Compose is already installed for Mac users as part of Docker Desktop.)
- [Fabric](https://www.fabfile.org/), version 2.4.0 or up
  - [Install instructions](https://www.fabfile.org/installing.html)
- Python, version 3.6.9 or up

Note that on Mac OS, if you have an older version of fabric installed, you may need to uninstall the old one and then install the new version with pip3:

```bash
pip uninstall fabric
pip3 install fabric
```

You can manage different python versions by setting up `pyenv`: https://realpython.com/intro-to-pyenv/

## Application architecture

The CRC application may be run both on a local development machine or in the Azure cloud.

In both instances there are three servers:
1. web application server: Python/ Django/ Wagtail, most of this repo is devoted to this
1. redis server: Used for caching
1. database server (Postgres): Stores most of the persistent application data

The remaining persistent data fall into two categories:
1. file resources. (images, pdfs, videos, zip archives) uploaded by content editors
1. index entries. Each page or resource created needs an index entry which is a small JSON document
   used by the Azure search indexer.

The servers and resources are disposed quite differently locally and in the cloud.

The behaviour of the application is conditioned by its environment variables. The environment similarly is managed differently locally and in the cloud. Be very careful with adding or removing
environment variables as each one will require entries in several specification files
as described below.

The web server runs as a Docker container constructed using ./Dockerfile both locally and in the cloud.

The application uses two external web servers via APIs:
1. Parkhouse/Paragon API manages all information relating to end-users (content editors are Django/Wagtail users). There is a mock of this API which can be used for testing purposes. Usually we test with a non-production instance of the API which is shared by ALL non-production instances of CRC-V3.
1. Government notification API which is used to send emails to end-users. This is mocked in all CRC-V3 instances except private beta and production.

### Build modes

There are two build modes for Django set by the environment variable BUILD_ENV:
* dev
* production
dev is used for local builds, and production for cloud builds.
These influence Django settings (found in ./campaignresourcecentre/settings). Settings used are a combination of base.py extended by either dev.py or prod.py.
For local builds these in turn may be extended by a file local.py (which is named in .gitignore because it should not be committed to the repo).

### Local build structure

The local build is made by docker-compose using the specification in ./docker-compose.yml which orchestrates three Docker containers:
1. Redis
1. PostgreSQL
1. CRCv3
1. Front-end debugging tools
Media storage is in a folder /media, and index storage in a folder /index

The Docker Compose specification mounts several of your local files and folders
into corresponding folders on the web container, including the media and index folders
and the application source files. This means that live changes to these files in either
the local machine or in the container are shared.

Any environment variable required at run time must be set up in ./docker-compose.yml, either hard-coded or copying from your local shell environment.
The copying occurs at the time you run "docker-compose up" either explicitly or implicitly with "fab start".

### Azure cloud build structure

In the cloud CRCv3 has the following architecture.

The servers are orchestrated by Kubernetes. Each review branch, the integration build, the staging build and production build has its own cluster of servers with an externally visible endpoint.

1. web: one or more docker containers within the cluster (autoscales with load)
2. redis: a single docker container within the cluster
3. database: provided externally by an Azure Postgres SQL instance. All integration builds share
   the same server instance and database.

Storage is provided by two separate Azure storage containers, one for media and one for index files, each with identity and access keys
determined by environment variables.

Integration and review builds share the same Azure containers, staging, performance testing and production builds each have their own pair of containers.

A cloud build is made by executing an Azure pipeline. Typically is in executed automatically by commits in the Azure repository, but it may be run standalone if you need to change some parameters.

The pipeline is specified in ./aks-deployment-pipeline.yml and it provides contextual information for each of the deployments that may be built:
* review branch
* integration
* staging
* production
* disaster recovery

Environment variables must each be treated appropriately in ./aks-deployment-pipeline.yml and in the .aks/deploy.yml template used in that file. There are several sources for environment variable values in cloud builds:
* hard-coded in the specifications (and therefore stored in the repo)
* extracted from the secrets vault (each deployment has its own secrets vault)
* pipeline parameters
* pipeline variables

"Appropriately" here means an environment symbol value must be one of:
* hard-coded for a specific environment
  (e.g. DEBUG is hard-coded False in production builds)
* hard-coded identically in all environments
  (e.g. the same local cluster redis credentials are used in each deployment)
* retrieved from the secrets vault identically for all or several environments,
  i.e. the same key has the same value in several different vaults
* retrieved from the secrets vault with a value that is unique to the deployment

Beware that symbol values are copied more than once in the build process via intermediary names which must be chosen for each new symbol.

When a new environment variable is added, consideration should be given to whether it should be secret, i.e. it would be a security risk if it were disclosed. If a secret then it will require an entry in each secrets vault before it is used in a cloud deployment.

## Running the local build for the first time

If you are using Docker Desktop, ensure the Resources:File Sharing settings allow the cloned directory to be mounted in the web container (avoiding `mounting` OCI runtime failures at the end of the build step).

Before starting your build ensure that your .env file sets up appropriate values for the environment of your build. More specifics in a separate section below.

Starting a local build can be done by running:

```bash
fab build
fab start
fab sh
```

Then within the SSH session:

```bash
dj migrate
dj createsuperuser or dj preparetestdata
djrun

```

preparetestdata creates a superuser username wagtail password wagtail and creates a rudimentary CRC site with the CRC taxonomy terms installed.

Alternatively, you may clone an existing deployment of CRC and test against its full content.
```
T.b.a.
```

Whichever method you use the site should now be available on the host machine at: http://127.0.0.1:8000/

### Frontend tooling

There are 2 ways to run the frontend tooling:

#### With the frontend docker container (default)

After starting the containers as above and running `djrun`, in a new
terminal session run `fab npm start`. This will start the frontend container and the site will
be available on port :3000 using browsersync. E.G `localhost:3000`.

#### Locally

To run the FE tooling locally. Create a `.env` file in the project root (see .env.example) and add `FRONTEND=local`.
Running `fab start` will now run the frontend container and you can start npm locally instead

There are a number of other commands to help with development using the fabric script. To see them all, run:

```bash
fab -l
```

## Front-end assets

Frontend npm packages can be installed locally with npm, then added to the frontend container with fabric like so:

```bash
npm install promise
fab npm install
```

## Environment symbols

The .env file that you use will contain secrets, so you should obtain your .env securely from
a colleague.

The following symbols are of particular importance if you are running locally.

### AZURE_CONTAINER

If this setting is missing, blank or has the value "none" then media and index entries are stored in the local folders ./media and ./index (mapped into the web container and used by it).

If AZURE_CONTAINER is set that both triggers the use of Azure storage for these files, and provides the name of the Azure container within an Azure account.

Be aware that if you use an AZURE_CONTAINER you will need to specify valid Azure account credentials in other symbols and that if you use the same container as another deployment then files that your Wagtail instance creates, modifies or deletes will be shared with the other deployment, but its Wagtail database will have no knowledge of this. This is often not a problem because Wagtail adds a cache-busting suffix to file names and URLs but there remains a problem of potential conflicts especially over deletes.

### AZURE_SEARCH_UPDATE

This setting defaults to True. Presently it is only used when deleting pages or resources, and causes the index entry to be deleted immediately from the search index, as well as its JSON file being deleted from the index folder. When running locally it is wise to set it False especially if you are testing deleting in a cloned database, because the search index entry will be deleted affecting all users of that index.

### Pipeline parameter symbols

These may be used on an ad hoc basis to vary the operation of the CRCV3 web instance.
* DEBUG - Django debug mode (true/y/false/n), default False
* PARAGON_MOCK - Mock the Paragon API (true/y/false/n) default False
* NOTIFY_DEBUG - Mock the government notification API (true/y/false/n)
default True except in production
* WEB_WORKERS - Number of concurrent Django processes per pod to handle requests default 5
* GUNICORN_CMD_ARGS - Optional parameters to pass to Gunicorn server

When DEBUG is false Django is run with the Gunicorn server, when true with the Django runserver server.
Non-debug mode requires a setting for WEB_WORKERS.

## Installing new or updated python packages

Python packages are managed using the poetry installer. This is controlled by the file
poetry/pyproject.toml that lists the required packages and specifies minimal or exact versions
for each.

The accompanying file poetry/poetry.lock, if it exists, specifies the precise versions of both the
required packages and all their dependencies and is used instead of pyproject.toml. If it does not exist, then poetry creates it from the specification in pyproject.toml as its first action.

To add a new package, or upgrade an existing one:

1. add an entry for the package in poetry/pyproject.toml
   [as described here](https://python-poetry.org/docs/basic-usage/#specifying-dependencies)
   or modify the existing entry if upgrading. 
1. delete poetry/poetry.lock. This will force poetry to create an updated version next time it runs
1. rebuild your local container which will create the new poetry/poetry.lock to be committed to
   the repository along with the modified pyproject.toml

## Versioning

[Semantic Versioning](https://semver.org/) is used for release management for this project. 

Git tag format for versions is `<Major>.<Minor>.<Patch>`

Format: eg:`01.00.00`

Main integration branch is `main`

## Developing features

- Branch of from `main` to start working on a new feature:

```
git checkout -b feature/<feature-name>
```

- Publish your feature:

```
git push -u origin feature/<feature-name>
```

- Create a merge request on Azure Dev. You can do so using Web UI by loggin into https://dev.azure.com/nhsuk/_git/dct.oneyou-cms/pullrequests.

- Once approved by your peer merge. Either merge it from web UI or rebase your branch into main from dev environment:

```
git checkout main
```

```
git pull
```

```
git merge feature/<feature-name>
git push
```

- Close the PR and delete the feature branch.

During a release if any features are merged into main branch, minor number in the version should be incremented.

### Endpoints

Each CRCv3 deployment has its own subdomain with a front-end server providing HTTPS and request throttling. Within that subdomain the front-end routes only to the following endpoints:
* /resources...
* /crc-admin...
Other URLs are redirected to standard NHS error pages.

### Rebuilds

If you require your deployment to have non-default pipeline parameters as seen above, then the pipeline may be executed on an ad-hoc basis and the values may be changed on the submission form.

### Bug fixes

- Branch of from main using `fix` prefix

```
git checkout -b fix/<fix-name>
```

- Publish your fix:

```
git push -u origin fix/<fix-name>
```

- Create a merge request on Azure Dev. You can do so using Web UI by loggin into https://dev.azure.com/nhsuk/_git/dct.oneyou-cms/pullrequests.

- Once approved by your peer merge. Either merge it from web UI or rebase your branch into main from dev environment:

```
git checkout master
```

```
git pull
```

```
git merge fix/<feature-name>
git push
```

- Close the PR and delete the fix branch.

During a release if `main` only contains fixes, patch number should be incremented in the version. If there are any features merged in minor should be incremented instead.

These are used for tracking status of and deploying to the related environments.

### Review branch

Review branch is used if developers needs to review the feature/fix change on cloud deployed instance. In this case create review branch using `review/` prefix.

- Branch of from main using `review/` prefix

```
git checkout -b review/<fix-name>
```

- Publish your fix:

```
git push -u origin review/<fix-name>
```

- This will trigger the pipeline and deploy the application to aks cluster. Use `https://crc-v3-review-<fix-name>.nhswebsite-dev.nhs.uk` url to access the cloud deployed instance of the application.

## Performance test

- Download jmeter tool from https://jmeter.apache.org/download_jmeter.cgi and install.
- Sample jmx script is added under jmeter folder.
- Start the jmeter application with interface.
- Load the jmx file and check the values for 'Number of threads(users)', 'Ramp-up period' and 'Duration' i.e currently set to 100, 10 and 60 respectively.
- Click run button and view the results on by clicking on either 'View Results Tree' or 'Summary Report'.

Ref:
![plot](./jmeter/sample-jmeter.png)


## Paragon users

Paragon users can be viewed and managed via the Wagtail admin "Paragon users" view.

To access this, users must have admin level access or be in a group with either the "Can view Paragon users and change access level" or "Can view Paragon users and change all details" permission enabled.

In order for the "Paragon users" view to display the most recently registered users, the number of Paragon users must be stored. The Paragon API does not provide a direct method to access this value so it must be deduced from search results. A management command `update_num_users` has been created to fetch and cache the number of users. This management command should be run periodically - every few minutes or so.
