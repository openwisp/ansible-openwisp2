Troubleshooting
===============

OpenWISP is deployed using **uWSGI**, it also uses **daphne** fo
WebSockets and **celery** as task queue.

All this services are run by **supervisor**.

.. code-block:: shell

    sudo service supervisor start|stop|status

You can view each individual process run by supervisor with the following
command:

.. code-block:: shell

    sudo supervisorctl status

For more info about Supervisord, refer to `Running supervisorctl
<http://supervisord.org/running.html#running-supervisorctl>`__.

The **nginx** web server sits in front of the **uWSGI** application
server. You can control nginx with the following commands:

.. code-block:: shell

    service nginx status start|stop|status

OpenWISP is installed in ``/opt/openwisp2`` (unless you changed the
``openwisp2_path`` variable in the ansible playbook configuration), these
are some useful directories to look for when experiencing issues.

========================= ==========================
Location                  Description
========================= ==========================
/opt/openwisp2            The OpenWISP 2 root dir.
/opt/openwisp2/log        Log files
/opt/openwisp2/env        Python virtual env
/opt/openwisp2/db.sqlite3 OpenWISP 2 sqlite database
========================= ==========================

All processes are running as ``www-data`` user.

If you need to copy or edit files, you can switch to ``www-data`` user
with the following commands:

.. code-block:: shell

    sudo su www-data -s /bin/bash
    cd /opt/openwisp2
    source env/bin/activate

SSL Certificate Gotchas
-----------------------

When you access the admin website you will get an SSL certificate warning
because the playbook creates a self-signed (untrusted) SSL certificate.
You can get rid of the warning by installing your own trusted certificate
and set the ``openwisp2_ssl_cert`` and ``openwisp2_ssl_key`` variables
accordingly or by following the instructions explained in the section
:doc:`certbot-ssl`.

If you keep the untrusted certificate, you will also need to disable SSL
verification on devices using :doc:`openwisp-config
</openwrt-config-agent/index>` by setting ``verify_ssl`` to ``0``,
although we advice against using this kind of setup in a production
environment.
