#!/usr/bin/env python
"""
- Creates the admin user when openwisp2 is installed
- Additionally creates the default organization if no organization is present
- Modifies default Site object
- Adds a default access credential and updates or creates default
  template to use the same
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwisp2.settings")
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from swapper import load_model

Credentials = load_model("connection", "Credentials")
Template = load_model("config", "Template")
User = get_user_model()
changed = False

if User.objects.filter(is_superuser=True).count() < 1:
    admin = User.objects.create_superuser(username="admin", password="admin", email="")
    print("superuser created")

if "django.contrib.sites" in settings.INSTALLED_APPS:
    from django.contrib.sites.models import Site

    site = Site.objects.first()
    if site and "example.com" in [site.name, site.domain]:
        site.name = "{{ inventory_hostname }}"
        site.domain = "{{ inventory_hostname }}"
        site.save()
        print("default site updated")

# Get SSH key pair
ssh_private_key = os.environ.get("PRIVATE_KEY")
ssh_pub_key = os.environ.get("PUBLIC_KEY")

# Create a default credentials object
if ssh_private_key and Credentials.objects.count() == 0:
    Credentials.objects.create(
        connector="openwisp_controller.connection.connectors.ssh.Ssh",
        name="OpenWISP Default",
        auto_add=True,
        params={"username": "root", "key": ssh_private_key},
    )
    print("Credentials object created")

# Update or create default template to add default credentials
queryset = Template.objects.filter(
    default=True, config__contains="/etc/dropbear/authorized_keys"
)
if ssh_pub_key and queryset.count() == 0:
    Template.objects.create(
        name="SSH Keys",
        default=True,
        backend="netjsonconfig.OpenWrt",
        config={
            "files": [
                {
                    "path": "/etc/dropbear/authorized_keys",
                    "mode": "0644",
                    "contents": ssh_pub_key,
                },
            ]
        },
    )
    print("created Default Credentials Template")
else:
    for template_obj in queryset.iterator():
        for config_file in template_obj.config["files"]:
            if (
                config_file["path"] == "/etc/dropbear/authorized_keys"
                and ssh_pub_key not in config_file["contents"]
            ):
                config_file["contents"] += "\n" + ssh_pub_key
                template_obj.save()
                print(f"changed {template_obj.name} to add default SSH credential")
