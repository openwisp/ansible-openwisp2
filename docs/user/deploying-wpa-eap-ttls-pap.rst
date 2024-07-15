Configuring FreeRADIUS for WPA Enterprise (EAP-TTLS-PAP)
========================================================

You can use OpenWISP RADIUS for setting up WPA Enterprise (EAP-TTLS-PAP)
authentication. This allows to authenticate on WiFi networks using Django
user credentials. Prior to proceeding, ensure you've reviewed the tutorial
on :doc:`/tutorials/wpa-enterprise-eap-ttls-pap`. This documentation
section complements the tutorial and focuses solely on demonstrating the
ansible role's capabilities to configure FreeRADIUS.

.. important::

    The ansible role supports OpenWISP's multi-tenancy by creating
    individual FreeRADIUS sites for each organization. You must include
    configuration details for **each organization** that will use WPA
    Enterprise.

Here's an example playbook which enables OpenWISP RADIUS module, installs
FreeRADIUS, and configures it for WPA Enterprise (EAP-TTLS-PAP):

.. code-block:: yaml

    - hosts: openwisp2
      become: "{{ become | default('yes') }}"
      roles:
        - openwisp.openwisp2
      vars:
        openwisp2_radius: true
        openwisp2_freeradius_install: true
        # Define a list of dictionaries detailing each organization's
        # name, UUID, RADIUS token, and ports for authentication,
        # accounting, and the inner tunnel. These details will be used
        # to create FreeRADIUS sites tailored for WPA Enterprise
        # (EAP-TTLS-PAP) authentication per organization.
        freeradius_eap_orgs:
            # A reference name for the organization,
            # used in FreeRADIUS configurations.
            # Don't use spaces or special characters.
          - name: openwisp
            # UUID of the organization.
            # You can retrieve this from the organization admin
            # in the OpenWISP web interface.
            uuid: 00000000-0000-0000-0000-000000000000
            # Radius token of the organization.
            # You can retrieve this from the organization admin
            # in the OpenWISP web interface.
            radius_token: secret-radius-token
            # Port used by the authentication service for
            # this FreeRADIUS site
            auth_port: 1822
            # Port used by the accounting service for this FreeRADIUS site
            acct_port: 1823
            # Port used by the authentication service of inner tunnel
            # for this FreeRADIUS site
            inner_tunnel_auth_port: 18230
            # If you want to use a custom certificate for FreeRADIUS
            # EAP module, you can specify the path to the CA, server
            # certificate, and private key, and DH key as follows.
            # Ensure that these files can be read by the "freerad" user.
            cert: /etc/freeradius/certs/cert.pem
            private_key: /etc/freeradius/certs/key.pem
            ca: /etc/freeradius/certs/ca.crt
            dh: /etc/freeradius/certs/dh
            tls_config_extra: |
              private_key_password = whatever
              ecdh_curve = "prime256v1"
          # You can add as many organizations as you want
          - name: demo
            uuid: 00000000-0000-0000-0000-000000000001
            radius_secret: demo-radius-token
            auth_port: 1832
            acct_port: 1833
            inner_tunnel_auth_port: 18330
            # If you omit the certificate fields,
            # the FreeRADIUS site will use the default certificates
            # located in /etc/freeradius/certs.

In the example above, custom ports 1822, 1823, and 18230 are utilized for
FreeRADIUS authentication, accounting, and inner tunnel authentication,
respectively. These custom ports are specified because the Ansible role
creates a common FreeRADIUS site for all organizations, which also
supports captive portal functionality. This common site is configured to
listen on the default FreeRADIUS ports 1812, 1813, and 18120. Therefore,
when configuring WPA Enterprise authentication for each organization,
unique ports must be provided to ensure proper isolation and
functionality.

Using Let's Encrypt Certificate for WPA Enterprise (EAP-TTLS-PAP)
-----------------------------------------------------------------

In this section, we demonstrate how to utilize Let's Encrypt certificates
for WPA Enterprise (EAP-TTLS-PAP) authentication. Similar to the
:doc:`./certbot-ssl`, we use `geerlingguy.certbot
<https://galaxy.ansible.com/geerlingguy/certbot/>`_ role to automatically
install and renew a valid SSL certificate.

The following example playbook achieves the following goals:

- Provision a separate Let's Encrypt certificate for the
  `freeradius.yourdomain.com` hostname. This certificate will be utilized
  by the FreeRADIUS site for WPA Enterprise authentication.
- Create a renewal hook to set permissions on the generated certificate so
  the FreeRADIUS server can read it.

.. note::

    You can also use the same SSL certificate for both Nginx and
    FreeRADIUS, but it's crucial to understand the security implications.
    Please exercise caution and refer to the example playbook comments for
    guidance.

.. code-block:: yaml

    - hosts: openwisp2
      become: "{{ become | default('yes') }}"
      roles:
        - geerlingguy.certbot
        - openwisp.openwisp2
      vars:
        # certbot configuration
        certbot_auto_renew_minute: "20"
        certbot_auto_renew_hour: "5"
        certbot_create_if_missing: true
        certbot_auto_renew_user: "<privileged-users-to-renew-certs>"
        certbot_certs:
          - email: "<paste-your-email>"
            domains:
              - "{{ inventory_hostname }}"
          # If you choose to re-use the same certificate for both services,
          # you can omit the following item in your playbook.
          - email: "<paste-your-email>"
            domains:
              - "freeradius.yourdomain.com"
        # Configuration to use Let's Encrypt certificate for OpenWISP server (Nnginx)
        openwisp2_ssl_cert: "/etc/letsencrypt/live/{{ inventory_hostname }}/fullchain.pem"
        openwisp2_ssl_key: "/etc/letsencrypt/live/{{ inventory_hostname }}/privkey.pem"
        # Configuration for openwisp-radius
        openwisp2_radius: true
        openwisp2_freeradius_install: true
        freeradius_eap_orgs:
          - name: demo
            uuid: 00000000-0000-0000-0000-000000000001
            radius_secret: demo-radius-token
            auth_port: 1832
            acct_port: 1833
            inner_tunnel_auth_port: 18330
            # Update the cert_file and private_key paths to point to the
            # Let's Encrypt certificate.
            cert: /etc/letsencrypt/live/freeradius.yourdomain.com/fullchain.pem
            private_key: /etc/letsencrypt/live/freeradius.yourdomain.com/privkey.pem
            # If you choose to re-use the same certificate for both services,
            # your configuration would look like this
            # cert: /etc/letsencrypt/live/{{ inventory_hostname }}/fullchain.pem
            # private_key: /etc/letsencrypt/live/{{ inventory_hostname }}/privkey.pem
      tasks:
        # Tasks to ensure the Let's Encrypt certificate can be read by the FreeRADIUS server.
        # If you are using the same certificate for both services, you need to
        # replace "freeradius.yourdomain.com" with "{{ inventory_hostname }}"
        # in the following task.
        - name: "Create a renewal hook for setting permissions on /etc/letsencrypt/live/freeradius.yourdomain.com"
          copy:
            content: |
              #!/bin/bash
              chown -R root:freerad /etc/letsencrypt/live/ /etc/letsencrypt/archive/
              chmod 0750 /etc/letsencrypt/live/ /etc/letsencrypt/archive/
              chmod -R 0640 /etc/letsencrypt/archive/freeradius.yourdomain.com/
              chmod 0750 /etc/letsencrypt/archive/freeradius.yourdomain.com/
            dest: /etc/letsencrypt/renewal-hooks/post/chown_freerad
            owner: root
            group: root
            mode: '0700'
          register: chown_freerad_result
        - name: Change the ownership of the certificate files
          when: chown_freerad_result.changed
          command: /etc/letsencrypt/renewal-hooks/post/chown_freerad
