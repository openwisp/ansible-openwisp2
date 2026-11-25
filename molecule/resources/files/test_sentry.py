"""Verify the rendered Sentry configuration without sending network events."""

import logging
import os
import runpy
import sys
from pathlib import Path

import django
import sentry_sdk
from django.conf import settings
from django.http import HttpResponse
from django.test import Client, override_settings
from django.urls import path
from sentry_sdk.transport import Transport


def broken_view(request):
    raise RuntimeError("sentry-django-test")


def healthy_view(request):
    return HttpResponse("ok")


urlpatterns = [path("broken/", broken_view), path("healthy/", healthy_view)]


class MemoryTransport(Transport):
    def __init__(self):
        super().__init__()
        self.events = []

    def capture_envelope(self, envelope):
        for item in envelope.items:
            if item.headers.get("type") == "event":
                self.events.append(item.payload.json)


os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
# Load the generated settings before inspecting the initialized client.
settings.DEBUG
client = sentry_sdk.get_client()
enabled = sys.argv[2] == "enabled"
assert client.is_active() == enabled, "Unexpected Sentry activation state"
source = Path(sys.argv[1], "settings.py").read_text()
assert "raven" not in source and "RAVEN_CONFIG" not in source
uwsgi_config = Path(sys.argv[1], "uwsgi.ini").read_text()
assert ("py-call-uwsgi-fork-hooks=True" in uwsgi_config) == enabled

if enabled:
    assert {"django", "celery"}.issubset(client.integrations)
    assert client.options["send_default_pii"] is False
    assert client.options["traces_sample_rate"] is None
    assert client.options["environment"] == 'test "quoted" environment'
    assert client.options["sample_rate"] == 0.0
    transport = MemoryTransport()
    client.transport = transport
    client.options["sample_rate"] = 1.0
else:
    assert "sentry_sdk" not in source

django.setup()
celery_config = runpy.run_path(str(Path(sys.argv[1], "celery_config.py")))
app = celery_config["app"]
# Force worker settings to load, including the custom logging configuration.
app.conf.task_always_eager = True
app.log.setup_logging_subsystem()
assert ("config_loggers" in celery_config) == (sys.argv[3] == "true")

if enabled:
    with override_settings(
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[],
        ALLOWED_HOSTS=["testserver"],
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    ):
        browser = Client(raise_request_exception=False)
        assert browser.get("/healthy/").status_code == 200
        assert browser.get("/broken/").status_code == 500

    @app.task
    def broken_task():
        raise RuntimeError("sentry-celery-test")

    result = broken_task.apply()
    assert result.failed(), "The test task should fail"
    logging.getLogger("sentry-test").error("sentry-logging-test")
    sentry_sdk.flush()
    exceptions = [
        value["value"]
        for event in transport.events
        for value in event.get("exception", {}).get("values", [])
    ]
    assert "sentry-django-test" in exceptions, "Django error was not captured"
    assert "sentry-celery-test" in exceptions, "Celery error was not captured"
    assert any(
        event.get("logentry", {}).get("message") == "sentry-logging-test"
        for event in transport.events
    ), "Logging error was not captured"

print("Sentry configuration and error capture checks passed")
