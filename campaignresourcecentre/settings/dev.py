from .base import *  # noqa

# Simplify the cache backend in development
if DEBUG:
    if "REDIS_URL" in env:
        REDIS_FORCE_TLS = env.get("REDIS_FORCE_TLS", "false").lower() == "true"
        REDIS_URL = env["REDIS_URL"]
        if REDIS_FORCE_TLS:
            REDIS_URL = REDIS_URL.replace("redis://", "rediss://")

        CACHES = {
            "default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": REDIS_URL}
        }
    else:
        CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# This key to be used locally only.
SECRET_KEY = "foo"


# Allow all the hosts locally only.
ALLOWED_HOSTS = ["*"]


# Allow requests from the local IPs to see more debug information.
# Configure some later, but only in debug mode
INTERNAL_IPS = []


# This is only to test Wagtail emails.
BASE_URL = "http://localhost:8000"


# Display sent emails in the console while developing locally.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Disable password validators when developing locally.
AUTH_PASSWORD_VALIDATORS = []


# Enable Wagtail's style guide in Wagtail's settings menu.
# http://docs.wagtail.io/en/stable/contributing/styleguide.html
#INSTALLED_APPS += ["wagtail.contrib.styleguide"]  # noqa


# Adds django-extensions into installed apps
INSTALLED_APPS += ["django_extensions"]  # noqa


# Disable forcing HTTPS locally since development server supports HTTP only.
SECURE_SSL_REDIRECT = False

# Adds Django Debug Toolbar, if preset and requested
# (slows system right down, so for use as required)
USING_DEBUG_TOOLBAR = False
if USING_DEBUG_TOOLBAR:
    try:
        import debug_toolbar  # noqa

        INSTALLED_APPS.append("debug_toolbar")  # noqa
        MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa
        import socket
        INTERNAL_IPS += ["127.0.0.1", "10.0.2.2"]
        # Add more IPs for running in Docker container
        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [ip[: ip.rfind(".")] + ".1" for ip in ips]
    except ImportError:
        pass

# Import settings from local.py file if it exists. Please use it to keep
# settings that are not meant to be checked into Git and never check it in.
try:
    from .local import *  # noqa
except ImportError:
    pass
