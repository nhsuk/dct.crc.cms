#!/bin/sh
python manage.py migrate
echo "1"
python manage.py test --noinput 
echo "2"
mv ./testresults.xml ./docker
echo "3"
coverage erase 
echo "4"
coverage run manage.py test --keepdb
echo "5"
coverage xml -i
echo "6"
mv ./coverage.xml ./docker
echo "7"
coverage html -i -d coverage_html
echo "8"
mv ./coverage_html/* ./docker/coverage_html