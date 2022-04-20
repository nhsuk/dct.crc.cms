# Note: This file is loaded on all environments, even production.
# Note: gunicorn requires at least two workers to avoid request blocking

alias dj="python manage.py"

if [ "$BUILD_ENV" = "dev" ]; then
    alias djrun="python manage.py runserver 0.0.0.0:8000"
    alias djgun="gunicorn campaignresourcecentre.wsgi:application --reload"
    alias djtest="python manage.py test --settings=campaignresourcecentre.settings.test"
fi
