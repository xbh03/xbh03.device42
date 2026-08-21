#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_healthstatus_info
short_description: Get Device42 health status
description:
    - Retrieve Device42 appliance health status.
    - Endpoint uses health status port C(4343) by default.
version_added: "0.1.0"
author:
    - Francesco Zoino <f.zoino@atdatenschutz.ch>
options:
    host:
        description:
            - Device42 host or IP.
        required: true
        type: str
    client_key:
        description:
            - Device42 API client key used to authenticate.
        required: true
        type: str
    client_secret_key:
        description:
            - Device42 API client secret key used to authenticate.
        required: true
        type: str
    proto:
        description:
            - Protocol used to connect to Device42.
        required: false
        type: str
        default: https
        choices:
            - http
            - https
    port:
        description:
            - Device42 health endpoint port.
        required: false
        type: int
        default: 4343
    sslverify:
        description:
            - Validate SSL certificates.
        required: false
        type: bool
        default: true
    debug:
        description:
            - Enable debug behavior in helper utilities.
        required: false
        type: bool
        default: false
    full:
        description:
            - Request full health stats set.
            - Allowed values are C(yes) and C(no).
        required: false
        type: str
        choices:
            - yes
            - no
"""

EXAMPLES = r"""
- name: Get Device42 health status
    xbh03.device42.d42_api_healthstatus_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get full Device42 health status
    xbh03.device42.d42_api_healthstatus_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        full: yes

- name: Get Device42 health status with custom health port
    xbh03.device42.d42_api_healthstatus_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        port: 4343
        full: no
"""

RETURN = r"""
health_status:
    description: Raw response from Device42 health status endpoint.
    type: dict
    returned: success
    sample: |
        version: 18.10.00.1690226275
        backup_status:
            - id: 1
                job_name: Demo Backup
                status: Good @  2019-01-10 18:51:31
        cpu_used_percent: "2.51904"
        dbsize: 84 MB
        disk_used_percent: "8"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.health_status.d42_health_status import (
        d42_health_status,
)


def run_module():
        module_args = dict(
                host=dict(type="str", required=True),
                client_key=dict(type="str", required=False),
                client_secret_key=dict(type="str", required=False, no_log=True),
                userid=dict(type="str", required=False),
                password=dict(type="str", required=False, no_log=True),
                proto=dict(type="str", required=False, default="https", choices=["http", "https"]),
                port=dict(type="int", required=False, default=4343),
                sslverify=dict(type="bool", required=False, default=True),
                debug=dict(type="bool", required=False, default=False),
                full=dict(type="str", required=False, choices=["yes", "no"]),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_health_status(
                host=module.params["host"],
                module=module,
                result=result,
                sslverify=module.params["sslverify"],
                client_key=module.params["client_key"],
                client_secret_key=module.params["client_secret_key"],
                userid=module.params["userid"],
                password=module.params["password"],
                proto=module.params["proto"],
                port=module.params["port"],
                debug=module.params["debug"],
        )

        health_status = helper.d42_get_health_stats(full=module.params["full"])
        result["health_status"] = health_status
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
