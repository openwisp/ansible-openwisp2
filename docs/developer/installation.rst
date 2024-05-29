Install ansible-openwisp2 for development
=========================================

.. note::

    If you need to modify the logic of this ansible role and you need to
    test your changes here we explain how to do it.

First of all, create the directory where you want to place the
repositories of the ansible roles and create directory roles.

.. code-block:: bash

    mkdir -p ~/openwisp-dev/roles
    cd ~/openwisp-dev/roles

Clone ``ansible-openwisp2`` and ``Stouts.postfix`` as follows:

.. code-block:: bash

    git clone https://github.com/openwisp/ansible-openwisp2.git openwisp.openwisp2
    git clone https://github.com/Stouts/Stouts.postfix
    git clone https://github.com/openwisp/ansible-ow-influxdb openwisp.influxdb

Now, go to the parent directory & create hosts file and playbook.yml:

.. code-block:: bash

    cd ../
    touch hosts
    touch playbook.yml

From here on you can follow the instructions available at the following
sections:

- `Create inventory file <#create-inventory-file>`__
- `Create playbook file <#create-playbook-file>`__
- `Run the playbook <#run-the-playbook>`__

**Note:** Please remember to `install ansible <#install-ansible>`__.

All done!

How to run tests
----------------

If you want to contribute to ``ansible-openwisp2`` you should run tests in
your development environment to ensure your changes are not breaking
anything.

To do that, proceed with the following steps:

**Step 1**: Clone ``ansible-openwisp2``

Clone repository by:

.. code-block::

    git clone https://github.com/<your_fork>/ansible-openwisp2.git openwisp.openwisp2
    cd openwisp.openwisp2

**Step 2**: Install docker

If you haven't installed docker yet, you need to install it (example for
linux debian/ubuntu systems):

.. code-block::

    sudo apt-get install docker.io

**Step 3**: Install molecule and dependences

.. code-block::

    pip install molecule[docker] molecule-plugins yamllint ansible-lint docker

**Step 4**: Download docker images

.. code-block::

    docker pull geerlingguy/docker-ubuntu2204-ansible:latest
    docker pull geerlingguy/docker-ubuntu2004-ansible:latest
    docker pull geerlingguy/docker-debian11-ansible:latest

**Step 5**: Run molecule test

.. code-block::

    molecule test -s local

If you don't get any error message it means that the tests ran
successfully without errors.

**ProTip:** Use ``molecule test --destroy=never`` to speed up subsequent
test runs.
