from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openwisp2.settings')

app = Celery('openwisp2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if hasattr(settings, 'RAVEN_CONFIG'):
    from raven.contrib.celery import register_logger_signal, register_signal
    from raven.contrib.django.raven_compat.models import client
    register_logger_signal(client)
    register_signal(client, ignore_expected=True)
