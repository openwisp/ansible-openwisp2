ansible-openwisp2
=================

[![Galaxy](http://img.shields.io/badge/galaxy-nemesisdesign.openwisp2-blue.svg?style=flat-square)](https://galaxy.ansible.com/nemesisdesign/openwisp2/)

Ansible role for the nascent openwisp2 controller.

Tested on **debian** and **ubuntu**.

Usage (tutorial)
================

If you don't know how to use ansible, don't panic, this procedure will
guide you towards a fully working basic openwisp2 installation.

If you already know how to use ansible, you can skip this tutorial.

Ansible is a configuration management tool that works by entering servers via SSH,
**so you need to install it and configure it on your local machine**.

Install ansible
---------------

Install ansible **on your local machine** if you haven't done already, there are various way in
which you can do this, but we prefer to use the official python
package manager, eg:

    sudo pip install ansible

If you don't have pip installed see [Installing pip](https://pip.pypa.io/en/stable/installing/)
on the pip documentation website.

[Installing ansible in other ways](http://docs.ansible.com/ansible/intro_installation.html#latest-release-via-yum)
is fine too, just make sure to install a version of the `2.0.x` series (which is the version with
which we have tested this playbook).

Install this role
-----------------

For the sake of simplicity, the easiest thing is to install this role
via `ansible-galaxy` (which was installed when installing ansible), therefore run:

    sudo ansible-galaxy install nemesisdesign.openwisp2

Choose a working directory
--------------------------

Choose a working directory where to put the configuration of openwisp2.

This will be useful when you will need to upgrade openwisp2.

Eg:

    mkdir ~/openwisp2-ansible-playbook
    cd ~/openwisp2-ansible-playbook

Putting this working directory under version control is also a very good idea.

Create inventory file
---------------------

The inventory file is where group of servers are defined. In our simple case we can
get away with defining just one group in which we will put just one server.

Create a new file `hosts` with the following contents:

    [openwisp2]
    openwisp2.mydomain.com

Substitute `openwisp2.mydomain.com` with your hostname (ip addresses are allowed as well).

Create playbook file
--------------------

Create a new playbook file `playbook.yml` with the following contents:

```yaml
- hosts: openwisp2
  sudo: "{{ sudo | default('yes') }}"
  roles:
    - nemesisdesign.openwisp2
  vars:
    openwisp2_shared_secret: <PLEASE_CHANGE_ME>
```

Substitute `<PLEASE_CHANGE_ME>` with a value of your liking, this value will be used for
`NETJSONCONFIG_SHARED_SECRET` setting, see the [relevant section in the README of django-netjsonconfig](https://github.com/openwisp/django-netjsonconfig#netjsonconfig-shared-secret)
for more information.

The line `sudo: "{{ sudo | default('yes') }}"` means ansible  will use the `sudo`
program to run each command. You may remove this line if you don't need it.

Run the playbook
----------------

Run the playbook with:

    ansible-playbook -i hosts playbook.yml -u <user> -k --ask-sudo-pass

Substitute `<user>` with your user.

The `--ask-sudo-pass` argument will need the `sshpass` program.

You can remove `-k` and `--ask-sudo-pass` if your public SSH key is installed on the server.

When the playbook is done running, if you got no errors you can login at:

    https://openwisp2.mydomain.com/admin
    username: admin
    passowrd: admin

Substitute `openwisp2.mydomain.com` with your hostname.

Change the password (and the username if you like) of the superuser as soon
as possible.

The superuser will be created only the first time the playbook is run.

Role variables
==============

This role has many variables values that can be changed to best suit
your needs.

Below are listed all the variables you can customize.

```yaml
- hosts: yourhost
  roles:
  # you can add other roles here
    - openwisp2
  vars:
    # generate a secret key with ./generate-django-secret-key
    # openwisp2_secret_key: changemeplease
    # change the openwisp2 shared secret to a value of your liking
    openwisp2_shared_secret: changemeplease
    # whether to use the stable release (true) or the development version (false)
    openwisp2_stable: true
    # set to false to use development version of netjsonconfig
    openwisp2_netjsonconfig_stable: true
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
