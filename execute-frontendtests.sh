#!/bin/bash

# Execute the front-end tests for this repo

# Test are executed in a temporary subdirectory
# Report files from the tests are available there

# Requires these environment values:

# BASE_URL: URL of the deployment to be tested (https:// + domain)
# SECRETS_FILE: Path to CSV file containing username/password pair(s)
# REPO_USERNAME: Username for the Docker repository with the Front End test image
# REPO_PASSWORD: Password "

# Can't have empty value for TAGS as pipeline parameter so change "all" to "" here
TAGS=$([ "$TAGS" = "all" ] && echo "" || echo "$TAGS")
echo "Effective TAGS: '$TAGS'"

WORK=$(mktemp -d -t frontendtest-XXXXXXXXXX)
echo "Test ${BASE_URL:?No deployment URL specified (BASE_URL)} in $WORK with tags: $TAGS"

cp -r FrontEndTests $WORK
mkdir $WORK/work
cd $WORK/work

echo "### Running docker image"
docker login dctimages.azurecr.io -u ${REPO_USERNAME:?No username for the Docker repo (REPO_PASSWORD)} -p ${REPO_PASSWORD:?No password for the Docker repo (REPO_PASSWORD)}
docker pull dctimages.azurecr.io/acceptancetests
docker run \
  --env BASE_URL \
  --env TAGS \
  --mount type=bind,source=$WORK/FrontEndTests,target=/automation-ui/FrontEndTests \
  --mount type=bind,source=${SECRETS_FILE:?No secrets file specified (SECRETS_FILE)},target=/automation-ui/login.csv \
  dctimages.azurecr.io/acceptancetests
echo "##vso[task.setvariable variable=PASSED;]$?"
echo "Status of tests: $PASSED"
exit $PASSED
