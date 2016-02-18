ansible-openwisp2
=================

Ansible role for the nascent openwisp2 controller.

Usable but not stable, will probably change a lot over time.

Usage
=====

Add an entry to your ``site.yml`` like the following one:

.. code-block:: yaml

    - hosts: yourhost
      roles:
      # you can add other roles here
        - openwisp2
      vars:
        # change scret_key and shared_secret for security reasons
        openwisp2_secret_key: fdPt*+$-ueeyic6-#txyy$5yf2er@c0d2n#h)qb)y5@lc$t*@w
        openwisp2_shared_secret: changemeplease
        openwisp2_stable: true
        # customize the app_path
        #openwisp2_path: /opt/openwisp2
        # customize django settings:
        #openwisp2_language_code: en-gb
        #openwisp2_time_zone: UTC
        # customize the self-signed SSL certificate info if needed
        #openwisp2_ssl_country: "US"
        #openwisp2_ssl_state: "California"
        #openwisp2_ssl_locality: "San Francisco"
        #openwisp2_ssl_organization: "IT dep."

Run the playbook::

    ansible-playbook -i hosts site.yml -l yourhost
