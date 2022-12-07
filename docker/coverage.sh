#!/bin/sh
python manage.py migrate
echo "1"
python manage.py test --noinput 
echo "2"
coverage erase 
echo "3"
coverage run manage.py test --settings=campaignresourcecentre.settings.test
echo "4"
coverage xml -i 
echo "5"
mv ./coverage.xml ./docker