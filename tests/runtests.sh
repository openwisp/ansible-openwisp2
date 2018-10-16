#!/bin/bash
set -e -x

# Download snippet
printf "Downloading common tests shim...\n"
wget -q -O ${PWD}/tests/test.sh https://gitlab.com/snippets/1751673/raw
chmod +x ${PWD}/tests/test.sh

# Run tests
${PWD}/tests/test.sh

# Check OpenWISP is running
docker exec "${container_id}" curl --insecure -s --head https://localhost/admin/login/?next=/admin/ \
 | sed -n "1p" | grep -q "200" \
 && (printf "Status code 200 test: pass\n" && exit 0) \
 || (printf "Status code 200 test: fail\n"; \
 docker exec "${container_id}" sh -c "tail -n 500/opt/openwisp2/log/*.log" \
 && exit 1)

# Check redis is running 
sudo docker exec "${container_id}" systemctl status redis-server \
 | grep "Active: active (running)" \
 || sudo docker exec "${container_id}" systemctl status redis \
 | grep "Active: active (running)" \
 && (printf "redis test: pass\n" && exit 0) \
 || (printf "redis test: failed\n"; exit 1)
