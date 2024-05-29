Deploying custom static content
===============================

For deploying custom static content (HTML files, etc.) add all the static
content in ``files/ow2_static`` directory. The files inside
``files/ow2_static`` will be uploaded to a directory named
``static_custom`` in ``openwisp2_path``.

This is helpful for `customizing OpenWISP's theme
<https://github.com/openwisp/openwisp-utils#openwisp_admin_theme_links>`__.

E.g., if you added a custom CSS file in
``files/ow2_static/css/custom.css``, the file location to use in
`OPENWISP_ADMIN_THEME_LINKS
<https://github.com/openwisp/openwisp-utils#openwisp_admin_theme_links>`__
setting will be ``css/custom.css``.
