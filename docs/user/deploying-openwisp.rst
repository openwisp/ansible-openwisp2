Usage (tutorial)
================

.. note::

    **NOTE**: it is highly suggested to use this procedure on clean
    virtual machines or linux containers.

.. raw:: html

    <p>
        <iframe width="560"
                height="315"
                src="https://www.youtube.com/watch?v=v_DUeFUGG8Q"
                frameborder="0"
                allowfullscreen>
        </iframe>
    </p>

If you don't know how to use ansible, don't panic, this procedure will
guide you towards a fully working basic openwisp2 installation.

If you already know how to use ansible, you can skip this tutorial.

First of all you need to understand two key concepts:

- for **“production server”** we mean a server (**not a laptop or a
  desktop computer!**) with public ipv4 / ipv6 which is used to host
  openwisp2
- for **“local machine”** we mean the host from which you launch ansible,
  eg: your own laptop

Ansible is a configuration management tool that works by entering
production servers via SSH, **so you need to install it and configure it
on the machine where you launch the deployment** and this machine must be
able to SSH into the production server.

Ansible will be run on your local machine and from there it will connect
to the production server to install openwisp2.

**If you are trying to install OpenWISP2 on your laptop or desktop pc just
for testing purposes**, please read :doc:`Install OpenWISP2 for testing in
a VirtualBox VM <./installing-on-vm>`.

.. _install_ansible:

Install ansible
---------------

Install ansible (recommended version 2.12) **on your local machine** (not
the production server!) if you haven't done already.

To **install ansible** we suggest you follow the official `ansible
installation guide
<https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-in-a-virtual-environment-with-pip>`__.
It is recommended to install ansible through a virtual environment to
avoid dependency issues.

Please ensure that you have the correct version of Jinja installed in your
Python environment: ``pip install Jinja2>=2.11``

.. _install_ansible_openwisp2:

Install this role
-----------------

For the sake of simplicity, the easiest thing is to install this role **on
your local machine** via ``ansible-galaxy`` (which was installed when
installing ansible), therefore run:

.. code-block:: shell

    ansible-galaxy install openwisp.openwisp2

Ensure that you have the ```community.general``
<https://github.com/ansible-collections/community.general>`__ and
``ansible.posix`` collections installed and up to date:

.. code-block:: shell

    ansible-galaxy collection install "community.general:>=3.6.0"
    ansible-galaxy collection install "ansible.posix"

Choose a working directory
--------------------------

Choose a working directory **on your local machine** where to put the
configuration of openwisp2.

This will be useful when you will need to upgrade openwisp2.

Eg:

.. code-block:: shell

    mkdir ~/openwisp2-ansible-playbook
    cd ~/openwisp2-ansible-playbook

Create inventory file
---------------------

The inventory file is where group of servers are defined. In our simple
case we will define just one group in which we will put just one server.

Create a new file called ``hosts`` in the working directory **on your
local machine** (the directory just created in the previous step), with
the following contents:

.. code-block:: text

    [openwisp2]
    openwisp2.mydomain.com

Substitute ``openwisp2.mydomain.com`` with your **production server**'s
hostname - **DO NOT REPLACE ``openwisp2.mydomain.com`` WITH AN IP
ADDRESS**, otherwise email sending through postfix will break, causing 500
internal server errors on some operations.

Create playbook file
--------------------

Create a new playbook file ``playbook.yml`` **on your local machine** with
the following contents:

.. code-block:: yaml

    - hosts: openwisp2
      become: "{{ become | default('yes') }}"
      roles:
        - openwisp.openwisp2
      vars:
        openwisp2_default_from_email: "openwisp2@openwisp2.mydomain.com"

The line ``become: "{{ become | default('yes') }}"`` means ansible will
use the ``sudo`` program to run each command. You may remove this line if
you don't need it (eg: if you are ``root`` user on the production server).

You may replace ``openwisp2`` on the ``hosts`` field with your production
server's hostname if you desire.

Substitute ``openwisp2@openwisp2.mydomain.com`` with what you deem most
appropriate as default sender for emails sent by OpenWISP 2.

Run the playbook
----------------

Now is time to **deploy openwisp2 to the production server**.

Run the playbook **from your local machine** with:

.. code-block:: shell

    ansible-playbook -i hosts playbook.yml -u <user> -k --become -K

Substitute ``<user>`` with your **production server**'s username.

The ``-k`` argument will need the ``sshpass`` program.

You can remove ``-k``, ``--become`` and ``-K`` if your public SSH key is
installed on the server.

**Tips**:

- If you have an error like ``Authentication or permission failure`` then
  try to use *root* user ``ansible-playbook -i hosts playbook.yml -u root
  -k``
- If you have an error about adding the host's fingerprint to the
  ``known_hosts`` file, you can simply connect to the host via SSH and
  answer yes when prompted; then you can run ``ansible-playbook`` again.

When the playbook is done running, if you got no errors you can login at
`https://openwisp2.mydomain.com/admin` with the following credentials:

.. code-block:: text

    username: admin
    password: admin

Substitute ``openwisp2.mydomain.com`` with your production server's
hostname.

Now proceed with the following steps:

1. change the password (and the username if you like) of the superuser as
   soon as possible
2. update the ``name`` field of the default ``Site`` object to accurately
   display site name in email notifications
3. edit the information of the default organization
4. in the default organization you just updated, note down the
   automatically generated *shared secret* option, you will need it to use
   the `auto-registration feature of openwisp-config
   <https://github.com/openwisp/openwisp-config#automatic-registration>`__
5. this Ansible role creates a default template to update
   ``authorized_keys`` on networking devices using the default access
   credentials. The role will either use an existing SSH key pair or
   create a new one if no SSH key pair exists on the host machine.

Now you are ready to start configuring your network! **If you need help**
you can ask questions on one of the official `OpenWISP Support Channels
<http://openwisp.org/support.html>`__.

Upgrading openwisp2
===================

**It's highly recommended to back up your current instance before
upgrading**.

Update this ansible-role via ``ansible-galaxy``:

.. code-block:: shell

    ansible-galaxy install --force openwisp.openwisp2

Run ``ansible-playbook`` again **from your local machine**:

.. code-block:: shell

    ansible-playbook -i hosts playbook.yml

You may also run the playbook automatically periodically or when a new
release of OpenWISP2, for example, by setting up a continuous integration
system.

Deploying the upcoming release of OpenWISP
==========================================

The following steps will help you set up and install the new version of
OpenWISP which is not released yet, but ships new features and fixes.

Create a directory for organizing your playbook, roles and collections. In
this example, ``openwisp-dev`` is used. Create ``roles`` and
``collections`` directories in ``~/openwisp-dev``.

.. code-block::

    mkdir -p ~/openwisp-dev/roles
    mkdir -p ~/openwisp-dev/collections

Change directory to ``~/openwisp-dev/`` in terminal and create
configuration and requirement files for Ansible.

.. code-block::

    cd ~/openwisp-dev/
    touch ansible.cfg
    touch requirements.yml

Setup ``roles_path`` and ``collections_paths`` variables in
``ansible.cfg`` as follows:

.. code-block::

    [defaults]
    roles_path=~/openwisp-dev/roles
    collections_paths=~/openwisp-dev/collections

Ensure your ``requirements.yml`` contains following content:

.. code-block:: yml

    ---
    roles:
      - src: https://github.com/openwisp/ansible-openwisp2.git
        version: master
        name: openwisp.openwisp2-dev
    collections:
      - name: community.general
        version: ">=3.6.0"

Install requirements from the ``requirements.yml`` as follows

.. code-block::

    ansible-galaxy install -r requirements.yml

Now, create hosts file and playbook.yml:

.. code-block::

    touch hosts
    touch playbook.yml

Follow instructions in `“Create inventory file”
<#create-inventory-file>`__ section to configure ``hosts`` file.

You can reference the example playbook below (tested on Debian 11) for
installing a fully-featured version of OpenWISP.

.. code-block:: yml

    - hosts: openwisp2
      become: "{{ become | default('yes') }}"
      roles:
        - openwisp.openwisp2-dev
      vars:
        openwisp2_network_topology: true
        openwisp2_firmware_upgrader: true
        openwisp2_radius: true
        openwisp2_monitoring: true # monitoring is enabled by default

Read `“Role Variables” <#role-variables>`__ section to learn about
available configuration variables.

Follow instructions in `“Run the playbook” <#run-the-playbook>`__ section
to run above playbook.
