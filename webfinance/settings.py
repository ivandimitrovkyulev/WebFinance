"""
Django settings for webfinance project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import io
import logging
import environ
from pathlib import Path
from urllib.parse import urlparse

from google.auth import default as gcp_auth_default
from google.cloud import secretmanager
from google.cloud.logging import Client


# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables, first check for local .env file then for Google's Secrets Manager Service
env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env(DEBUG=(bool, False))

if os.path.isfile(env_file):
    env.read_env(env_file)
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Get Secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("Neither .env or GOOGLE_CLOUD_PROJECT detected. Secrets not loaded!")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# SECURITY WARNING: It's recommended that you use this when running in production. The URL will be known once
# you first deploy to App Engine. This code takes the URL and converts it to both these settings formats.
APPENGINE_URL = env.list("APPENGINE_URL", default=None)
if APPENGINE_URL:
    ALLOWED_HOSTS = []
    CSRF_TRUSTED_ORIGINS = []
    SECURE_SSL_REDIRECT = True

    for url in APPENGINE_URL:
        # Ensure a scheme is present in the URL before it's processed.
        if not urlparse(url).scheme:
            url = f"https://{url}"

        ALLOWED_HOSTS.append(urlparse(url).netloc)
        CSRF_TRUSTED_ORIGINS.append(APPENGINE_URL)
else:
    ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'accounts.apps.AccountsConfig',
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'webfinance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"webfinance/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webfinance.wsgi.application'

# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': env.db(),  # Uses info from DATABASE_URL variable
}

# If flag has been set - configure proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = "static"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR/"webfinance/static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.UserAccount"

# Allauth variables
ACCOUNT_USER_DISPLAY = lambda user: user.email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
LOGIN_REDIRECT_URL = "/"

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = env('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


# Logging configurations. https://docs.djangoproject.com/en/dev/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s - %(levelname)s - %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S, %Z"
        }
    },
    'handlers': {},
    'loggers': {
        'app_log': {
            'handlers': [],
            'level': 'DEBUG',
        },
    }
}

if os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Only add this handler if running inside App Engine
    credentials, _ = gcp_auth_default()
    # Google CloudLoggingHandler handler
    google_client = Client(credentials=credentials, project=credentials.__dict__['_quota_project_id'])
    # Attach def cloud logging handler to the root logger
    google_client.setup_logging(log_level=logging.DEBUG)
else:
    # If run locally add a new RotatingFileHandler
    LOGGING['handlers']['local_log_file'] = {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': os.path.join(BASE_DIR, 'webfinance.log'),
        'maxBytes': 1024 * 1024 * 50,  # 50MB maximum size
        'backupCount': 1,
        'formatter': 'verbose',
    }
    LOGGING['loggers']['app_log']['handlers'].append('local_log_file')
