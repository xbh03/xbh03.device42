#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_eoleos_info
short_description: Get Device42 OS EOL/EOS information
description:
    - Retrieve operating systems End of Life and End of Support information from Device42.
    - Uses C(/api/1.0/os_eoleos/).
version_added: "0.2.0"
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
        required: false
        type: str
    client_secret_key:
        description:
            - Device42 API client secret key used to authenticate.
        required: false
        type: str
    userid:
        description:
            - Device42 username used to authenticate.
        required: false
        type: str
    password:
        description:
            - Device42 password used to authenticate.
        required: false
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
"""

EXAMPLES = r"""
- name: Get OS EOL/EOS information
    xbh03.device42.operating_systems.d42_api_eoleos_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get OS EOL/EOS information using basic auth
    xbh03.device42.operating_systems.d42_api_eoleos_info:
        host: device42.example.internal
        userid: admin
        password: secret123
"""

RETURN = r"""
api_os_eoleos:
    description: Raw response from Device42 OS EOL/EOS endpoint.
    type: dict
    returned: success
    sample: |
        values:
            - id: 1
                os_id: 21
                os: Ubuntu
                version: 4.4.0-53-generic
                end_of_life: "2017-11-15"
                end_of_support: "2017-11-30"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.operating_systems.d42_eoleos import (
        d42_eoleos,
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
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_eoleos(
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

        result["api_os_eoleos"] = helper.d42_get_os_eoleos()
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
