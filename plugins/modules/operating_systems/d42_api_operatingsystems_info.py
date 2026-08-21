#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_operatingsystems_info
short_description: Get Device42 operating systems
description:
    - Retrieve information about operating systems from Device42.
    - Supports list endpoint C(/api/1.0/operatingsystems/) and specific endpoint C(/api/1.0/operatingsystems/{id}/).
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
            - Device42 API port.
        required: false
        type: int
        default: 443
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
    name:
        description:
            - Filter by OS name.
        required: false
        type: str
    manufacturer:
        description:
            - Filter by OS manufacturer.
        required: false
        type: str
    category:
        description:
            - Filter by OS category (for example Linux, Windows).
        required: false
        type: str
    query_type:
        description:
            - Select which operating systems endpoint to query.
            - Use C(list) for C(/api/1.0/operatingsystems/).
            - Use C(specific) for C(/api/1.0/operatingsystems/{id}/).
        required: false
        type: str
        default: list
        choices:
            - list
            - specific
    operating_system_id:
        description:
            - Operating system ID for specific endpoint.
        required: false
        type: int
"""

EXAMPLES = r"""
- name: Get all Device42 operating systems
    xbh03.device42.d42_api_operatingsystems_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter operating systems by name
    xbh03.device42.d42_api_operatingsystems_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        name: Microsoft Windows 7 Professional

- name: Filter operating systems by manufacturer and category
    xbh03.device42.d42_api_operatingsystems_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        manufacturer: Juniper
        category: Linux

- name: Get specific operating system by ID
    xbh03.device42.d42_api_operatingsystems_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: specific
        operating_system_id: 1
"""

RETURN = r"""
operating_systems:
    description: Raw response from Device42 operating systems endpoint.
    type: dict
    returned: when query_type=list
    sample: |
        operatingsystems:
            - id: 1
                name: Microsoft Windows 7 Professional
                manufacturer: ""
                category: ""
operating_system:
    description: Raw response from Device42 specific operating system endpoint.
    type: dict
    returned: when query_type=specific
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.operating_systems.d42_operating_systems import (
        d42_operating_systems,
)


def run_module():
        module_args = dict(
                host=dict(type="str", required=True),
                client_key=dict(type="str", required=False),
                client_secret_key=dict(type="str", required=False, no_log=True),
                userid=dict(type="str", required=False),
                password=dict(type="str", required=False, no_log=True),
                proto=dict(type="str", required=False, default="https", choices=["http", "https"]),
                port=dict(type="int", required=False, default=443),
                sslverify=dict(type="bool", required=False, default=True),
                debug=dict(type="bool", required=False, default=False),
                name=dict(type="str", required=False),
                manufacturer=dict(type="str", required=False),
                category=dict(type="str", required=False),
                query_type=dict(type="str", required=False, default="list", choices=["list", "specific"]),
                operating_system_id=dict(type="int", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_operating_systems(
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

        query_type = module.params["query_type"]

        if query_type == "specific":
                if module.params["operating_system_id"] is None:
                        module.fail_json(msg="operating_system_id is required when query_type=specific.")

                result["operating_system"] = helper.d42_get_operating_system_by_id(
                        operating_system_id=module.params["operating_system_id"],
                )
                module.exit_json(**result)

        operating_systems = helper.d42_get_operating_systems(
                name=module.params["name"],
                manufacturer=module.params["manufacturer"],
                category=module.params["category"],
        )

        result["operating_systems"] = operating_systems
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
