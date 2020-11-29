import os
import sys
from celery.schedules import crontab
from datetime import timedelta

TESTING = 'test' in sys.argv

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
    # all-auth
    'django.contrib.sites',
    # overrides allauth templates
    # must precede allauth
    'openwisp_users.accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',
    # openwisp2 modules
    'openwisp_users',
    'openwisp_controller.pki',
    'openwisp_controller.config',
    'openwisp_controller.geo',
    'openwisp_controller.connection',
{% if openwisp2_monitoring %}
    'openwisp_monitoring.monitoring',
    'openwisp_monitoring.device',
    'openwisp_monitoring.check',
    'nested_admin',
{% endif %}
    'openwisp_notifications',
    'flat_json_widget',
{% if openwisp2_network_topology %}
    'openwisp_network_topology',
{% endif %}
{% if openwisp2_firmware_upgrader %}
    'openwisp_firmware_upgrader',
{% endif %}
    # openwisp2 admin theme
    # (must be loaded here)
    'openwisp_utils.admin_theme',
    # admin
    'django.contrib.admin',
    'django.forms',
    # other dependencies
    'sortedm2m',
    'reversion',
    'leaflet',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'django_filters',
{% if openwisp2_radius %}
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'openwisp_radius',
{% endif %}
{% if openwisp2_firmware_upgrader or openwisp2_radius %}
    'private_storage',
{% endif %}
    'drf_yasg',
    'channels',
    'pipeline',
{% for app in openwisp2_extra_django_apps %}
    '{{ app }}',
{% endfor %}
{% if openwisp2_sentry.get('dsn') %}
    'raven.contrib.django.raven_compat',
{% endif %}
]

EXTENDED_APPS = [
    'django_x509',
    'django_loci',
]

{% if openwisp2_firmware_upgrader or openwisp2_radius %}
PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'private')
{% endif %}

AUTH_USER_MODEL = 'openwisp_users.User'
SITE_ID = 1
LOGIN_REDIRECT_URL = 'admin:index'
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openwisp_utils.staticfiles.DependencyFinder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware'
]

{% if openwisp2_radius %}
OPENWISP_RADIUS_FREERADIUS_ALLOWED_HOSTS = {{ openwisp2_radius_allowed_hosts }}
REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'openwisp_radius.api.serializers.PasswordResetSerializer',
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'openwisp_radius.api.serializers.RegisterSerializer',
}
# SMS settings
OPENWISP_RADIUS_SMS_TOKEN_MAX_IP_DAILY = {{ openwisp2_radius_sms_token_max_ip_daily }}
SENDSMS_BACKEND = '{{ openwisp2_radius_sms_backend }}'

{% endif %}

ROOT_URLCONF = 'openwisp2.urls'
OPENWISP_USERS_AUTH_API = {{ openwisp2_users_auth_api }}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('{{ openwisp2_redis_host }}', {{ openwisp2_redis_port }})]},
    },
}
ASGI_APPLICATION = 'openwisp2.routing.application'

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
                'openwisp_utils.admin_theme.context_processor.menu_items',
                'openwisp_utils.admin_theme.context_processor.admin_theme_settings',
                'openwisp_notifications.context_processors.notification_api_settings',
            ],
        },
    },
]

# Run celery in eager mode using in-memory broker while running tests
if not TESTING:
    CELERY_TASK_ACKS_LATE = {{ openwisp2_celery_task_acks_late }}
    CELERY_BROKER_URL = '{{ openwisp2_celery_broker_url }}'
else:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = 'memory://'

# Workaround for stalled migrate command
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': {{ openwisp2_celery_broker_max_tries }},
}

CELERY_BEAT_SCHEDULE = {
    'delete_old_notifications': {
        'task': 'openwisp_notifications.tasks.delete_old_notifications',
        'schedule': crontab(**{ {{ cron_delete_old_notifications }} }),
        'args': ({{ openwisp2_notifications_delete_old_notifications }},),
    },
{% if openwisp2_monitoring %}

    'run_checks': {
        'task': 'openwisp_monitoring.check.tasks.run_checks',
        'schedule': timedelta(minutes=5),
    },
{% endif %}
{% if openwisp2_radius %}

    'deactivate_expired_users': {
        'task': 'openwisp_radius.tasks.deactivate_expired_users',
        'schedule': crontab(**{ {{ cron_deactivate_expired_users }} }),
        'args': None,
        'relative': True,
    },
    'delete_old_users': {
        'task': 'openwisp_radius.tasks.delete_old_users',
        'schedule': crontab(**{ {{ cron_delete_old_users }} }),
        'args': [{{ openwisp2_radius_delete_old_users }}],
        'relative': True,
    },
    'cleanup_stale_radacct': {
        'task': 'openwisp_radius.tasks.cleanup_stale_radacct',
        'schedule': crontab(**{ {{ cron_cleanup_stale_radacct }} }),
        'args': [{{ openwisp2_radius_cleanup_stale_radacct }}],
        'relative': True,
    },
    'delete_old_postauth': {
        'task': 'openwisp_radius.tasks.delete_old_postauth',
        'schedule': crontab(**{ {{ cron_delete_old_postauth }} }),
        'args': [{{ openwisp2_radius_delete_old_postauth }}],
        'relative': True,
    },

{% if openwisp2_radius_delete_old_radacct %}
    'delete_old_radacct': {
        'task': 'openwisp_radius.tasks.delete_old_radacct',
        'schedule': crontab(**{ {{ cron_delete_old_radacct }} }),
        'args': [{{ openwisp2_radius_delete_old_radacct }}],
        'relative': True,
    },
{% endif %}
{% endif %}
}

{% if openwisp2_celery_task_routes_defaults %}
CELERY_TASK_ROUTES = {
{% if openwisp2_celery_network %}
    # network operations, executed in the "network" queue
    'openwisp_controller.connection.tasks.*': {'queue': 'network'},
{% endif %}
{% if openwisp2_monitoring and openwisp2_celery_monitoring %}
    # monitoring checks are executed in a dedicated "monitoring" queue
    'openwisp_monitoring.check.tasks.perform_check': {'queue': 'monitoring'},
{% endif %}
{% if openwisp2_firmware_upgrader and openwisp2_celery_firmware_upgrader %}
    # firmware upgrade operations, executed in the "firmware_upgrader" queue
    'openwisp_firmware_upgrader.tasks.upgrade_firmware': {'queue': 'firmware_upgrader'},
    'openwisp_firmware_upgrader.tasks.batch_upgrade_operation': {'queue': 'firmware_upgrader'},
{% endif %}
    # all other tasks are routed to the default queue (named "celery")
}
{% endif %}

# FOR DJANGO REDIS

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '{{ openwisp2_redis_cache_url }}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

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

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
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
{% else %}
LEAFLET_CONFIG = {}
{% endif %}
# always disable RESET_VIEW button
LEAFLET_CONFIG['RESET_VIEW'] = False

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
            'format': '[%(levelname)s %(asctime)s] module: %(module)s, process: %(process)d, thread: %(thread)d\n%(message)s\n'
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
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/openwisp2.log'),
            'maxBytes': 15728640,
            'backupCount': 3,
            'formatter': 'verbose'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
{% if openwisp2_sentry.get('dsn') %}
        'sentry': {
            'level': 'ERROR',
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
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['main_log'],
            'propagate': False,
        }
    }
}

# HTML minification with django pipeline
PIPELINE = {'PIPELINE_ENABLED': True}
# static files minification and invalidation with django-compress-staticfiles
STATICFILES_STORAGE = 'openwisp2.storage.CompressStaticFilesStorage'
# GZIP compression is handled by nginx
BROTLI_STATIC_COMPRESSION = False
GZIP_STATIC_COMPRESSION = False

{% if openwisp2_sentry.get('dsn') %}
RAVEN_CONFIG = {{ openwisp2_sentry|to_nice_json }}
{% endif %}

{% if openwisp2_monitoring %}
TIMESERIES_DATABASE = {
    'BACKEND': '{{ openwisp2_timeseries_database.backend }}',
    'USER': '{{ openwisp2_timeseries_database.user }}',
    'PASSWORD': '{{ openwisp2_timeseries_database.password }}',
    'NAME': '{{ openwisp2_timeseries_database.name }}',
    'HOST': '{{ openwisp2_timeseries_database.host }}',
    'PORT': '{{ openwisp2_timeseries_database.port }}',
}

INSTALLED_APPS.append('djcelery_email')
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
{% endif %}

{% for setting, value in openwisp2_extra_django_settings.items() %}
{{ setting }} = {% if value is string %}'{{ value }}'{% else %}{{ value }}{% endif %}

{% endfor %}

{% for instruction in openwisp2_extra_django_settings_instructions %}
{{ instruction }}

{% endfor %}
