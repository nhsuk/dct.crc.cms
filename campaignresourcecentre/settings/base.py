"""
Django settings for campaignresourcecentre project.
"""
import os
import sys

env = os.environ.copy()


def getenv_bool(name: str, default: bool = False) -> bool:
    # A blank string is defined, but we want it to be defaulted
    text = env.get(name) or str(default)
    return text.lower() in ("yes", "y", "true", "1", "t")


def getenv_int(name: str, default: int = 0) -> int:
    # A blank string is defined, but we want it to be defaulted
    text = env.get(name) or str(default)
    return int(text)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Derive DEBUG from environment
# https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = getenv_bool("DEBUG", False)


# Secret key is important to be kept secret. Never share it with anyone. Please
# always set it in the environment variable and never check into the
# repository.
# In its default template Django generates a 50-characters long string using
# the following function:
# https://github.com/django/django/blob/fd8a7a5313f5e223212085b2e470e43c0047e066/django/core/management/utils.py#L76-L81
# https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
if "SECRET_KEY" in env:
    SECRET_KEY = env["SECRET_KEY"]


# Define what hosts an app can be accessed by.
# It will return HTTP 400 Bad Request error if your host is not set using this
# setting.
# https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
if "ALLOWED_HOSTS" in env:
    ALLOWED_HOSTS = env["ALLOWED_HOSTS"].split(",")


# Application definition

INSTALLED_APPS = [
    "campaignresourcecentre.azurestore.apps.AzurestoreConfig",
    "campaignresourcecentre.apps.CRCV3Config",
    "campaignresourcecentre.baskets",
    "campaignresourcecentre.campaigns",
    "campaignresourcecentre.core",
    "campaignresourcecentre.documents",
    "campaignresourcecentre.forms",
    "campaignresourcecentre.guides",
    "campaignresourcecentre.home",
    "campaignresourcecentre.images",
    "campaignresourcecentre.navigation",
    "campaignresourcecentre.orders.apps.OrdersConfig",
    "campaignresourcecentre.page_lifecycle",
    "campaignresourcecentre.paragon",
    "campaignresourcecentre.paragon_users",
    "campaignresourcecentre.resources",
    "campaignresourcecentre.search",
    "campaignresourcecentre.standardpages",
    "campaignresourcecentre.users",
    "campaignresourcecentre.utils",
    "wagtailnhsukfrontend",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
    "captcha",
    "wagtailcaptcha",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # Must be before `django.contrib.staticfiles`
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "pattern_library",
    "wagtailaccessibility",
    "wagtailreacttaxonomy",
    "wagtail_2fa",
    "django_otp",
    "django_otp.plugins.otp_totp",
]


# Middleware classes
# https://docs.djangoproject.com/en/stable/ref/settings/#middleware
# https://docs.djangoproject.com/en/stable/topics/http/middleware/
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise middleware is used to server static files (CSS, JS, etc.).
    # According to the official documentation it should be listed underneath
    # SecurityMiddleware.
    # http://whitenoise.evans.io/en/stable/#quickstart-for-django-apps
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "campaignresourcecentre.core.middleware.crccachingmiddleware.CRCUpdateCacheMiddleware",
    # above line replaces django.middleware.cache.UpdateCacheMiddleware,
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "wagtail_2fa.middleware.VerifyUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "campaignresourcecentre.core.middleware.crccachingmiddleware.CRCFetchFromCacheMiddleware",
    # above line replaces django.middleware.cache.FetchFromCacheMiddleware,
]

ROOT_URLCONF = "campaignresourcecentre.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                # This is a custom context processor that lets us add custom
                # global variables to all the templates.
                "campaignresourcecentre.utils.context_processors.global_vars",
            ],
            "builtins": ["pattern_library.loader_tags"],
        },
    }
]

WSGI_APPLICATION = "campaignresourcecentre.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
DATABASES = {
    "default": {
        "NAME": env.get("DB_NAME", "postgres"),
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.get("DB_HOST", "db"),
        "PORT": getenv_int("DB_PORT", 5432),
        "USER": env.get("DB_USER", "postgres"),
        "PASSWORD": env.get("DB_PASS", "postgres"),
        "CONN_MAX_AGE": getenv_int("DB_CONN_MAX_AGE", 60)
        # Beware do not use DB_CONN_MAX_AGE > 0 with runserver (djrun) as
        # it will exceed permitted database connections under moderate to heavy load
    }
}


# Server-side cache settings. Do not confuse with front-end cache.
# https://docs.djangoproject.com/en/stable/topics/cache/
# If the server has a Redis instance exposed via a URL string in the REDIS_URL
# environment variable, prefer that. Otherwise use the database backend. We
# usually use Redis in production and database backend on staging and dev. In
# order to use database cache backend you need to run
# "django-admin createcachetable" to create a table for the cache.
#
# On platforms like Heroku which automatically set the REDIS_URL environment
# variable, the value is usually set to not use TLS.
# Setting the `REDIS_FORCE_TLS` environment variable to True will replace redis://
# in the connection string with rediss://, enabling connectionst to redis over TLS.
#
# Do not use the same Redis instance for other things like Celery!
if "REDIS_URL" in env:
    REDIS_FORCE_TLS = env.get("REDIS_FORCE_TLS", "false").lower() == "true"
    REDIS_URL = env["REDIS_URL"]
    if REDIS_FORCE_TLS:
        REDIS_URL = REDIS_URL.replace("redis://", "rediss://")

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
            "KEY_PREFIX": "default",
        },
        "renditions": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
            "KEY_PREFIX": "renditions",
            "TIMEOUT": 600,
        },
    }
else:
    # If using DatabaseCache, cache table must be created
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "database_cache",
        }
    }

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Values for the Django cache middleware - note we have subclassed it
CACHE_MIDDLEWARE_ALIAS = "default"
CCACHE_MIDDLEWARE_SECONDS = 30 * 60
CACHE_MIDDLEWARE_PREFIX = "page"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Search
# https://docs.wagtail.io/en/latest/topics/search/backends.html

WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "campaignresourcecentre.search.azure"}}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

# We serve static files with Whitenoise (set in MIDDLEWARE). It also comes with
# a custom backend for the static files storage. It makes files cacheable
# (cache-control headers) for a long time and adds hashes to the file names,
# e.g. main.css -> main.1jasdiu12.css.
# The static files with this backend are generated when you run
# "django-admin collectstatic".
# http://whitenoise.evans.io/en/stable/#quickstart-for-django-apps
# https://docs.djangoproject.com/en/stable/ref/settings/#staticfiles-storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Place static files that need a specific URL (such as robots.txt and favicon.ico) in the "public" folder
WHITENOISE_ROOT = os.path.join(BASE_DIR, "public")


# This is where Django will look for static files outside the directories of
# applications which are used by default.
# https://docs.djangoproject.com/en/stable/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [
    # "static_compiled" is a folder used by the front-end tooling
    # to output compiled static assets.
    os.path.join(PROJECT_DIR, "static_compiled")
]

# This is where Django will put files collected from application directories
# and custom direcotires set in "STATICFILES_DIRS" when
# using "django-admin collectstatic" command.
# https://docs.djangoproject.com/en/stable/ref/settings/#static-root
STATIC_ROOT = env.get("STATIC_DIR", os.path.join(BASE_DIR, "static"))


# This is the URL that will be used when serving static files, e.g.
# https://llamasavers.com/static/
# https://docs.djangoproject.com/en/stable/ref/settings/#static-url
STATIC_URL = env.get("STATIC_URL", "/crc-static/")


# Where in the filesystem the media (user uploaded) content is stored.
# MEDIA_ROOT is not used when a non-file storage backend such as Azure is set up.
# Probably only relevant to the local development.
# https://docs.djangoproject.com/en/stable/ref/settings/#media-root
MEDIA_ROOT = env.get("MEDIA_DIR", os.path.join(BASE_DIR, "media"))


# The URL path that media files will be accessible at. This setting won't be
# used if S3 backend is set up.
# Probably only relevant to the local development.
# https://docs.djangoproject.com/en/stable/ref/settings/#media-url
MEDIA_URL = env.get("MEDIA_URL", "/media/")

# Azure storage configuration
# https://docs.djangoproject.com/en/stable/ref/settings/#default-file-storage
AZURE_CONTAINER = env.get("AZURE_CONTAINER", "")
if AZURE_CONTAINER and AZURE_CONTAINER.lower() != "none":
    # Add django-storages to the installed apps
    INSTALLED_APPS = INSTALLED_APPS + ["storages"]

    DEFAULT_FILE_STORAGE = (
        "campaignresourcecentre.custom_storages.custom_azure.AzureMediaStorage"
    )
    SEARCH_STORAGE_CLASS = (
        "campaignresourcecentre.custom_storages.custom_azure.AzureSearchStorage"
    )
    AZURE_ACCOUNT_NAME = env["AZURE_ACCOUNT_NAME"]
    AZURE_ACCOUNT_KEY = env["AZURE_ACCOUNT_KEY"]
    AZURE_SEARCH_CONTAINER = env["AZURE_SEARCH_CONTAINER"]
    AZURE_SEARCH_ACCESS_KEY = env["AZURE_SEARCH_ACCESS_KEY"]
    AZURE_SEARCH_STORAGE_ACCOUNT_NAME = env["AZURE_SEARCH_STORAGE_ACCOUNT_NAME"]
    # AZURE_SEARCH_UPDATE determines whether search resources are indexed as updates are made
    AZURE_SEARCH_UPDATE = getenv_bool("AZURE_SEARCH_UPDATE", True)
    AZURE_CUSTOM_DOMAIN = env["AZURE_CUSTOM_DOMAIN"]
    AZURE_URL_EXPIRATION_SECS = 1860
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    SEARCH_STORAGE_CLASS = "django.core.files.storage.FileSystemStorage"
    AZURE_SEARCH_UPDATE = False

# Logging
# This logging is configured to be used with Sentry and console logs. Console
# logs are widely used by platforms offering Docker deployments, e.g. Heroku.
# We use Sentry to only send error logs so we're notified about errors that are
# not Python exceptions.
# We do not use default mail or file handlers because they are of no use for
# us.
# https://docs.djangoproject.com/en/stable/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Send logs with at least INFO level to the console.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "campaignresourcecentre": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "wagtail": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}


# Email settings
# We use GOV.UK Notify to send emails.
# https://www.notifications.service.gov.uk/services/5516fd78-9e45-450a-8d50-87139dfc2d30
# https://docs.djangoproject.com/en/2.1/topics/email/

EMAIL_BACKEND = "django_gov_notify.backends.NotifyEmailBackend"


# Sentry configuration.
# See instructions on the intranet:
# https://intranet.torchbox.com/delivering-projects/tech/starting-new-project/#sentry
is_in_shell = len(sys.argv) > 1 and sys.argv[1] in ["shell", "shell_plus"]

if "SENTRY_DSN" in env and not is_in_shell:

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.utils import get_default_release

    sentry_kwargs = {"dsn": env["SENTRY_DSN"], "integrations": [DjangoIntegration()]}

    # There's a chooser to toggle between environments at the top right corner on sentry.io
    # Values are typically 'staging' or 'production' but can be set to anything else if needed.
    # dokku config:set gosh SENTRY_ENVIRONMENT=staging
    # heroku config:set SENTRY_ENVIRONMENT=production
    if "SENTRY_ENVIRONMENT" in env:
        sentry_kwargs.update({"environment": env["SENTRY_ENVIRONMENT"]})

    release = get_default_release()
    if release is None:
        try:
            # But if it's not, we assume that the commit hash is available in
            # the GIT_REV environment variable. It's a default environment
            # variable used on Dokku:
            # http://dokku.viewdocs.io/dokku/deployment/methods/git/#configuring-the-git_rev-environment-variable
            release = env["GIT_REV"]
        except KeyError:
            try:
                # Assume this is a Heroku-hosted app with the "runtime-dyno-metadata" lab enabled
                release = env["HEROKU_RELEASE_VERSION"]
            except KeyError:
                # If there's no commit hash, we do not set a specific release.
                release = None

    sentry_kwargs.update({"release": release})
    sentry_sdk.init(**sentry_kwargs)


# Front-end cache
# This configuration is used to allow purging pages from cache when they are
# published.
# These settings are usually used only on the production sites.
# This is a configuration of the CDN/front-end cache that is used to cache the
# production websites.
# https://docs.wagtail.io/en/latest/reference/contrib/frontendcache.html
# The backend can be configured to use an account-wide API key, or an API token with
# restricted access.

if (
    "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env
    or "FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN" in env
):
    INSTALLED_APPS.append("wagtail.contrib.frontend_cache")
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "ZONEID": env["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
        }
    }

    if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env:
        # To use an account-wide API key, set the following environment variables:
        #  * FRONTEND_CACHE_CLOUDFLARE_TOKEN
        #  * FRONTEND_CACHE_CLOUDFLARE_EMAIL
        #  * FRONTEND_CACHE_CLOUDFLARE_ZONEID
        # These can be obtained from a sysadmin.
        WAGTAILFRONTENDCACHE["default"].update(
            {
                "EMAIL": env["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
                "TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
            }
        )

    else:
        # To use an API token with restricted access, set the following environment variables:
        #  * FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN
        #  * FRONTEND_CACHE_CLOUDFLARE_ZONEID
        WAGTAILFRONTENDCACHE["default"].update(
            {"BEARER_TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN"]}
        )


# Set s-max-age header that is used by reverse proxy/front end cache. See
# urls.py.
try:
    CACHE_CONTROL_S_MAXAGE = int(env.get("CACHE_CONTROL_S_MAXAGE", 600))
except ValueError:
    pass


# Give front-end cache 30 second to revalidate the cache to avoid hitting the
# backend. See urls.py.
CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
    env.get("CACHE_CONTROL_STALE_WHILE_REVALIDATE", 30)
)


# Required to get e.g. wagtail-sharing working on Heroku and probably many other platforms.
# https://docs.djangoproject.com/en/stable/ref/settings/#use-x-forwarded-port
USE_X_FORWARDED_PORT = env.get("USE_X_FORWARDED_PORT", "true").lower().strip() == "true"

# Security configuration
# This configuration is required to achieve good security rating.
# You can test it using https://securityheaders.com/
# https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security

# Enabling this doesn't have any benefits but will make it harder to make
# requests from javascript because the csrf cookie won't be easily accessible.
# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-httponly
# CSRF_COOKIE_HTTPONLY = True

# Force HTTPS redirect (enabled by default!)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect
if env.get("SECURE_SSL_REDIRECT", "true").strip().lower() == "true":
    SECURE_SSL_REDIRECT = True


# This will allow the cache to swallow the fact that the website is behind TLS
# and inform the Django using "X-Forwarded-Proto" HTTP header.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# This is a setting setting HSTS header. This will enforce the visitors to use
# HTTPS for an amount of time specified in the header. Please make sure you
# consult with sysadmin before setting this.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
if "SECURE_HSTS_SECONDS" in env:
    SECURE_HSTS_SECONDS = int(env["SECURE_HSTS_SECONDS"])


# https://docs.djangoproject.com/en/stable/ref/settings/#secure-browser-xss-filter
if env.get("SECURE_BROWSER_XSS_FILTER", "true").lower().strip() == "true":
    SECURE_BROWSER_XSS_FILTER = True


# https://docs.djangoproject.com/en/stable/ref/settings/#secure-content-type-nosniff
if env.get("SECURE_CONTENT_TYPE_NOSNIFF", "true").lower().strip() == "true":
    SECURE_CONTENT_TYPE_NOSNIFF = True


# Content Security policy settings
# http://django-csp.readthedocs.io/en/latest/configuration.html
if "CSP_DEFAULT_SRC" in env:
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")

    # The “special” source values of 'self', 'unsafe-inline', 'unsafe-eval', and 'none' must be quoted!
    # e.g.: CSP_DEFAULT_SRC = "'self'" Without quotes they will not work as intended.

    CSP_DEFAULT_SRC = env.get("CSP_DEFAULT_SRC").split(",")
    if "CSP_SCRIPT_SRC" in env:
        CSP_SCRIPT_SRC = env.get("CSP_SCRIPT_SRC").split(",")
    if "CSP_STYLE_SRC" in env:
        CSP_STYLE_SRC = env.get("CSP_STYLE_SRC").split(",")
    if "CSP_IMG_SRC" in env:
        CSP_IMG_SRC = env.get("CSP_IMG_SRC").split(",")
    if "CSP_CONNECT_SRC" in env:
        CSP_CONNECT_SRC = env.get("CSP_CONNECT_SRC").split(",")
    if "CSP_FONT_SRC" in env:
        CSP_FONT_SRC = env.get("CSP_FONT_SRC").split(",")
    if "CSP_BASE_URI" in env:
        CSP_BASE_URI = env.get("CSP_BASE_URI").split(",")
    if "CSP_OBJECT_SRC" in env:
        CSP_OBJECT_SRC = env.get("CSP_OBJECT_SRC").split(",")


# Referrer-policy header settings.
# https://django-referrer-policy.readthedocs.io/en/1.0/

REFERRER_POLICY = env.get(
    "SECURE_REFERRER_POLICY", "no-referrer-when-downgrade"
).strip()

# Recaptcha
# These settings are required for the captcha challange to work.
# https://github.com/springload/wagtail-django-recaptcha

if "RECAPTCHA_PUBLIC_KEY" in env and "RECAPTCHA_PRIVATE_KEY" in env:
    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = env["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY = env["RECAPTCHA_PRIVATE_KEY"]

# Django REST framework settings
# Change default settings that enable basic auth.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    )
}

AUTH_USER_MODEL = "users.User"

# Wagtail settings

# This name is displayed in the Wagtail admin.
WAGTAIL_SITE_NAME = "Campaign Resource Centre"


# This is used by Wagtail's email notifications for constructing absolute
# URLs. Please set to the domain that users will access the admin site.
if "PRIMARY_HOST" in env:
    BASE_URL = "https://{}".format(env["PRIMARY_HOST"])

# Custom image model
# https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html
WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

# Rich text settings to remove unneeded features
# We normally don't want editors to use the images
# in the rich text editor, for example.
# They should use the image stream block instead
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "h2",
                "h3",
                "h4",
                "ol",
                "ul",
                "link",
                "document-link",
            ]
        },
    }
}

# Custom document model
# https://docs.wagtail.io/en/stable/advanced_topics/documents/custom_document_model.html
WAGTAILDOCS_DOCUMENT_MODEL = "documents.CustomDocument"


PASSWORD_REQUIRED_TEMPLATE = "wagtail/password_required.html"


# Default size of the pagination used on the front-end.
DEFAULT_PER_PAGE = 20


# Google Tag Manager ID from env
GOOGLE_TAG_MANAGER_ID = env.get("GOOGLE_TAG_MANAGER_ID")


# Allows us to toggle search indexing via an environment variable.
SEO_NOINDEX = env.get("SEO_NOINDEX", "false").lower() == "true"

TESTING = "test" in sys.argv

# By default, Django uses a computationally difficult algorithm for passwords hashing.
# We don't need such a strong algorithm in tests, so use MD5
if TESTING:
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Paragon configuration

PARAGON_API_ENDPOINT = env.get("PARAGON_API_ENDPOINT")
PARAGON_API_KEY = env.get("PARAGON_API_KEY")
PARAGON_MOCK = getenv_bool("PARAGON_MOCK", False)

PARAGON_SIGN_KEY = env.get("PARAGON_SIGN_KEY")
PARAGON_SALT = env.get("PARAGON_SALT")
PARAGON_ENCRYPTION_KEY = env.get("PARAGON_ENCRYPTION_KEY")

# Notify service configuration

GOVUK_NOTIFY_API_KEY = env.get("NOTIFY_API_KEY")
GOVUK_NOTIFY_TEST_API_KEY = env.get("GOVUK_NOTIFY_TEST_API_KEY")

# Use the real GOV.UK Notify client by default
NOTIFY_DEBUG = getenv_bool("NOTIFY_DEBUG", False)

# Adobe tracking configuration

ADOBE_TRACKING_URL = env.get("ADOBE_TRACKING_URL")

# Silence system checks.

SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]


# How long after a page is reviewed that it should be reviewed again.
PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION = 12

# Only show the password reset form if there's a GOV.UK Notify API key set,
# otherwise there's no way to send the email.
WAGTAIL_PASSWORD_RESET_ENABLED = bool(GOVUK_NOTIFY_API_KEY)

# Azure search configuration

AZURE_SEARCH = {
    "PREFIX": env.get("AZURE_SEARCH_PREFIX"),
    "API_HOST": env.get("AZURE_SEARCH_API_HOST"),
    "API_VERSION": env.get("AZURE_SEARCH_API_VERSION"),
    "DELETE_API_HOST": env.get("AZURE_SEARCH_DELETE_API_HOST"),
    "DELETE_API_VERSION": env.get("AZURE_SEARCH_DELETE_API_VERSION"),
    "API_KEY": env.get("AZURE_SEARCH_API_KEY"),
    "FACETS": env.get("AZURE_SEARCH_FACETS"),
}

# session settings

# Enabled so that the user is logged out once the browser is closed.
# Can be overidden per session. See:
# https://docs.djangoproject.com/en/3.2/topics/http/sessions/#browser-length-sessions-vs-persistent-sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# renews session after every request
SESSION_SAVE_EVERY_REQUEST = True
# expires cookies after 30 mins
SESSION_COOKIE_AGE = 1800

CAMPAIGNS_FROM_AZ = getenv_bool("CAMPAIGNS_FROM_AZ", True)
# Events tracking
CAMPAIGNS_EVENT_API_ENDPOINT = env.get("CAMPAIGNS_EVENT_API_ENDPOINT")

COOKIE_CONSENT_CAMPAIGNS = env.get("COOKIE_CONSENT_CAMPAIGNS")

CAMPAIGN_HUB_PAGE_FILTERS = [
    "CANCER",
    "CHILDHOODHEALTH",
    "COVID",
    "DRINKING",
    "EARLYDIAG",
    "EATING",
    "FLU",
    "MATERNITY",
    "MENTALHEALTH",
    "NHS",
    "PHYSICALACTIVITY",
    "QUITTINGSMOKING",
]

PHE_PARTNERSHIPS_EMAIL = env.get("PHE_PARTNERSHIPS_EMAIL")

# forces users to use 2fa flow
WAGTAIL_2FA_REQUIRED = True
