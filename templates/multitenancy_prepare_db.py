#!/usr/bin/env python
"""
Prepares DB for loaddata command (must perform some cleanup first)
"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwisp2.settings")
django.setup()

from django.contrib.auth.models import ContentType
from django.contrib.auth.models import Permission
from openwisp_users.models import Organization
from openwisp_controller.config.models import OrganizationConfigSettings

# flush automatically created content types and permissions
ContentType.objects.all().delete()
Permission.objects.all().delete()

# create the default organization
org = Organization.objects.create(id='{{ openwisp2_default_organization_id }}',
                                  name='default',
                                  slug='default')
OrganizationConfigSettings.objects.create(organization=org,
                                          registration_enabled=True,
                                          shared_secret='{{ openwisp2_shared_secret|default("<CHANGE-ME>") }}')
