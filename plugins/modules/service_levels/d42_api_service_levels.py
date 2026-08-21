#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_service_levels
short_description: Manage Device42 service levels
description:
    - Create Device42 service levels.
    - Supports C(POST /api/1.0/service_level/).
    - The Device42 API does not provide update or delete endpoints for service levels.
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
    name:
        description:
            - Name of the service level.
            - Required.
        required: true
        type: str
"""

EXAMPLES = r"""
- name: Create service level
    xbh03.device42.service_levels.d42_service_levels:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        name: Decommissioned

- name: Create service level using basic auth
    xbh03.device42.service_levels.d42_service_levels:
        host: device42.example.internal
        userid: admin
        password: secret123
        name: Production
"""

RETURN = r"""
api_service_level:
    description: Matching service level entry after create, or existing entry if already present.
    type: dict
    returned: success
response:
    description: Raw response from Device42 create operation.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.service_levels.d42_service_levels import (
        d42_service_levels,
)


def _find_service_level(helper, name):
        payload = helper.d42_get_service_levels()
        entries = payload if isinstance(payload, list) else []
        for entry in entries:
                if str(entry.get("name")) == str(name):
                        return entry
        return None


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
                name=dict(type="str", required=True),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_service_levels(
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

        name = module.params["name"]
        existing = _find_service_level(helper, name=name)

        if existing is not None:
                result["api_service_level"] = existing
                result["msg"] = "Service level already present"
                module.exit_json(**result)

        result["changed"] = True

        if module.check_mode:
                result["msg"] = "Service level would be created"
                module.exit_json(**result)

        response = helper.d42_post_service_level(name=name)
        result["response"] = response
        result["api_service_level"] = _find_service_level(helper, name=name)
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
