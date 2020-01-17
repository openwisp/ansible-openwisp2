#!/bin/bash

# Exit on any individual command failure.
set -e

# Pretty colors.
red="\033[0;31m"
green="\033[0;32m"
neutral="\033[0m"

timestamp=$(date +%s)

# Allow environment variables to override defaults.
distro=${distro:-"centos:7"}
playbook=${playbook:-"test.yml"}
ansible_opts=${ansible_opts:-"ansible_python_interpreter=/usr/bin/python"}
role_dir=${role_dir:-"$PWD"}
cleanup=${cleanup:-"true"}
container_id=${container_id:-$timestamp}
test_idempotence=${test_idempotence:-"true"}

## Set up vars for Docker setup.
# CentOS 7
if [ $distro = "centos:7" ]; then
  init="/usr/lib/systemd/systemd"
  opts="--privileged --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro"
# Ubuntu 18.04
elif [ $distro = "ubuntu:18.04" ]; then
  init="/lib/systemd/systemd"
  opts="--privileged --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro"
# Ubuntu 16.04
elif [ $distro = "ubuntu:16.04" ]; then
  init="/lib/systemd/systemd"
  opts="--privileged --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro"
# Debian 10
elif [ $distro = "debian:10" ]; then
  init="/lib/systemd/systemd"
  opts="--privileged --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro"
# Debian 9
elif [ $distro = "debian:9" ]; then
  init="/lib/systemd/systemd"
  opts="--privileged --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro"
# Fedora 27
elif [ $distro = "fedora:27" ]; then
  init="/usr/lib/systemd/systemd"
  opts="--privileged --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro"
# Fedora 28
elif [ $distro = "fedora:28" ]; then
  init="/usr/lib/systemd/systemd"
  opts="--privileged --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro"
  ansible_opts="ansible_python_interpreter=/usr/bin/python3"
fi

# Run the container using the supplied OS
printf ${green}"Starting Docker container: registry.gitlab.com/ninuxorg/docker/ansible-$distro"${neutral}"\n"
docker pull registry.gitlab.com/ninuxorg/docker/ansible-$distro
docker run --detach --volume="$role_dir":/etc/ansible/roles/role_under_test:rw --name $container_id $opts registry.gitlab.com/ninuxorg/docker/ansible-$distro $init

printf "\n"

# Install requirements if `requirements.yml` is present
if [ -f "$role_dir/tests/requirements.yml" ]; then
  printf ${green}"Requirements file detected; installing dependencies"${neutral}"\n"
  docker exec --tty $container_id env TERM=xterm ansible-galaxy install -r /etc/ansible/roles/role_under_test/tests/requirements.yml
fi

printf "\n"

# Test Ansible syntax.
printf ${green}"Checking Ansible playbook syntax"${neutral}
docker exec --tty $container_id env TERM=xterm ansible-playbook /etc/ansible/roles/role_under_test/tests/$playbook --syntax-check

printf "\n"

# Run Ansible playbook
printf ${green}"Running command: docker exec $container_id env TERM=xterm ansible-playbook /etc/ansible/roles/role_under_test/tests/$playbook"${neutral}
docker exec $container_id env TERM=xterm env ANSIBLE_FORCE_COLOR=1 ansible-playbook /etc/ansible/roles/role_under_test/tests/$playbook -e $ansible_opts

# Check OpenWISP is running
echo "Launching OpenWISP tests"
docker exec "${container_id}" curl --insecure -s --head https://localhost/admin/login/?next=/admin/ \
 | sed -n "1p" | grep -q "200" \
 && (printf "Status code 200 test: pass\n" && exit 0) \
 || (printf "Status code 200 test: fail\n"; \
 docker exec "${container_id}" sh -c "tail -n 500/opt/openwisp2/log/*.log" \
 && exit 1)

# Check redis is running
echo "Checking if redis is running"
docker exec "${container_id}" systemctl status redis-server \
 | grep "Active: active (running)" \
 || docker exec "${container_id}" systemctl status redis \
 | grep "Active: active (running)" \
 && (printf "redis test: pass\n" && exit 0) \
 || (printf "redis test: failed\n"; exit 1)

# we only run a specific subset of tests which should always work
# independently of how the openwisp2 instance is configured
docker exec "${container_id}" \
    /opt/openwisp2/env/bin/python /opt/openwisp2/manage.py test --keepdb \
        openwisp_controller.pki \
        openwisp_controller.config.tests.test_config \
        openwisp_controller.config.tests.test_controller \
        openwisp_controller.config.tests.test_device \
        openwisp_controller.config.tests.test_tag \
        openwisp_controller.config.tests.test_template \
        openwisp_controller.config.tests.test_views \
        openwisp_controller.config.tests.test_vpn \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_preview_device \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_device_preview_button \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_template_preview_button \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_vpn_preview_button \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_device_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_device_organization_fk_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_device_organization_fk_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_device_templates_m2m_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_template_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_template_organization_fk_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_template_vpn_fk_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_vpn_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_vpn_organization_fk_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_vpn_ca_fk_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_vpn_cert_fk_queryset \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_changelist_recover_deleted_button \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_recoverlist_operator_403 \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_device_template_filter \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_device_contains_default_templates_js \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_template_not_contains_default_templates_js \
        openwisp_controller.config.tests.test_admin.TestAdmin.test_vpn_not_contains_default_templates_js \
        openwisp_controller.geo.tests.test_channels \
        openwisp_controller.geo.tests.test_api

if [ "$test_idempotence" = true ]; then
  # Run Ansible playbook again (idempotence test).
  printf ${green}"Running playbook again: idempotence test"${neutral}
  idempotence=$(mktemp)
  docker exec $container_id  env TERM=xterm env ANSIBLE_FORCE_COLOR=1 ansible-playbook /etc/ansible/roles/role_under_test/tests/$playbook -e $ansible_opts --diff | tee -a $idempotence
  tail $idempotence \
    | grep -q "changed=0.*failed=0" \
    && (printf ${green}"Idempotence test: pass"${neutral}"\n") \
    || (printf ${red}"Idempotence test: fail"${neutral}"\n$(tail $idempotence)")
fi

# Remove the Docker container (if configured).
if [ "$cleanup" = true ]; then
  printf "Removing Docker container...\n"
  docker rm -f $container_id
fi
