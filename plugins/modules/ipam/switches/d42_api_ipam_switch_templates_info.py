#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_switch_templates_info
short_description: Get Device42 IPAM switch templates
description:
    - Retrieve switch templates from Device42 IPAM.
    - Supports C(GET /api/1.0/switch_templates/).
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
- name: Get all switch templates
    xbh03.device42.ipam.switches.d42_api_ipam_switch_templates_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get all switch templates with basic auth
    xbh03.device42.ipam.switches.d42_api_ipam_switch_templates_info:
        host: device42.example.internal
        userid: admin
        password: secret123
"""

RETURN = r"""
ipam_switch_templates:
    description: Raw response from Device42 switch templates endpoint.
    type: list
    returned: success
    sample:
        - switch_type: Modular/Distributed (Single)
          template_id: 2
          template_name: m3
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.switches.d42_ipam_switch_templates import (
    d42_ipam_switch_templates,
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

    helper = d42_ipam_switch_templates(
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

    result["ipam_switch_templates"] = helper.d42_get_switch_templates()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
