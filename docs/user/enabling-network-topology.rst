Enabling the Network Topology Module
====================================

To enable the :doc:`Network Topology module <network-topology/index>` you
need to set ``openwisp2_network_topology`` to ``true`` in your
``playbook.yml`` file. Here's a short summary of how to do this:

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
        openwisp2_network_topology: true

**Step 5**: :ref:`Run the playbook <ansible_run_playbook>`

When the playbook is done running, if you got no errors you can login at
https://openwisp2.mydomain.com/admin with the following credentials:

.. code-block:: text

    username: admin
    password: admin
