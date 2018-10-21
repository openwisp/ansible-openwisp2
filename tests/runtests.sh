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
