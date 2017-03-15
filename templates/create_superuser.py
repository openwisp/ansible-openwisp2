#!/usr/bin/env python
"""
- Creates the admin user when openwisp2 is installed
- Additionally creates the default organization if no organization is present
- Modifies default Site object
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openwisp2.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
changed = False

if User.objects.filter(is_superuser=True).count() < 1:
    admin = User.objects.create_superuser(username='admin',
                                          password='admin',
                                          email='')
    print('superuser created')

if 'openwisp_users' in settings.INSTALLED_APPS:
    from openwisp_users.models import Organization

    if Organization.objects.count() < 1:
        options = dict(id='{{ openwisp2_default_organization_id }}',
                       name='default',
                       slug='default')
        org = Organization.objects.create(**options)

        if 'openwisp_controller.config' in settings.INSTALLED_APPS:
            from openwisp_controller.config.models import OrganizationConfigSettings

            OrganizationConfigSettings.objects.create(organization=org,
                                                      registration_enabled=True)
        print('default organization created')

if 'django.contrib.sites' in settings.INSTALLED_APPS:
    from django.contrib.sites.models import Site
    site = Site.objects.first()
    if site and 'example.com' in [site.name, site.domain]:
        site.name = '{{ ansible_fqdn }}'
        site.domain = '{{ inventory_hostname }}'
        site.save()
        print('default site updated')
