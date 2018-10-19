#!/bin/bash
set -e -x

docker exec "${container_id}" curl --insecure -s --head https://localhost/admin/login/?next=/admin/ \
| sed -n '1p' | grep -q '200' \
&& (echo 'Status code 200 test: pass' && exit 0) \
|| (echo 'Status code 200 test: fail'; docker exec "${container_id}" sh -c 'tail -n 500 /opt/openwisp2/log/*.log' && exit 1)
