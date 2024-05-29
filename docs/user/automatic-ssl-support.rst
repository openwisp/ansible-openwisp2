Automatic SSL certificate
=========================

This section explains how to **automatically install and renew a valid SSL
certificate** signed by `letsencrypt <https://letsencrypt.org/>`__.

The first thing you have to do is to setup a valid domain for your
openwisp2 instance, this means your inventory file (hosts) should look
like the following:

.. code-block:: text

    [openwisp2]
    openwisp2.yourdomain.com

You must be able to add a DNS record for ``openwisp2.yourdomain.com``, you
cannot use an ip address in place of ``openwisp2.yourdomain.com``.

Once your domain is set up and the DNS record is propagated, proceed by
installing the ansible role `geerlingguy.certbot
<https://galaxy.ansible.com/geerlingguy/certbot/>`__:

.. code-block:: shell

    ansible-galaxy install geerlingguy.certbot

Then proceed to edit your ``playbook.yml`` so that it will look similar to
the following example:

.. code-block:: yaml

    - hosts: openwisp2
      become: "{{ become | default('yes') }}"
      roles:
        - geerlingguy.certbot
        - openwisp.openwisp2
      vars:
        # SSL certificates
        openwisp2_ssl_cert: "/etc/letsencrypt/live/{{ inventory_hostname }}/fullchain.pem"
        openwisp2_ssl_key: "/etc/letsencrypt/live/{{ inventory_hostname }}/privkey.pem"

        # certbot configuration
        certbot_auto_renew_minute: "20"
        certbot_auto_renew_hour: "5"
        certbot_create_if_missing: true
        certbot_auto_renew_user: "<privileged-users-to-renew-certs>"
        certbot_certs:
          - email: "<paste-your-email>"
            domains:
              - "{{ inventory_hostname }}"
      pre_tasks:
        - name: Update APT package cache
          apt:
            update_cache: true
            changed_when: false
            retries: 5
            delay: 10
            register: result
            until: result is success

Read the `documentation of geerlingguy.certbot
<https://github.com/geerlingguy/ansible-role-certbot#readme>`__ to learn
more about configuration of certbot role.

Once you have set up all the variables correctly, run the playbook again.
