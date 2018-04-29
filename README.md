ansible-openwisp2
=================

[![Installing OpenWISP2](https://raw.githubusercontent.com/openwisp/ansible-openwisp2/master/docs/install-openwisp2.png)](https://www.youtube.com/watch?v=v_DUeFUGG8Q&index=1&list=PLPueLZei9c8_DEYgC5StOcR5bCAcQVfR8)

[![Build Status](https://travis-ci.org/openwisp/ansible-openwisp2.svg?branch=master)](https://travis-ci.org/openwisp/ansible-openwisp2)
[![Galaxy](http://img.shields.io/badge/galaxy-openwisp.openwisp2-blue.svg?style=flat-square)](https://galaxy.ansible.com/openwisp/openwisp2/)
[![Galaxy](https://img.shields.io/ansible/role/d/14542.svg?style=flat-square)](https://galaxy.ansible.com/openwisp/openwisp2/)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square)](https://gitter.im/openwisp/general)

Ansible role that installs the openwisp2 controller.

Tested on **debian**, **ubuntu**, **fedora**, **redhat** and **centos**.

**NOTE**: it is highly suggested to use this procedure on clean virtual machines or linux containers.

**Minimum ansible version supported**: 2.4.

Help OpenWISP
=============

Like OpenWISP? Find out how to help us!

- [Help us to grow our community](http://openwisp.io/docs/general/help-us.html)
- [How to contribute to OpenWISP](http://openwisp.io/docs/developer/contributing.html)

Architecture
============

If you are fond of **Python**, **Django** and **Unix**/**Linux** systems, you may find interesting
to know more about what happens under the hood in **OpenWISP 2**.

![openwisp2 modules diagram](https://raw.githubusercontent.com/openwisp/ansible-openwisp2/master/docs/openwisp2-modules-diagram.png)

For more information see also [Applying the Unix Philosophy to Django projects: a report from the real world](https://www.slideshare.net/FedericoCapoano/applying-the-unix-philosophy-to-django-projects-a-report-from-the-real-world).

Usage (tutorial)
================

If you don't know how to use ansible, don't panic, this procedure will
guide you towards a fully working basic openwisp2 installation.

If you already know how to use ansible, you can skip this tutorial.

First of all you need to understand two key concepts:

* for **"production server"** we mean a server (**not a laptop or a desktop computer!**) with public
  ipv4 / ipv6 which is used to host openwisp2
* for **"local machine"** we mean the host from which you launch ansible, eg: your own laptop

Ansible is a configuration management tool that works by entering production servers via SSH,
**so you need to install it and configure it on the machine where you launch the deployment** and
this machine must be able to SSH into the production server.

Ansible will be run on your local machine and from there it will connect to the production server
to install openwisp2.

**If you are trying to install OpenWISP2 on your laptop or desktop pc just for testing purposes**,
please read [Install OpenWISP2 for testing in a VirtualBox VM](#install-openwisp2-for-testing-in-a-virtualbox-vm).

Install ansible
---------------

Install ansible (version 2.4 or higher) **on your local machine** (not the production server!) if
you haven't done already.

To **install ansible** we suggest you follow the official [ansible installation guide](http://docs.ansible.com/ansible/latest/intro_installation.html).

After having installed ansible, **you need to install git** (example for linux debian/ubuntu systems):

    sudo apt-get install git

Install this role
-----------------

For the sake of simplicity, the easiest thing is to install this role **on your local machine**
via `ansible-galaxy` (which was installed when installing ansible), therefore run:

    ansible-galaxy install openwisp.openwisp2

Choose a working directory
--------------------------

Choose a working directory **on your local machine** where to put the configuration of openwisp2.

This will be useful when you will need to upgrade openwisp2.

Eg:

    mkdir ~/openwisp2-ansible-playbook
    cd ~/openwisp2-ansible-playbook

Putting this working directory under version control is also a very good idea.

Create inventory file
---------------------

The inventory file is where group of servers are defined. In our simple case we can
get away with defining just one group in which we will put just one server.

Create a new file called `hosts` **in your local machine**'s working directory
(the directory just created in the previous step), with the following contents:

    [openwisp2]
    openwisp2.mydomain.com

Substitute `openwisp2.mydomain.com` with your **production server**'s hostname - **DO NOT REPLACE
`openwisp2.mydomain.com` WITH AN IP ADDRESS**, otherwise email sending through postfix will break,
causing 500 internal server errors on some operations.

Create playbook file
--------------------

Create a new playbook file `playbook.yml` **on your local machine** with the following contents:

```yaml
- hosts: openwisp2
  become: "{{ become | default('yes') }}"
  roles:
    - openwisp.openwisp2
  vars:
    openwisp2_default_from_email: "openwisp2@openwisp2.mydomain.com"
```

The line `become: "{{ become | default('yes') }}"` means ansible  will use the `sudo`
program to run each command. You may remove this line if you don't need it (eg: if you are
using the `root` user on the production server).

You may replace `openwisp2` on the `hosts` field with your production server's hostname if you desire.

Substitute `openwisp2@openwisp2.mydomain.com` with what you deem most appropriate
as default sender for emails sent by OpenWISP 2.

Run the playbook
----------------

Now is time to **deploy openwisp2 to the production server**.

Run the playbook **from your local machine** with:

    ansible-playbook -i hosts playbook.yml -u <user> -k --become -K

Substitute `<user>` with your **production server**'s username.

The `-k` argument will need the `sshpass` program.

You can remove `-k`, `--become` and `-K` if your public SSH key is installed on the server.

**Tips**:

- If you have an error like `Authentication or permission failure` then try to use *root* user `ansible-playbook -i hosts playbook.yml -u root -k`
- If you have an error about adding the host's fingerprint to the `known_hosts` file, you can simply connect to the host via SSH and answer yes when prompted; then you can run `ansible-playbook` again.

When the playbook is done running, if you got no errors you can login at:

    https://openwisp2.mydomain.com/admin
    username: admin
    password: admin

Substitute `openwisp2.mydomain.com` with your production server's hostname.

Now proceed with the following steps:

1. change the password (and the username if you like) of the superuser as soon as possible
2. edit the information of the default organization
3. in the default organization you just updated, note down the automatically generated *shared secret*
   option, you will need it to use the [auto-registration feature of openwisp-config](https://github.com/openwisp/openwisp-config#automatic-registration)

Now you are ready to start configuring your network! **If you need help** you can ask questions
on one of the official [OpenWISP Support Channels](http://openwisp.org/support.html).

Install OpenWISP2 for testing in a VirtualBox VM
-------------------------------------------------

If you want to try out **OpenWISP 2** in your own development environment, the safest
way is to use a VirtualBox Virtual Machine (from here on VM).

### Installing Debian 9 on VirtualBox

Install [VirtualBox](https://virtualbox.org) and create a new Virtual Machine running
Debian 9. A step-by-step guide is available
[here](http://www.brianlinkletter.com/installing-debian-linux-in-a-virtualbox-virtual-machine/),
however we need to change a few things to get ansible working.

#### VM configuration

Proceed with the installation as shown in the guide linked above, and come back
here when you see this screen:

![Screenshot of the Software Selection screen](https://raw.githubusercontent.com/openwisp/ansible-openwisp2/master/docs/debian-software-selection.png)

We're only running this as a server, so you can uncheck `Debian desktop environment`.
Make sure `SSH server` and `standard system utilities` are checked.

Next, add a [Host-only Network Adapter](https://www.virtualbox.org/manual/ch06.html#network_hostonly)
and assign an IP address to the VM.

- Go to `File > Preferences > Network > Host-only Networks`
- Click the <kbd>+</kbd> icon to create a new adapter
- Set the IPv4 address to `192.168.56.1` and the IPv4 Network Mask to `255.255.255.0`. The IPv6 settings can be ignored
  ![Screenshot of the Host-only network configuration screen](https://raw.githubusercontent.com/openwisp/ansible-openwisp2/master/docs/host-only-network.png)
- Shut off your VM
- In your VM settings, in the Network section, click Adapter 2
- Select Host-only adapter and the name of the adapter you created
- Boot up your VM, run `su`, and type in your superuser password
- Run `ls /sys/class/net` and take note of the output
- Run `nano /etc/network/interfaces` and add the following at the end of the file:

        auto enp0s8
        iface enp0s8 inet static
            address 192.168.56.2
            netmask 255.255.255.0
            network 192.168.56.0
            broadcast 192.168.56.255

  Replace `enp0s8` with the network interface not present in the file but is shown when running `ls /sys/class/net`
- Save the file with <kbd>Ctrl</kbd><kbd>O</kbd> then <kbd>Enter</kbd>, and exit with <kbd>Ctrl</kbd><kbd>X</kbd>
- Restart the machine by running `reboot`

Make sure you can access your VM via ssh:

```bash
ssh 192.168.56.2
```

#### Back to your local machine

Proceed with these steps in your **local machine**, not the VM.

**Step 1**: [Install ansible](#install-ansible)

**Step 2**: [Install the OpenWISP2 role for Ansible](#install-this-role)

**Step 3**: [Set up a working directory](#choose-a-working-directory)

**Step 4**: Create the `hosts` file

Create an ansible inventory file named `hosts` **in your working directory**
(i.e. not in the VM) with the following contents:

```
[openwisp2]
192.168.56.2
```

**Step 5**: Create the ansible playbook

In the same directory where you created the `host` file,
create an empty file named `playbook.yml` which contains the following:

```yaml
- hosts: openwisp2
  roles:
    - openwisp.openwisp2
  # the following line is needed only when an IP address is used as the inventory hostname
  vars:
      postfix_myhostname: localhost
```

**Step 6**: Run the playbook

```bash
ansible-playbook -i hosts playbook.yml -b -k -K --become-method=su
```

When the playbook ran successfully, you can log in at:

```
https://192.168.56.2/admin
username: admin
password: admin
```

Enabling the network topology module
------------------------------------

To enable the network topology module you need to set `openwisp2_network_topology` to `true` in
your `playbook.yml` file. Here's a short summary of how to do this:

**Step 1**: [Install ansible](#install-ansible)

**Step 2**: [Install this role](#install-this-role)

**Step 3**: [Create inventory file](#create-inventory-file)

**Step 4**: Create a playbook file with following contents:

```yaml
- hosts: openwisp2
  become: "{{ become | default('yes') }}"
  roles:
    - openwisp.openwisp2
  vars:
    openwisp2_network_topology: true
```

**Step 5**: [Run the playbook](#run-the-playbook)

When the playbook is done running, if you got no errors you can login at:

    https://openwisp2.mydomain.com/admin
    username: admin
    password: admin

SSL certificate gotchas
=======================

When you access the admin website you will get an SSL certificate warning because the
playbook creates a self-signed (untrusted) SSL certificate. You can get rid of the warning by
installing your own trusted certificate and set the `openwisp2_ssl_cert` and `openwisp2_ssl_key`
variables accordingly or by following the instructions explained in the section
["Automatic SSL certificate"](#automatic-ssl-certificate).

If you keep the untrusted certificate, you will also need to disable SSL verification on devices
using [openwisp-config](https://github.com/openwisp/openwisp-config) by setting `verify_ssl` to `0`,
although I advice against using this kind of setup in a production environment.

Automatic SSL certificate
=========================

This section explains how to **automatically install and renew a valid SSL certificate** signed by
[letsencrypt](https://letsencrypt.org/).

The first thing you have to do is to setup a valid domain for your openwisp2 instance, this means
your inventory file (hosts) should look like the following:

    [openwisp2]
    openwisp2.yourdomain.com

You must be able to add a DNS record for `openwisp2.yourdomain.com`, you cannot use an ip address
in place of `openwisp2.yourdomain.com`.

Once your domain is set up and the DNS record is propagated, proceed by installing the ansible role
[thefinn93.letsencrypt](https://github.com/thefinn93/ansible-letsencrypt):

    sudo ansible-galaxy install thefinn93.letsencrypt

Then proceed to edit your `playbook.yml` so that it will look similar to the following example:

```yaml
- hosts: openwisp2
  become: "{{ become | default('yes') }}"
  roles:
    - thefinn93.letsencrypt
    - openwisp.openwisp2
  vars:
    # SSL certificates
    openwisp2_ssl_cert: "/etc/letsencrypt/live/{{ ansible_fqdn }}/fullchain.pem"
    openwisp2_ssl_key: "/etc/letsencrypt/live/{{ ansible_fqdn }}/privkey.pem"
    # letsencrypt configuration
    letsencrypt_webroot_path: "{{ openwisp2_path }}/public_html"
    letsencrypt_email: <YOUR_EMAIL_HERE>
    letsencrypt_renewal_command_args: '--renew-hook "service nginx restart"'
    letsencrypt_renewal_frequency:
      day: "*"
      hour: "7,19"  # renewal cronjob runs at 7 AM and at 7 PM
      minute: 0
```

Fill a real email address in place of `<YOUR_EMAIL_HERE>`, it may be used by [letsencrypt](https://letsencrypt.org/)
to send you important communications regarding your SSL certificate.

Once you have set up all the variables correctly, run the playbook again.

Upgrading openwisp2
===================

Update this ansible-role via `ansible-galaxy`:

    sudo ansible-galaxy install --force openwisp.openwisp2

Run `ansible-playbook` again **from your local machine**:

    ansible-playbook -i hosts playbook.yml

You may also run the playbook automatically periodically or when a new release of OpenWISP2, for
example, by setting up a continuous integration system.

Role variables
==============

This role has many variables values that can be changed to best suit
your needs.

Below are listed all the variables you can customize (you may also want to take a look at
[the default values of these variables](https://github.com/openwisp/ansible-openwisp2/blob/master/defaults/main.yml)).

```yaml
- hosts: yourhost
  roles:
  # you can add other roles here
    - openwisp.openwisp2
  vars:
    # optional openwisp2 modules
    openwisp2_network_topology: false
    # you may replace the values of these variables with any URL
    # supported by pip (the python package installer)
    # use these to install forks, branches or development versions
    # WARNING: only do this if you know what you are doing; disruption
    # of service is very likely to occur during development
    openwisp2_controller_pip: false
    openwisp2_users_pip: false
    openwisp2_django_netjsonconfig_pip: false
    openwisp2_django_x509_pip: false
    openwisp2_netjsonconfig_pip: false
    openwisp2_network_topology_pip: false
    openwisp2_django_netjsongraph_pip: false
    # by default python3 is used, if may need to set this to python2.7 for older systems
    openwisp2_python: python2.7
    # customize the app_path
    openwisp2_path: /opt/openwisp2
    # It is recommended that you change the value of this variable if you intend to use
    # OpenWISP2 in production, as a misconfiguration may result in emails not being sent
    openwisp2_default_from_email: "openwisp2@yourhostname.com"
    # edit database settings only if you are not using sqlite
    openwisp2_database:
        engine: django.db.backends.postgresql
        name: openwisp2
        user: postgres
        password: ""
        host: ""
        port: ""
        options: {}
    # SPATIALITE_LIBRARY_PATH django setting
    openwisp2_spatialite_path: "mod_spatialite"
    # customize other django settings:
    openwisp2_language_code: en-gb
    openwisp2_time_zone: UTC
    # django-netjsonconfig context
    openwisp2_context: {}
    # additional allowed hosts
    openwisp2_allowed_hosts:
        - myadditionalhost.openwisp.org
    # geographic map settings
    openwisp2_leaflet_config:
        DEFAULT_CENTER: [42.06775, 12.62011]
        DEFAULT_ZOOM: 6
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
    # additional python packages that will be installed with pip
    openwisp2_extra_python_packages:
        - bpython
        - django-owm-legacy
    # additional django apps that will be added to settings.INSTALLED_APPS
    # (if the app needs to be installed, the name its python package
    # must be also added to the openwisp2_extra_python_packages var)
    openwisp2_extra_django_apps:
        - owm_legacy
    # additional django settings example
    openwisp2_extra_django_settings:
        - CSRF_COOKIE_AGE: 2620800.0
    # extra URL settings for django
    openwisp2_extra_urls: "url(r'', include('my_custom_app.urls'))"
    # spdy protocol support (disabled by default)
    openwisp2_nginx_spdy: false
    # HTTP2 protocol support (disabled by default)
    openwisp2_nginx_http2: false
    # ipv6 must be enabled explicitly to avoid errors
    openwisp2_nginx_ipv6: false
    # dictionary containing more nginx settings for
    # the 443 section of the openwisp2 nginx configuration
    # IMPORTANT: 1. you can add more nginx settings in this dictionary
    #            2. here we list the default values used
    openwisp2_nginx_ssl_config:
        gzip: "on"
        gzip_comp_level: "6"
        gzip_proxied: "any"
        gzip_min_length: "1000"
        gzip_types:
            - "text/plain"
            - "text/html"
            - "image/svg+xml"
            - "application/json"
            - "application/javascript"
            - "text/xml"
            - "text/css"
            - "application/xml"
            - "application/x-font-ttf"
            - "font/opentype"
    # the following setting controls which ip address range
    # is allowed to access the openwisp2 admin web interface
    # (by default any IP is allowed)
    openwisp2_admin_allowed_network: null
    # install ntp client (enabled by default)
    openwisp2_install_ntp: true
    # enable sentry example
    openwisp2_sentry:
        dsn: "https://7d2e3cd61acc32eca1fb2a390f7b55e1:bf82aab5ddn4422688e34a486c7426e3@getsentry.com:443/12345"
    openwisp2_default_cert_validity: 1825
    openwisp2_default_ca_validity: 3650
    # redis cache url
    openwisp2_redis_cache_url: redis://127.0.0.1:6379/1
```

Support
=======

See [OpenWISP Support Channels](http://openwisp.org/support.html).
