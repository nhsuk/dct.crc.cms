#!/bin/bash

### Run this script to run the contact_us_form acceptance tests
### Can pass in any parameters, such as --env "BASE_URL=-Dbase_url=https://www.nhs.uk"  or --env "TAGS=--tags=-notindev"

#Set the path to the feature files from the root of the acceptance test project folder
PATH_TO_TESTS=./Change4lifeTest/feature

#Set the path to the root of the acceptance test project folder from where you are running this file from
PATH_TO_ACCEPTANCE_TEST_ROOT=..

if [ ! -z "$1" ]
  then
    echo "### You provided the arguments:" "$@"
fi

cd ${PATH_TO_ACCEPTANCE_TEST_ROOT}
echo "### Running from " $(pwd)

echo "### Removing old reports"
rm -rf ./report
echo "### Removing old log files"
rm -rf ./logs
echo "### Removing old screenshots"
rm -rf ./screenshots

echo "### Building docker image"
docker build -t acceptancetests -f AcceptanceTest.dockerfile .

echo "### Running docker image"
docker run --env "PATH_TO_TESTS=${PATH_TO_TESTS}" $@ acceptancetests
#docker run --disable-dev-shm-usage
PASSED=$?

echo "### Copying report folder from container to host"
CONTAINER_ID=$(docker container list --all --last 1 --format "{{ .ID }}")
docker cp ${CONTAINER_ID}:/automation-ui/report ./report
echo "### Copying logs folder from container to host"
docker cp ${CONTAINER_ID}:/automation-ui/logs ./logs
echo "### Copying screenshots folder from container to host"
docker cp ${CONTAINER_ID}:/automation-ui/screenshots ./screenshots || echo "### ...no screenshots to copy"

echo "### Finished running acceptance tests"
exit ${PASSED}