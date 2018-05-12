import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ openwisp2_secret_key }}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '{{ inventory_hostname }}',
{% for host in openwisp2_allowed_hosts %}
    '{{ host }}',
{% endfor %}
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # openwisp2 admin theme
    # (must be loaded here)
    'openwisp_utils.admin_theme',
    # all-auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',
    # openwisp2 modules
    'openwisp_users',
    'openwisp_controller.pki',
    'openwisp_controller.config',
    'openwisp_controller.geo',
{% if openwisp2_network_topology %}
    'openwisp_network_topology',
{% endif %}
    # admin
    'django.contrib.admin',
    'django.forms',
    # other dependencies
    'sortedm2m',
    'reversion',
    'leaflet',
    'rest_framework',
    'rest_framework_gis',
    'channels',
{% for app in openwisp2_extra_django_apps %}
    '{{ app }}',
{% endfor %}
{% if openwisp2_sentry.get('dsn') %}
    'raven.contrib.django.raven_compat',
{% endif %}
]

EXTENDED_APPS = [
    'django_netjsonconfig',
    'django_x509',
    'django_loci',
{% if openwisp2_network_topology %}
    'django_netjsongraph',
{% endif %}
]

AUTH_USER_MODEL = 'openwisp_users.User'
SITE_ID = '1'
LOGIN_REDIRECT_URL = 'admin:index'
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openwisp_utils.staticfiles.DependencyFinder',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE = MIDDLEWARE_CLASSES

ROOT_URLCONF = 'openwisp2.urls'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {'hosts': [('localhost', 6379)]},
        'ROUTING': 'openwisp_controller.geo.channels.routing.channel_routing',
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'openwisp_utils.loaders.DependencyLoader'
                ]),
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# FOR DJANGO REDIS

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "{{ openwisp2_redis_cache_url }}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'openwisp2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': '{{ openwisp2_database.engine }}',
        'NAME': '{{ openwisp2_database.name }}',
{% if openwisp2_database.user is defined and openwisp2_database.user%}
        'USER': '{{ openwisp2_database.user }}',
{% endif %}
{% if openwisp2_database.password is defined and openwisp2_database.password %}
        'PASSWORD': '{{ openwisp2_database.password }}',
{% endif %}
{% if openwisp2_database.host is defined and openwisp2_database.host %}
        'HOST': '{{ openwisp2_database.host }}',
{% endif %}
{% if openwisp2_database.port is defined and openwisp2_database.port %}
        'PORT': '{{ openwisp2_database.port }}',
{% endif %}
{% if openwisp2_database.options is defined and openwisp2_database.options %}
        'OPTIONS': {{ openwisp2_database.options|to_nice_json }}
{% endif %}
    }
}

{% if openwisp2_spatialite_path %}
SPATIALITE_LIBRARY_PATH = '{{ openwisp2_spatialite_path }}'
{% endif %}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = '{{ openwisp2_language_code }}'
TIME_ZONE = '{{ openwisp2_time_zone }}'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = '%s/static' % BASE_DIR
MEDIA_ROOT = '%s/media' % BASE_DIR
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

{% if openwisp2_context %}
NETJSONCONFIG_CONTEXT = {{ openwisp2_context|to_nice_json }}
{% endif %}

# django x509 settings
DJANGO_X509_DEFAULT_CERT_VALIDITY = {{ openwisp2_default_cert_validity }}
DJANGO_X509_DEFAULT_CA_VALIDITY = {{ openwisp2_default_ca_validity }}

{% if openwisp2_leaflet_config %}
LEAFLET_CONFIG = {{ openwisp2_leaflet_config|to_nice_json }}
{% endif %}

# Set default email
DEFAULT_FROM_EMAIL = '{{ openwisp2_default_from_email }}'
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
        'verbose': {
            'format': '\n\n[%(levelname)s %(asctime)s] module: %(module)s, process: %(process)d, thread: %(thread)d\n%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'main_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'log/error.log'),
            'maxBytes': 5242880.0,
            'backupCount': 3,
            'formatter': 'verbose'
        },
{% if openwisp2_sentry.get('dsn') %}
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['require_debug_false']
        },
{% endif %}
    },
    'root': {
        'level': 'INFO',
        'handlers': [
            'main_log',
            'console',
            'mail_admins',
{% if openwisp2_sentry.get('dsn') %}
            'sentry'
{% endif %}
        ]
    }
}

{% if openwisp2_sentry.get('dsn') %}
RAVEN_CONFIG = {{ openwisp2_sentry|to_nice_json }}
{% endif %}

{% for setting, value in openwisp2_extra_django_settings.items() %}
{{ setting }} = {% if value is string %}'{{ value }}'{% else %}{{ value }}{% endif %}

{% endfor %}

{% for instruction in openwisp2_extra_django_settings_instructions %}
{{ instruction }}

{% endfor %}
