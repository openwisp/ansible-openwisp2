#!/usr/bin/env python
"""
Prepares fixture file that will be imported with loaddata
"""
import json
import uuid

substitutions = [
    ('"django_netjsonconfig"', '"config"'),
    ('"django_netjsonconfig.config"', '"config.config"'),
    ('"django_netjsonconfig.vpn"', '"config.vpn"'),
    ('"django_netjsonconfig.template"', '"config.template"'),
    ('\"django_netjsonconfig.config\"', '"config.config"'),
    ('\"django_netjsonconfig.vpn\"', '"config.vpn"'),
    ('\"django_netjsonconfig.template\"', '"config.template"'),
    ('"django_x509"', '"pki"'),
    ('"django_x509.ca"', '"pki.ca"'),
    ('"django_x509.cert"', '"pki.cert"'),
    ('"auth.user"', '"openwisp_users.user"'),
    ('{"app_label": "auth", "model": "user"}', '{"app_label": "openwisp_users", "model": "user"}')
]
contents = open('pre_multitenancy_migration.json').read()

for substitution in substitutions:
    contents = contents.replace(substitution[0], substitution[1])

default_org_id = '{{ openwisp2_default_organization_id }}'
data = json.loads(contents)

new_data = []

for row in data:
    # add organization relation to openwisp2 models
    if 'config.' in row['model'] or 'pki.' in row['model']:
        row['fields']['organization'] = default_org_id
    # generate new uuid for users
    elif row['model'] == 'openwisp_users.user':
        row['pk'] = uuid.uuid4().hex
    # drop data which references old primary keys
    # that are being changed in this procedure
    # we can remove this data because is not strictly
    # essential to OpenWISP 2 functioning and it would
    # require too much work to migrate
    elif row['model'] in ['admin.logentry',
                          'reversion.revision',
                          'reversion.version',
                          'sessions.session']:
        continue
    new_data.append(row)

# create default organization configuration settings
# contains the shared_secret attribute which is
# required for auto registration
organization_settings = {
    "model": "config.organizationconfigsettings",
    "pk": default_org_id,
    "fields": {
        "organization": default_org_id,
        "registration_enabled": True,
        "shared_secret": "{{ openwisp2_shared_secret|default('<CHANGE-ME>') }}"
    }
}
new_data.append(organization_settings)

contents = json.dumps(new_data, indent=4, sort_keys=True)

result = open('post_multitenancy_migration.json', 'w')
result.write(contents)
result.write('\n')
result.close()
