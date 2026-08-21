#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_appgroup_calc_rule_info
short_description: Get Device42 application group calculation information
description:
    - Retrieve Device42 application group calculation rules.
    - Retrieve a single application group calculation rule by ID.
    - Retrieve items associated with a specific application group.
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
    rule_id:
        description:
            - Application group calculation rule ID.
            - Uses endpoint C(/api/2.0/app_group_calc_rule/{id}/).
        required: false
        type: int
    rule_name:
        description:
            - Full or partial name filter for calculation rules.
            - Uses endpoint C(/api/2.0/app_group_calc_rule/).
        required: false
        type: str
    application_group_id:
        description:
            - Application group ID.
            - Uses endpoint C(/api/2.0/application_group/{id}/items).
        required: false
        type: int
"""

EXAMPLES = r"""
- name: Get all Device42 application group calculation rules
    xbh03.device42.d42_api_appgroup_calc_rule_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get Device42 application group calculation rules filtered by name
    xbh03.device42.d42_api_appgroup_calc_rule_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        rule_name: Custom Rule

- name: Get specific Device42 application group calculation rule by ID
    xbh03.device42.d42_api_appgroup_calc_rule_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        rule_id: 1

- name: Get items for a specific application group
    xbh03.device42.d42_api_appgroup_calc_rule_info:
        host: device42.example.internal
        userid: admin
        password: secret123
        application_group_id: 12
"""

RETURN = r"""
api_appgroup_calc_rules:
    description: Raw response from Device42 application group calculation rules endpoint.
    type: dict
    returned: when listing calculation rules
api_appgroup_calc_rule:
    description: Raw response from Device42 specific application group calculation rule endpoint.
    type: dict
    returned: when C(rule_id) is provided
api_application_group_items:
    description: Raw response from Device42 application group items endpoint.
    type: dict
    returned: when C(application_group_id) is provided
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.application_groups.d42_appgroup_calc_rule import (
    d42_appgroup_calc_rule,
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
        rule_id=dict(type="int", required=False),
        rule_name=dict(type="str", required=False),
        application_group_id=dict(type="int", required=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    selected_endpoints = 0
    if module.params["rule_id"] is not None:
        selected_endpoints += 1
    if module.params["application_group_id"] is not None:
        selected_endpoints += 1

    if selected_endpoints > 1:
        module.fail_json(
            msg=(
                "rule_id and application_group_id are different endpoints. "
                "Use only one endpoint selector per request."
            )
        )

    rule_helper = d42_appgroup_calc_rule(
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

    if module.params["rule_id"] is not None:
        result["api_appgroup_calc_rule"] = rule_helper.d42_get_appgroup_calc_rule_by_id(
            rule_id=module.params["rule_id"]
        )
        module.exit_json(**result)

    if module.params["application_group_id"] is not None:
        result["api_application_group_items"] = rule_helper.d42_get_application_group_items(
            application_group_id=module.params["application_group_id"]
        )
        module.exit_json(**result)

    result["api_appgroup_calc_rules"] = rule_helper.d42_get_appgroup_calc_rules(name=module.params["rule_name"])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
