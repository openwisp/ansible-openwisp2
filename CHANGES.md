# Change log

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
