#!/bin/bash
set -e

# Default is to run the Django App
if [[ $# -eq 0 ]]; then

  #Run Gunicorn
  echo Executing gunicorn with defaults after ${GUNICORN_CMD_ARGS}
  exec gunicorn campaignresourcecentre.wsgi:application \
      --name campaignresourcecentre \
      --bind 0.0.0.0:8000 \
      --log-level=info \
      --log-file=- \
      --access-logfile=- \
      --error-logfile=- \

fi

# EXECUTE DOCKER COMMAND NOW
echo Executing $@
exec "$@"
