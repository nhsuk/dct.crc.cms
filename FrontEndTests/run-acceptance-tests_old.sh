#!/bin/bash
set -e

### Run this script to run the contact_us_form acceptance tests
### Can pass in any parameters, such as --env "BASE_URL=-Dbase_url=https://www.nhs.uk"  or --env "TAGS=--tags=-notindev"

#Set the path to the feature files from the root of the acceptance test project folder
PATH_TO_TESTS=./FrontEndTests/feature

#Set the path to the root of the acceptance test project folder from where you are running this file from
PATH_TO_ACCEPTANCE_TEST_ROOT=..

if [ ! -z "$1" ]
  then
    echo "### You provided the arguments:" "$@"
fi

cd ${PATH_TO_ACCEPTANCE_TEST_ROOT}
echo "### Running from " $(pwd)

echo "### Removing old reports"
rm -rf ./report && mkdir ./report
echo "### Removing old log files"
rm -rf ./logs && mkdir ./logs
echo "### Removing old screenshots"
rm -rf ./screenshots && mkdir ./screenshots

echo "### Building docker image"
docker build -t acceptancetests -f AcceptanceTest.dockerfile .

echo "### Running docker image"

if [ $2 ]
then
  for i in "${@:2}"
  do
    echo "Starting container for TAG: $i"
    docker container run -d --name $i --env "PATH_TO_TESTS=${PATH_TO_TESTS}" --env "BASE_URL=-Dbase_url=\"$1\"" --env "TAGS=--tags=${i}" --env "NO_SKIPPED=--no-skipped" acceptancetests
  done
else
  cd './CRCV3_Tests/feature/'
  allFeaturesFiles=`ls *.feature`
  for eachFeatureFile in $allFeaturesFiles
  do
    echo "Starting container for Feature: $eachFeatureFile"
    docker container run -d --name $eachFeatureFile --env "PATH_TO_TESTS=${PATH_TO_TESTS}" --env "BASE_URL=-Dbase_url=\"$1\"" --env "TAGS=-i ${eachFeatureFile}" --env "NO_SKIPPED=--no-skipped" acceptancetests
  done
  # Go Back to Root Directory
  cd .. && cd ..
fi

echo "### Started running acceptance tests..."

# Check containers have exited at specified intervals in order to copy files to host and remove containers
TIMER=0
SLEEP_TIMER=30
CONTAINER_STILL_RUNNING=true
while $CONTAINER_STILL_RUNNING
do
  sleep $SLEEP_TIMER
  TIMER=$((TIMER+SLEEP_TIMER))
  # Fetch all running detached containers with its ID
  RUNNING_CONTAINERS=`docker container ps --all --filter "status=running" --format "{{.ID}}"`
  # If empty run if statement below
  if [[ -z $RUNNING_CONTAINERS ]]
  then
    # Fetch all stopped/exited detached containers with its NAME
    echo "### Total run time: $((TIMER/60)) mins and $((TIMER%60)) secs"
    STOPPED_CONTAINERS=`docker container ps --all --filter "status=exited" --format "{{.Names}}"`
    for CONTAINER_NAME in $STOPPED_CONTAINERS
    do
      # Copy test files to local agent/VM
      echo "### Copying report, logs and screenshots folder from container: "$CONTAINER_NAME" to host"
      docker cp $CONTAINER_NAME:/automation-ui/report/junit/ ./report
      docker cp $CONTAINER_NAME:/automation-ui/logs/ .
      docker cp $CONTAINER_NAME:/automation-ui/screenshots/ .

      # Checks the exit code for the container
      ExitCode=`docker inspect $CONTAINER_NAME --format='{{.State.ExitCode}}'`
      if [ $ExitCode != 0 ]
      then
        echo "### ***Potential Failure(s)!*** Test exited with code: $ExitCode for container: "$CONTAINER_NAME""
        PASSED=$ExitCode
      fi
    done
    # Remove all containers once tests have finished
    echo "### Removing all containers"
    docker rm $(docker ps -a -q)

    CONTAINER_STILL_RUNNING=false
  elif [[ $TIMER -gt 1200 ]]
  then
    # Stop and remove all containers if running for more than specified expected time
    echo "### Run limit reached for running containers. Removing all containers"
    docker kill $(docker ps -q) && docker rm $(docker ps -a -q)
    exit 1
  else
    echo "Tests are still running - Check back in $SLEEP_TIMER seconds. Current run time: $((TIMER/60)) mins and $((TIMER%60)) secs"
  fi
done

echo "### Finished running acceptance tests"
exit ${PASSED}
