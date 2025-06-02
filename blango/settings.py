from pathlib import Path
import os
from configurations import Configuration, values
import dj_database_url

class Dev(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = 'django-insecure-+sn%dpa!086+g+%44z9*^j^q-u4n!j(#wl)x9a%_1op@zz2+1-'
    DEBUG = values.BooleanValue(True)
    ALLOWED_HOSTS = values.ListValue(["localhost", "0.0.0.0", ".codio.io"])
    

    # Get CODIO_HOSTNAME with a fallback
    CODIO_HOSTNAME = os.environ.get('CODIO_HOSTNAME', 'localhost') # Example fallback

    X_FRAME_OPTIONS = 'ALLOW-FROM ' + CODIO_HOSTNAME + '-8000.codio.io'
    CSRF_TRUSTED_ORIGINS = ['https://' + CODIO_HOSTNAME + '-8000.codio.io']
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SAMESITE = 'None'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'blog',
        "crispy_forms",
        "crispy_bootstrap5"
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware', # Ensure this is enabled
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware', # Ensure this is enabled
    ]

    ROOT_URLCONF = 'blango.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
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

    WSGI_APPLICATION = 'blango.wsgi.application'

    DATABASES = {
      "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
      "alternative": dj_database_url.config(
          "ALTERNATIVE_DATABASE_URL",
          default=f"sqlite:///{BASE_DIR}/alternative_db.sqlite3",
      ),
    }

    AUTH_PASSWORD_VALIDATORS = [
        # ... your validators
    ]

    PASSWORD_HASHERS = [
      'django.contrib.auth.hashers.Argon2PasswordHasher',
      'django.contrib.auth.hashers.PBKDF2PasswordHasher',
      'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
      'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    ]

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = values.Value("UTC")
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    STATIC_URL = '/static/'
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "verbose",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "filters": ["require_debug_false"],
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }
    
  
  

class Prod(Dev):
  DEBUG = False
  # SECRET_KEY = values.SecretValue('023fb4c21c3d5b12f1d45f94536a8538bf7fc92e6c997a4590')