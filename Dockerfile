FROM node:14-alpine AS frontend

# Make build & post-install scripts behave as if we were in a CI environment (e.g. for logging verbosity purposes).
ARG CI=true

# Install front-end dependencies.
COPY package.json package-lock.json .babelrc.js webpack.config.js ./
RUN npm ci --no-optional --no-audit --progress=false

# Compile static files
COPY ./campaignresourcecentre/static_src/ ./campaignresourcecentre/static_src/
RUN npm run build:prod


# We use Debian images because they are considered more stable than the alpine
# ones becase they use a different C compiler. Debian images also come with
# all useful packages required for image manipulation out of the box. They
# however weight a lot, approx. up to 1.5GiB per built image.
FROM python:3.12-alpine AS backend
RUN apk update
RUN apk add curl postgresql-dev bash py3-pip
RUN pip3 install --upgrade pip setuptools

ARG POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.8.5

RUN adduser campaignresourcecentre -D && mkdir /app && chown campaignresourcecentre /app

WORKDIR /app

# Set default environment variables. They are used at build time and runtime.
# If you specify your own environment variables on Heroku or Dokku, they will
# override the ones set here. The ones below serve as sane defaults only.
#  * PATH - Make sure that Poetry is on the PATH
#  * PYTHONUNBUFFERED - This is useful so Python does not hold any messages
#    from being output.
#    https://docs.python.org/3.8/using/cmdline.html#envvar-PYTHONUNBUFFERED
#    https://docs.python.org/3.8/using/cmdline.html#cmdoption-u
#  * PYTHONPATH - enables use of django-admin command.
#  * DJANGO_SETTINGS_MODULE - default settings used in the container.
#  * PORT - default port used. Please match with EXPOSE so it works on Dokku.
#    Heroku will ignore EXPOSE and only set PORT variable. PORT variable is
#    read/used by Gunicorn.
#  * WEB_CONCURRENCY - number of workers used by Gunicorn. The variable is
#    read by Gunicorn. Taken from pipeline variable
#  * GUNICORN_CMD_ARGS - additional arguments to be passed to Gunicorn. This
#    variable is read by Gunicorn. Taken from pipeline variable
ENV PATH=$PATH:${POETRY_HOME}/bin \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=campaignresourcecentre.settings.production \
    PORT=8000

ARG BUILD_ENV

# Make $BUILD_ENV available at runtime
ENV BUILD_ENV=${BUILD_ENV}

# Port exposed by this container. Should default to the port used by your WSGI
# server (Gunicorn). This is read by Dokku only. Heroku will ignore this.
EXPOSE 8000

# Install poetry using the installer (keeps Poetry's dependencies isolated from the app's)
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false

# Install your app's Python requirements

COPY --chown=campaignresourcecentre ./poetry ./poetry

RUN cd ./poetry && if [ "$BUILD_ENV" = "dev" ]; then poetry install --extras gunicorn; else poetry install --no-dev --extras gunicorn; fi; cd ../

COPY --chown=campaignresourcecentre --from=frontend ./campaignresourcecentre/static_compiled ./campaignresourcecentre/static_compiled

# Copy application code.
COPY --chown=campaignresourcecentre ./campaignresourcecentre ./campaignresourcecentre
COPY --chown=campaignresourcecentre ./manage.py  ./docker-entrypoint.sh ./initializer-entrypoint.sh  gunicorn-conf.py ./

# Collect static. This command will move static files from application
# directories and "static_compiled" folder to the main static directory that
# will be served by the WSGI server.
# Note the static folder is owned by the current user i.e. root and so collectstatic
# cannot be run within fab.sh (unlike migrate or createsuperuser)
RUN SECRET_KEY=none python3 manage.py collectstatic --noinput --clear

# Load shortcuts
COPY ./docker/bashrc.sh /home/campaignresourcecentre/.bashrc

# Don't use the root user as it's an anti-pattern and Heroku does not run
# containers as root either.
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
USER campaignresourcecentre

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD gunicorn campaignresourcecentre.wsgi:application
