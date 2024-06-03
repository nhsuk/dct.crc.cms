#!/bin/sh
echo "[1/9] Running migrations..."
python manage.py migrate

echo "[2/9] Erasing old coverage..."
coverage erase

echo "[3/9] Running tests..."
coverage run manage.py test --noinput --keepdb
exitcode=$?

echo "[4/9] Mounting test results..."
mv ./testresults.xml ./docker

echo "[5/9] Generating xml coverage report..."
coverage xml -i --skip-empty

echo "[6/9] Mounting xml coverage report..."
mv ./coverage.xml ./docker

echo "[7/9] Generating html coverage report..."
coverage html -i --skip-empty -d coverage_html

echo "[8/9] Mounting html coverage report..."
mkdir ./docker/coverage_html
mv ./coverage_html/* ./docker/coverage_html

echo "[9/9] Exiting with code $exitcode"
exit $exitcode