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
        secret_key: fdPt*+$-ueeyic6-#txyy$5yf2er@c0d2n#h)qb)y5@lc$t*@w
        shared_secret: changemeplease
        https: on
        stable: true
        # customize the self-signed SSL certificate info if needed
        #ssl_country: "US"
        #ssl_state: "California"
        #ssl_locality: "San Francisco"
        #ssl_organization: "IT dep."

Run the playbook::

    ansible-playbook -i hosts site.yml -l yourhost
