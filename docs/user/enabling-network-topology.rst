Enabling the Network Topology module
====================================

To enable the `Network Topology module
<https://openwisp.io/docs/user/network-topology.html>`__ you need to set
``openwisp2_network_topology`` to ``true`` in your ``playbook.yml`` file.
Here's a short summary of how to do this:

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
        openwisp2_network_topology: true

**Step 5**: `Run the playbook <#run-the-playbook>`__

When the playbook is done running, if you got no errors you can login at:

.. code-block::

    https://openwisp2.mydomain.com/admin
    username: admin
    password: admin
