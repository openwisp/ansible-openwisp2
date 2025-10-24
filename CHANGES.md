# Change log

## Version 25.10.0 [2025-10-24]

### Features

- Made Daphne socket configurable.
- Added Calling-Station-ID and Called-Station-ID attributes to the FreeRADIUS REST configuration [#548](https://github.com/openwisp/ansible-openwisp2/issues/548).
- Added option to change the Celery execution pool.
- Added support for restricting admin access to multiple subnets [#481](https://github.com/openwisp/ansible-openwisp2/issues/481) [#518](https://github.com/openwisp/ansible-openwisp2/issues/518).
- Introduced new variable `openwisp2_inventory_hostname_localhost`.

### Changes

- Added default sqlite timeout (10 seconds).

#### Dependencies

- Upgraded to OpenWISP Users 1.2.x (see [change log](https://github.com/openwisp/openwisp-users/releases/tag/1.2.0))
- Upgraded to OpenWISP Controller 1.2.x (see [change log](https://github.com/openwisp/openwisp-controller/releases/tag/1.2.0))
- Upgraded to OpenWISP Monitoring 1.2.x (see [change log](https://github.com/openwisp/openwisp-monitoring/releases/tag/1.2.0))
- Upgraded to OpenWISP Network Topology 1.2.x (see [change log](https://github.com/openwisp/openwisp-network-topology/releases/tag/1.2.0))
- Upgraded to OpenWISP Firmware Upgrader 1.2.x (see [change log](https://github.com/openwisp/openwisp-firmware-upgrader/releases/tag/1.2.0))
- Upgraded to OpenWISP RADIUS 1.2.x (see [change
  log](https://github.com/openwisp/openwisp-radius/releases/tag/1.2.0))
- Bumped `django-cors-headers>=4.9.0,<4.10.0`
- Bumped `ansible-core>=2.15,<2.19`.
- Bumped `channels_redis>=4.3.0,<4.4.0`.
- Bumped `django-redis>=6.0.0,<6.1.0`.
- Bumped `django-pipeline>=4.1.0,<4.2.0`.
- Bumped `uwsgi>=2.0.30,<2.1.0`.
- Switched from `django-celery-email` to `django-celery-email-reboot` [#477](https://github.com/openwisp/ansible-openwisp2/issues/477).
- Added support for Debian 13.
- Dropped support for Ubuntu 20.04.

### Bugfixes

- Fixed `Restart freeradius` handler to properly restart the FreeRADIUS service instead of only ensuring it is running.
- Ensured Django templates from OpenWISP extensions take precedence over those from other apps.
- Moved OpenWISP version to a separate file to prevent circular imports.

## Version 24.11.1 [2024-11-27]

### Bugfixes

- Updated ``__openwisp_version__`` to ``24.11.1``.

## Version 24.11.0 [2024-11-26]

### Features

- Added support for Django CORS
- Allowed deploying [WPA Enterprise 2 EAP-TTLS-PAP](https://openwisp.io/docs/stable/ansible/user/deploying-wpa-eap-ttls-pap.html)
- Added a task to add `inventory_hostname` to `/etc/hosts`
- Added websocket routes for network topology
- Added `openwisp2_websocket_extra_routes` variable to configure websocket
  routes
- Added `openwisp2_daphne_install` variable to allow disabling Daphne
- Added `freeradius_openwisp_site_listen_ipaddr` variable to configure
  FreeRADIUS listen address
- Added `openwisp2_monitoring_default_retention_policy` variable to configure
  the default retention policy for monitoring metrics
- Added `openwisp2_uwsgi_extra_conf` variable to configure extra uWSGI
  parameters
- Added `openwisp2_email_timeout` variable to set the [default email
  timeout](https://docs.djangoproject.com/en/4.2/ref/settings/#email-timeout)
- Added variables `openwisp2_users_user_password_expiration` and
  `openwisp2_users_staff_user_password_expiration` to configure password
  expiration settings
- Added the `openwisp2_celerybeat` variable to allow disabling the CeleryBeat
  worker
- Introduced a consent mechanism for the [collection of usage
  metrics](https://openwisp.io/docs/stable/utils/user/metric-collection.html)

### Changes

- Upgraded to OpenWISP Users 1.1.x (see [change log](https://github.com/openwisp/openwisp-users/releases/tag/1.1.0))
- Upgraded to OpenWISP Controller 1.1.x (see [change log](https://github.com/openwisp/openwisp-controller/releases/tag/1.1.0))
- Upgraded to OpenWISP Monitoring 1.1.x (see [change log](https://github.com/openwisp/openwisp-monitoring/releases/tag/1.1.0))
- Upgraded to OpenWISP Network Topology 1.1.x (see [change log](https://github.com/openwisp/openwisp-network-topology/releases/tag/1.1.0))
- Upgraded to OpenWISP Firmware Upgrader 1.1.x (see [change log](https://github.com/openwisp/openwisp-firmware-upgrader/releases/tag/1.1.0))
- Upgraded to OpenWISP RADIUS 1.1.x (see [change log](https://github.com/openwisp/openwisp-radius/releases/tag/1.1.0))
- Upgraded to FreeRADIUS 3.2
- **Backward incompatible change**:
  `openwisp2_radius_delete_old_radiusbatch_users` variable now expects days
  instead of months
- Increased the *prefetch multiplier* for `network` and `monitoring` Celery
  workers to `10`
- Updated URLs to support cloud backends for private storage
- Removed the SQL module from the default FreeRADIUS site
- Changed the default value of the `openwisp2_radius_cleanup_stale_radacct`
  variable to `1`
- Added support for Debian 12
- Added support for Ubuntu 24.04
- Dropped support for Debian 10
- Dropped support for Ubuntu 18.04
- Dropped support for Python 3.7

### Bugfixes

- Implemented efficient reloading of supervisor services
- Included `allowed_hostnames` in the NGINX Content-Security-Policy.

## Version 22.05.3 [2023-02-21]

- Updated source for Stouts.postfix role dependency
- Fix: updated openssl command syntax

## Version 22.05.2 [2022-10-18]

- Removed sql module from default freeradius site which was generating errors
- Fixed ``openwisp2_should_install_python_37`` false test
- Fixed installation of Python 3.7 on old systems
- Fixed installation of freeradius on Ubuntu 22.04.1

## Version 22.05.1 [2022-05-30]

- Fixed redis installation issue on some Ubuntu versions

## Version 22.05 [2022-05-12]

### Changes

- Upgraded to OpenWISP Users 1.0.x (see [change log](https://github.com/openwisp/openwisp-users/releases/tag/1.0.0))
- Upgraded to OpenWISP Controller 1.0.x (see [change log](https://github.com/openwisp/openwisp-controller/releases/tag/1.0.0))
- Upgraded to OpenWISP Network Topology 1.0.x (see [change log](https://github.com/openwisp/openwisp-network-topology/releases/tag/1.0.0))
- Upgraded to OpenWISP Firmware Upgrader 1.0.x (see [change log](https://github.com/openwisp/openwisp-firmware-upgrader/releases/tag/1.0.0))
- **Backward incompatible change**: simplified installation of
  custom modules, the variables with `_pip` suffix have been abandoned
  in favour of supplying the full version in the variables having
  `_version` suffix, for more information please see [[change!] Simplify installation of custom modules #193](https://github.com/openwisp/ansible-openwisp2/commit/3c651a0179ecd7881cd6f388ee4a7d0a8c5a7689)
- `openwisp2_firmware_upgrader_max_file_size` now sets
  `OPENWISP_FIRMWARE_UPGRADER_MAX_FILE_SIZE` in `settings.py` and
  updates `client_max_body_size` in nginx config.
- Added variable to configure daphne websocket timeout;
  this timeout value is also used for configuring the "group_expiry"
  of `CHANNEL_LAYERS`.
- Updated nginx SSL configuration:
  - Dropped TLSv1.0 and TLSv1.1 protocol
  - Updated cipher list
- Updated NGINX security headers
- Disabled nginx `server_tokens`
- Added django-celery-email as default email backend
- Added `django.contrib.humanize` to `INSTALLED_APPS`
- Moved geocoding check from django-loci to explicit task

### Features

- Added support for [OpenWISP Monitoring](https://openwisp.io/docs/user/monitoring.html)
- Added optional support for [OpenWISP RADIUS](https://openwisp.io/docs/user/radius.html)
- Added support for Ubuntu 22.04
- Added support for internationalization
- Added option to [deploy custom static files](https://github.com/openwisp/ansible-openwisp2#deploying-custom-static-content)
- Added support for [subnet division rule feature](https://openwisp.io/docs/user/subnet-division-rules.html)
- Added the [OpenWISP Users authentication backend](https://github.com/openwisp/openwisp-users#authentication-backend) (enabled by default)
- Added sesame default configuration
- Allow specifying Django version
- Added uWSGI listen option

### Bugfixes

- Added handler for removing celerybeat-schedule.db whenever
  there's a change to the python code
- Updated celery supervisor config to support Celery 5
- Fixed support for Ubuntu 18.04
  - the role will install Python 3.7 if Python version < 3.7 is found
  - pinned setuptools~=59.6.0
- Fixed uWSGI OSError
