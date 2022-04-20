
# Local Database Sync

  

We sometimes need to sync the local database in our development environment to a deployed enviroment such as staging.

#### This script will:

1. Download latest database dump for the specifed environment

2. Delete the existing database

3. Restore the database using the downloaded dump


### Backups and pipelines

A new backup of the database is made everyday at 7pm for all the environments. This is done via a Azure release pipeline that can be found [here](https://dev.azure.com/nhsuk/dct.campaign-resource-centre-v3/_release?_a=releases&view=mine&definitionId=2).

  

If there is a need for a fresh database dump you can trigger a new release on this pipeline.

  

### Database dumps

The database dumps are currently stored in project artifacts which can be found [here](https://dev.azure.com/nhsuk/dct.campaign-resource-centre-v3/_packaging?_a=feed&feed=dct-crcv3).

You can also download a database dump manully via the artifacts.

  

# Prerequisites

In order to run this script you will need to:

  

- Have the Azure CLI extenison installed

- Be logged into the Azure CLI

- Have the docker containers running (`fab start/fab qstart`)

### Setup
In order to use the script you will need the Azure CLI installed on your machine.
You can install Azure CLI for your system by following the instructions [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

**After sucessful installation run:**

    az login
  
**For WSL users you will need to run:**

    az login --use-device-code

## Commands and usage

There is a single command which can take multiple variables.

  

**Command:**

  

    fab sync-db <environment>

**Environments**

  

    staging

    integration

    review

**Example usage:**

    fab sync-db staging
