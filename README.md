ansible-openwisp2
=================

[![Galaxy](http://img.shields.io/badge/galaxy-nemesisdesign.openwisp2-blue.svg?style=flat-square)](https://galaxy.ansible.com/nemesisdesign/openwisp2/)

Ansible role for the nascent openwisp2 controller.

Usable but not stable, will probably change a lot over time.

Usage
=====

Generate a `SECRET_KEY` for django (copy the output of the following
command):

    ./generate-django-secret-key

Add an entry to your `site.yml` like the following one:

```yaml
- hosts: yourhost
  roles:
  # you can add other roles here
    - openwisp2
  vars:
    # generate a secret key with ./generate-django-secret-key
    openwisp2_secret_key: changemeplease
    # change the openwisp2 shared secret to a value of your liking
    openwisp2_shared_secret: changemeplease
    # whether to use the stable release (true) or the development version (false)
    openwisp2_stable: true
    # by default python3.4 is used, if may need to set this to python2.7 for older systems
    openwisp2_python: python2.7
    # customize the app_path
    openwisp2_path: /opt/openwisp2
    # edit database settings only if you are not using sqlite
    openwisp2_database:
        engine: django.db.backends.postgresql
        name: openwisp2
        user: postgres
        password: ""
        host: ""
        port: ""
        options: {}
    # customize other django settings:
    openwisp2_language_code: en-gb
    openwisp2_time_zone: UTC
    # django-netjsonconfig context
    openwisp2_context: {}
    # additional allowed hosts
    openwisp2_allowed_hosts:
        - myadditionalhost.openwisp.org
    # specify path to a valid SSL certificate and key
    # (a self-signed SSL cert will be generated if omitted)
    openwisp2_ssl_cert: "/etc/nginx/ssl/server.crt"
    openwisp2_ssl_key: "/etc/nginx/ssl/server.key"
    # customize the self-signed SSL certificate info if needed
    openwisp2_ssl_country: "US"
    openwisp2_ssl_state: "California"
    openwisp2_ssl_locality: "San Francisco"
    openwisp2_ssl_organization: "IT dep."
    # the following setting controls which ip address range
    # is allowed to access the controller via unencrypted HTTP
    # (this feature is disabled by default)
    openwisp2_http_allowed_ip: "10.8.0.0/16"
    # additional apps to install with pip and put in settings.INSTALLED_APPS
    openwisp2_extra_django_apps:
        - django_extensions
    # spdy protocol in nginx is enabled by default
    openwisp2_nginx_spdy: true
    # enable sentry
    openwisp2_sentry:
        dsn: "https://7d2e3cd61acc32eca1fb2a390f7b55e1:bf82aab5ddn4422688e34a486c7426e3@getsentry.com:443/12345"
```

Run the playbook:

    ansible-playbook -i hosts site.yml -l yourhost

When the playbook is done running, if you got no errors you can login at::

    https://<host>/admin
    username: admin
    passowrd: admin

Change the password (and the username if you like) of the superuser as soon
as possible.

The superuser will be created only the first time the playbook is run.
