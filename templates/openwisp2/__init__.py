from .celery import app as celery_app

__all__ = ['celery_app']
__openwisp_version__ = '24.11.1'
__openwisp_installation_method__ = (
    '{{ openwisp2_installation_method | default("ansible-openwisp2") }}'
)
