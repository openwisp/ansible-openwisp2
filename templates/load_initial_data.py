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
Ca = load_model("pki", "Ca")
Vpn = load_model("config", "Vpn")

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
ssh_private_key = os.environ.get("PRIVATE_KEY", "")
ssh_pub_key = os.environ.get("PUBLIC_KEY", "")

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


# Create Ca
if len(Ca.objects.all()) == 0:
    ca_instance = Ca.objects.create(
        name="{{ inventory_hostname }} CA",
    )
    print("created {{ inventory_hostname }} Certificate Authority")
else:
    # If Ca already exists, get the first one
    ca_instance = Ca.objects.first()

# Create Vpn
if len(Vpn.objects.all()) == 0:
    vpn_instance = Vpn.objects.create(
        name="{{ inventory_hostname }}-vpn",
        host="{{ inventory_hostname }}",
        backend="openwisp_controller.vpn_backends.OpenVpn",
        ca=ca_instance,
        config={
            "openvpn": [{
                "server": "10.42.0.0 255.255.255.0",
                "name": "{{ inventory_hostname }}-vpn",
                "mode": "server",
                'proto': 'udp',
                "port": 1194,
                "dev_type": "tun",
                "dev": "tun0",
                "local": "",
                "comp_lzo": "adaptive",
                "auth": "SHA1",
                "data_ciphers": [
                    {
                        "cipher": "AES-256-GCM",
                        "optional": False
                    },
                    {
                        "cipher": "AES-128-GCM",
                        "optional": False
                    }
                ],
                "data_ciphers_fallback": "AES-256-GCM",
                "cipher": "AES-256-GCM",
                "engine": "",
                "ca": "ca.pem",
                "cert": "cert.pem",
                "key": "key.pem",
                "pkcs12": "",
                "tls_auth": "",
                "ns_cert_type": "",
                "mtu_disc": "no",
                "mtu_test": False,
                "fragment": 0,
                "mssfix": 1450,
                "keepalive": "",
                "persist_tun": False,
                "persist_key": False,
                "tun_ipv6": False,
                "up": "",
                "up_delay": 0,
                "down": "",
                "script_security": 1,
                "user": "",
                "group": "",
                "mute": 0,
                "status": "",
                "status_version": 1,
                "mute_replay_warnings": False,
                "secret": "",
                "reneg_sec": 3600,
                "tls_timeout": 2,
                "tls_cipher": "",
                "remote_cert_tls": "",
                "float": False,
                "auth_nocache": False,
                "fast_io": False,
                "log": "",
                "verb": 1,
                "topology": "subnet",
                "tls_server": True,
                "dh": "dh.pem",
                "crl_verify": "",
                "duplicate_cn": False,
                "client_to_client": False,
                "client_cert_not_required": False,
                "username_as_common_name": False,
                "auth_user_pass_verify": ""
            }],
            "files": [
                {
                    "path": "ca.pem",
                    "mode": "0644",
                    "contents": "{{ '{{ ca }}' }}"
                },
                {
                    "path": "cert.pem",
                    "mode": "0644",
                    "contents": "{{ '{{ cert }}' }}"
                },
                {
                    "path": "key.pem",
                    "mode": "0644",
                    "contents": "{{ '{{ key }}' }}"
                },
                {
                    "path": "dh.pem",
                    "mode": "0644",
                    "contents": "{{ '{{ dh }}' }}"
                }
            ]
        }
    )
    print(f"created {{ inventory_hostname }} Vpn Server")
    print(f"openwisp2_vpn_name = {vpn_instance.name}")
    print(f"openwisp2_vpn_id   = {vpn_instance.id}")