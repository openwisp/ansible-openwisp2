#!/usr/bin/env python
# Creates the admin user when openwisp2 is installed
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openwisp2.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

if User.objects.filter(is_superuser=True).count() < 1:
    admin = User.objects.create_superuser(username='admin',
                                          password='admin',
                                          email='')
    print('superuser created')
print('superuser present')
