#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_vendors_info
short_description: Get Device42 vendors
description:
    - Retrieve vendors from Device42.
    - Supports optional filter by vendor name.
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
            - Vendor name filter.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all Device42 vendors
    xbh03.device42.d42_api_vendors_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get Device42 vendor by name
    xbh03.device42.d42_api_vendors_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        name: Acer Incorporated
"""

RETURN = r"""
api_vendors:
    description: Raw response from Device42 vendors endpoint.
    type: dict
    returned: success
    sample: |
        vendors:
            - name: Acer Incorporated
                vendor_id: "10"
                account_no: "1234"
                contact_info: "8004553432"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.vendors.d42_vendors import (
        d42_vendors,
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
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_vendors(
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

        api_vendors = helper.d42_get_vendors(name=module.params["name"])
        result["api_vendors"] = api_vendors
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
