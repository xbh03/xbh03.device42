#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_admingroups_info
short_description: Get Device42 admin groups
description:
    - Retrieve admin groups from Device42.
    - This module contains the read-only admin groups endpoints exposed by the helper.
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
            - Use together with C(client_secret_key) as an alternative to C(userid) and C(password).
        required: false
        type: str
    client_secret_key:
        description:
            - Device42 API client secret key used to authenticate.
            - Use together with C(client_key) as an alternative to C(userid) and C(password).
        required: false
        type: str
    userid:
        description:
            - Device42 username used to authenticate.
            - Use together with C(password) as an alternative to C(client_key) and C(client_secret_key).
        required: false
        type: str
    password:
        description:
            - Device42 password used to authenticate.
            - Use together with C(userid) as an alternative to C(client_key) and C(client_secret_key).
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
    include_cols:
        description:
            - Comma-separated list of extra columns to include in the response.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all Device42 admin groups
    xbh03.device42.d42_api_admingroups_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get Device42 admin groups with additional columns
    xbh03.device42.d42_api_admingroups_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        include_cols: permissions

- name: Get Device42 admin groups with username and password auth
    xbh03.device42.d42_api_admingroups_info:
        host: device42.example.internal
        userid: admin
        password: secret123
"""

RETURN = r"""
api_admingroups:
    description: Raw response from Device42 admin groups endpoint.
    type: dict
    returned: success
    sample: |
        admingroups:
            - id: 6
                name: System Generated Read, Add and Edit
                members:
                    - User1
                    - User2
        total_count: 1
        limit: 1000
        offset: 0
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.admin_users_groups.d42_admingroups import (
        d42_admingroups,
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
                include_cols=dict(type="str", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_admingroups(
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

        api_admingroups = helper.d42_get_admingroups(include_cols=module.params["include_cols"])

        result["api_admingroups"] = api_admingroups
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
