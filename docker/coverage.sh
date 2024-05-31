#!/bin/sh
echo "running migrations..."
python manage.py migrate
echo "erasing old coverage..."
coverage erase 
echo "running tests..."
coverage run manage.py test --noinput --keepdb
exitcode=$?
echo "mounting test results"
mv ./testresults.xml ./docker
echo "generating xml coverage report..."
coverage xml -i
echo "mounting xml coverage report"
mv ./coverage.xml ./docker
echo "getnerating html coverage report..."
coverage html -i -d coverage_html
echo "mounting html coverage report"
mkdir ./docker/coverage_html
mv ./coverage_html/* ./docker/coverage_html
echo "exiting with code $exitcode"
exit $exitcode