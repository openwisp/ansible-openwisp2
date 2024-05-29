Enabling the RADIUS module
==========================

To enable the `RADIUS module
<https://openwisp.io/docs/user/radius.html>`__ you need to set
``openwisp2_radius`` to ``true`` in your ``playbook.yml`` file. Here's a
short summary of how to do this:

**Step 1**: `Install ansible <#install-ansible>`__

**Step 2**: `Install this role <#install-this-role>`__

**Step 3**: `Create inventory file <#create-inventory-file>`__

**Step 4**: Create a playbook file with following contents:

.. code-block:: yaml

    - hosts: openwisp2
      become: "{{ become | default('yes') }}"
      roles:
        - openwisp.openwisp2
      vars:
        openwisp2_radius: true
        openwisp2_freeradius_install: true
        # set to false when you don't want to register openwisp-radius
        # API endpoints.
        openwisp2_radius_urls: true

**Note:** ``openwisp2_freeradius_install`` option provides a basic
configuration of freeradius for openwisp, it sets up the `radius user
token mechanism
<https://openwisp-radius.readthedocs.io/en/latest/user/api.html#radius-user-token-recommended>`__
if you want to use another mechanism or manage your freeradius separately,
please disable this option by setting it to ``false``.

**Step 5**: `Run the playbook <#run-the-playbook>`__

When the playbook is done running, if you got no errors you can login at:

.. code-block::

    https://openwisp2.mydomain.com/admin
    username: admin
    password: admin

**Note:** for more information regarding radius configuration options,
look for the word “radius” in the `Role variables <#role-variables>`__
section of this document.
