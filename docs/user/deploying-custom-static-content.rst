Deploying Custom Static Content
===============================

For deploying custom static content (HTML files, etc.) add all the static
content in ``files/ow2_static`` directory. The files inside
``files/ow2_static`` will be uploaded to a directory named
``static_custom`` in ``openwisp2_path``.

This is helpful for :ref:`customizing OpenWISP's theme
<openwisp_admin_theme_links>`.

E.g., if you added a custom CSS file in
``files/ow2_static/css/custom.css``, the file location to use in
:ref:`openwisp_admin_theme_links` setting will be ``css/custom.css``.
