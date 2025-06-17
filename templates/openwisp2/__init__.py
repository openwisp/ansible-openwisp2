from .celery import app as celery_app
from .version import __openwisp_installation_method__, __openwisp_version__

__all__ = ["celery_app", "__openwisp_version__", "__openwisp_installation_method__"]
