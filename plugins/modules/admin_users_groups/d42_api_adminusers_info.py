#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_adminusers_info
short_description: Get Device42 admin users
description:
    - Retrieve admin users from Device42.
    - If C(user_id) is provided, returns a specific admin user by ID.
    - Otherwise returns the admin users list with optional filters.
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
    user_id:
        description:
            - Device42 admin user ID.
            - When set, the module retrieves only that admin user.
        required: false
        type: int
    username:
        description:
            - Filter admin users by username.
            - Ignored when C(user_id) is set.
        required: false
        type: str
    email:
        description:
            - Filter admin users by email address.
            - Ignored when C(user_id) is set.
        required: false
        type: str
    include_cols:
        description:
            - Comma-separated list of columns to include in the response.
            - Ignored when C(user_id) is set.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all Device42 admin users
    xbh03.device42.d42_api_adminusers_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get all Device42 admin users with username and password auth
    xbh03.device42.d42_api_adminusers_info:
        host: device42.example.internal
        userid: admin
        password: secret123

- name: Get Device42 admin users filtered by username
    xbh03.device42.d42_api_adminusers_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        username: JohnDoe
        include_cols: auth_type,is_active,is_staff,username,id,email,groups

- name: Get Device42 admin user by ID
    xbh03.device42.d42_api_adminusers_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        user_id: 125
"""

RETURN = r"""
api_adminusers:
    description: Raw response from Device42 admin users endpoint.
    type: dict
    returned: when C(user_id) is not set
    sample:
        adminusers:
            - id: 125
              username: JohnDoe
              email: JohnDoe@device42.com
              groups:
                - System Generated Read Only
                - GroupABC
              is_staff: true
              is_active: true
        total_count: 1
        limit: 1000
        offset: 0
api_adminuser:
    description: Raw response from Device42 specific admin user endpoint.
    type: dict
    returned: when C(user_id) is set
    sample:
        id: 125
        username: JohnDoe
        email: JohnDoe@device42.com
        groups:
            - System Generated Read Only
            - GroupABC
        is_staff: true
        is_active: true
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.admin_users_groups.d42_adminusers import (
        d42_adminusers,
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
            user_id=dict(type="int", required=False),
            username=dict(type="str", required=False),
            email=dict(type="str", required=False),
            include_cols=dict(type="str", required=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    helper = d42_adminusers(
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

    if module.params["user_id"] is not None:
        api_adminuser = helper.d42_get_adminuser_by_id(user_id=module.params["user_id"])
        result["api_adminuser"] = api_adminuser
    else:
        api_adminusers = helper.d42_get_adminusers(
                username=module.params["username"],
                email=module.params["email"],
                include_cols=module.params["include_cols"],
        )
        result["api_adminusers"] = api_adminusers

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
