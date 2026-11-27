import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwisp2.settings")

app = Celery("openwisp2")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

{% if openwisp2_django_celery_logging %}
from logging.config import dictConfig

from celery.signals import setup_logging


@setup_logging.connect
def config_loggers(*args, **kwargs):
    dictConfig(settings.LOGGING)


{% endif %}
