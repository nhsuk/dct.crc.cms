#!/bin/bash

# Execute the front-end tests for this repo
# Note this file is not specific to CRC. The same script can test any repository having
# a front-end tests folder.

# Test are executed in a temporary subdirectory
# Report files from the tests are available there

# Requires these environment values:

# BASE_URL: URL of the deployment to be tested (https:// + domain)
# SECRETS_FILE: Path to CSV file containing username/password pair(s)
# REPO_USERNAME: Username for the Docker repository with the Front End test image
# REPO_PASSWORD: Password "
# IMAGE_TAG: Tag for required version of the Front End test image
# PARALLEL - number of parallel runs to execute (default 1)
# SCENARIOS - how to run scenarios (sequential/parallel, default sequential)

echo "### IMAGE_TAG: ${IMAGE_TAG:=1.1.1}"
echo "### PARALLEL: ${PARALLEL:=1}"
echo "### SCENARIOS: ${SCENARIOS:=sequential}"
echo "### TIMEOUT: ${TIMEOUT:=3000}s"

# Can't have empty value for TAGS as pipeline parameter so change "all" to "" here
TAGS=$([ "$TAGS" = "all" ] && echo "" || echo "$TAGS")
echo "Effective TAGS: '$TAGS'"

# Create a temporary directory for the tests
REPO_ROOT=$(pwd)
WORK=$(mktemp -d -t frontendtest-XXXXXXXXXX)
echo "Test ${BASE_URL:?No deployment URL specified (BASE_URL)} in $WORK with tags [$TAGS]"

cp -r FrontEndTests $WORK
mkdir $WORK/work
cd $WORK/work

echo "### Running docker container image ${IMAGE_TAG:?No image tag specified (IMAGE_TAG)}"
docker login dctimages.azurecr.io -u ${REPO_USERNAME:?No username for the Docker repo (REPO_USERNAME)} -p ${REPO_PASSWORD:?No password for the Docker repo (REPO_PASSWORD)}
docker build --build-arg IMAGE_TAG=${IMAGE_TAG} -t my-acceptancetests:${IMAGE_TAG} -f $REPO_ROOT/Dockerfile-FrontendTests .

printf  'Docker Build completed'

# Wait for the BASE_URL to be available or timeout after one minute

for i in {1, 6}
do
  curl --output /dev/null -k --head --fail --max-time 10 ${BASE_URL} && break
  printf 'Failed to access server, trying again in 10 seconds...\n'
  sleep 10
done
printf  'Server seems to be responding - confirm\n'
# Confirm site now running or fail
curl --output /dev/null -k --head --fail --max-time 10 ${BASE_URL} || exit 1
printf  'Server responded. Running tests now\n'

# get Docker to use host network so it can access localhost:8000 with no fuss
docker run \
  --network host \
  --env BASE_URL \
  --env TAGS \
  --env PARALLEL=$PARALLEL \
  --env SCENARIOS=$SCENARIOS \
  --env TIMEOUT=$TIMEOUT \
  --env WAGTAIL_USER \
  --env WAGTAIL_PASSWORD \
  --env WAGTAIL_AUTOMATION_USERNAME \
  --env WAGTAIL_AUTOMATION_PASSWORD \
  --env WAGTAIL_TOTP_URI \
  --mount type=bind,source=$WORK/FrontEndTests,target=/automation-ui/FrontEndTests \
  --mount type=bind,source=${SECRETS_FILE:?No secrets file specified (SECRETS_FILE)},target=/automation-ui/login.csv \
  my-acceptancetests:${IMAGE_TAG}
PASSED=$?
echo "Status of tests: $PASSED"


exit $PASSED