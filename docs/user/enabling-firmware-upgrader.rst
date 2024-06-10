Enabling the Firmware Upgrader Module
=====================================

**Note**: It is encouraged that you read the :doc:`quick-start guide of
openwisp-firmware-upgrader </firmware-upgrader/user/quickstart>` before
going ahead.

To enable the :doc:`Firmware Upgrader </firmware-upgrader/index>` module
you need to set ``openwisp2_firmware_upgrader`` to ``true`` in your
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
        openwisp2_firmware_upgrader: true

**Step 5**: :ref:`Run the playbook <ansible_run_playbook>`

When the playbook is done running, if you got no errors you can login at
https://openwisp2.mydomain.com/admin with the following credentials:

.. code-block:: text

    username: admin
    password: admin

You can configure :doc:`openwisp-firmware-upgrader specific settings
<firmware-upgrader/user/settings>` using the
``openwisp2_extra_django_settings`` or
``openwisp2_extra_django_settings_instructions``.

E.g:

.. code-block:: yaml

    - hosts: openwisp2
      become: "{{ become | default('yes') }}"
      roles:
        - openwisp.openwisp2
      vars:
        openwisp2_firmware_upgrader: true
        openwisp2_extra_django_settings_instructions:
          - |
            OPENWISP_CUSTOM_OPENWRT_IMAGES = (
                ('my-custom-image-squashfs-sysupgrade.bin', {
                    'label': 'My Custom Image',
                    'boards': ('MyCustomImage',)
                }),
            )

Refer the :doc:`role-variables` section of the documentation for a
complete list of available role variables.
