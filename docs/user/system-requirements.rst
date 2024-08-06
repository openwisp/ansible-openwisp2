System Requirements
===================

The following specifications will run a new, *empty* instance of OpenWISP.
Please ensure you account for the amount of disk space your use case will
require, e.g. allocate enough space for users to upload floor plan images.

Hardware Requirements (Recommended)
-----------------------------------

- 2 CPUs
- 2 GB Memory
- Disk space - depends on the projected size of your database and uploaded
  photo images

Keep in mind that increasing the number of celery workers will require
more memory and CPU. You will need to increase the amount of celery
workers as the number of devices you manage grows.

For more information about how to increase concurrency, look for the
variables which end with ``_concurrency`` or ``_autoscale`` in the
:doc:`role-variables` section.

Software
--------

A fresh installation of one of the supported operating systems is
generally sufficient, with no preconfiguration required. The Ansible
Playbook will handle the installation and configuration of all
dependencies, providing you with a fully operational OpenWISP setup.

.. important::

    Ensure the hostname of your target machine matches what is in your
    Ansible configuration file. Also, please ensure that Ansible can
    access your target machine by SSH, be it either with a key or
    password. For more information see the `Ansible Getting Started
    Documentation
    <https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html>`__.

Supported Operating Systems
---------------------------

- Debian 12
- Debian 11
- Ubuntu 24 LTS
- Ubuntu 22 LTS
- Ubuntu 20 LTS
