#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_appgroup_calc_template_info
short_description: Get Device42 application group calculation templates
description:
    - Retrieve application group calculation templates from Device42.
    - If C(template_id) is provided, returns a specific template by ID.
    - Otherwise returns all templates with optional C(name) filter.
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
    template_id:
        description:
            - Application group calculation template ID.
            - When set, the module retrieves only that template.
        required: false
        type: int
    name:
        description:
            - Full or partial name filter for calculation templates.
            - Ignored when C(template_id) is set.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all Device42 application group calculation templates
    xbh03.device42.d42_api_appgroup_calc_template_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get templates with basic auth
    xbh03.device42.d42_api_appgroup_calc_template_info:
        host: device42.example.internal
        userid: admin
        password: secret123

- name: Get templates filtered by name
    xbh03.device42.d42_api_appgroup_calc_template_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        name: Custom Template

- name: Get specific template by ID
    xbh03.device42.d42_api_appgroup_calc_template_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        template_id: 1
"""

RETURN = r"""
api_appgroup_calc_templates:
    description: Raw response from Device42 application group calculation templates endpoint.
    type: dict
    returned: when C(template_id) is not set
    sample:
        total_count: 1
        templates:
            - id: 1
              name: Custom Template Name
              calculation_format: DOQL
api_appgroup_calc_template:
    description: Raw response from Device42 specific application group calculation template endpoint.
    type: dict
    returned: when C(template_id) is set
    sample:
        id: 1
        name: Custom Template Name
        calculation_format: DOQL
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.application_groups.d42_appgroup_calc_template import (
    d42_appgroup_calc_template,
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
        template_id=dict(type="int", required=False),
        name=dict(type="str", required=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    helper = d42_appgroup_calc_template(
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

    if module.params["template_id"] is not None:
        result["api_appgroup_calc_template"] = helper.d42_get_appgroup_calc_template_by_id(
            template_id=module.params["template_id"]
        )
    else:
        result["api_appgroup_calc_templates"] = helper.d42_get_appgroup_calc_templates(
            name=module.params["name"]
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
