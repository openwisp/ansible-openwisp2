Enabling the RADIUS Module
==========================

To enable the :doc:`RADIUS module </user/radius>` you need to set
``openwisp2_radius`` to ``true`` in your ``playbook.yml`` file. Here's a
short summary of how to do this:

**Step 1**: :ref:`Install ansible <ansible_install>`

**Step 2**: :ref:`Install this role <ansible_install_role>`

**Step 3**: :ref:`Create inventory file <ansible_create_inventory_file>`

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

.. note::

    ``openwisp2_freeradius_install`` option provides a basic configuration
    of freeradius for OpenIWSP, it sets up the `radius user token
    mechanism
    <https://openwisp-radius.readthedocs.io/en/latest/user/api.html#radius-user-token-recommended>`__
    if you want to use another mechanism or manage your freeradius
    separately, please disable this option by setting it to ``false``.

**Step 5**: :ref:`Run the playbook <ansible_run_playbook>`

When the playbook is done running, if you got no errors you can login at:

.. code-block::

    https://openwisp2.mydomain.com/admin
    username: admin
    password: admin

**Note:** for more information regarding radius configuration options,
look for the word “radius” in the :doc:`role-variables` section of this
document.
