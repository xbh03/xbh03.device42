#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_appcomptemplate_info
short_description: Get Device42 application component templates
description:
    - Retrieve application component templates from Device42.
    - Supports all documented GET filters for C(/api/2.0/appcomp_templates/).
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
            - Filter by application component template ID.
        required: false
        type: int
    name:
        description:
            - Filter by application component template name.
        required: false
        type: str
    enabled:
        description:
            - Filter by template status.
            - Accepted values are C(yes) and C(no).
        required: false
        type: str
    rule_type:
        description:
            - Filter by target environment of the template.
            - Accepted values are C(Windows) and C(*Nix).
        required: false
        type: str
    rule_type_id:
        description:
            - Filter by rule type ID.
        required: false
        type: int
    service_id:
        description:
            - Filter by associated service ID.
        required: false
        type: int
    service_listening_port:
        description:
            - Filter by service listening port.
        required: false
        type: int
    app_name_pattern:
        description:
            - Filter by application name pattern.
        required: false
        type: str
    related_services_listening_port:
        description:
            - Filter by related services listening port.
        required: false
        type: int
    config_file_location:
        description:
            - Filter by config file location.
        required: false
        type: str
    traverse_subdirectories:
        description:
            - Filter by traverse subdirectories option.
            - Accepted values are C(yes) and C(no).
        required: false
        type: str
    filename_filter:
        description:
            - Filter by file name.
        required: false
        type: str
    application_category_id:
        description:
            - Filter by application category ID.
        required: false
        type: int
    application_category_name:
        description:
            - Filter by application category name.
        required: false
        type: str
    what:
        description:
            - Filter by impact target description.
        required: false
        type: str
    customer_id:
        description:
            - Filter by customer ID.
        required: false
        type: int
    customer:
        description:
            - Filter by customer name.
        required: false
        type: str
    last_changed_lt:
        description:
            - Filter by last changed date less than C(YYYY-MM-DD).
        required: false
        type: str
    last_changed_gt:
        description:
            - Filter by last changed date greater than C(YYYY-MM-DD).
        required: false
        type: str
    service_cmd_arg_match:
        description:
            - Filter by command argument match value.
        required: false
        type: str
    tags:
        description:
            - Filter by tags.
        required: false
        type: str
    match_type:
        description:
            - Filter by match type.
            - Accepted values are C(Text) and C(Regular Expression).
        required: false
        type: str
    match_type_id:
        description:
            - Filter by match type ID.
            - Use C(0) for Text and C(1) for Regular Expression.
        required: false
        type: int
"""

EXAMPLES = r"""
- name: Get all Device42 application component templates
    xbh03.device42.d42_api_appcomptemplate_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get templates using username and password auth
    xbh03.device42.d42_api_appcomptemplate_info:
        host: device42.example.internal
        userid: admin
        password: secret123

- name: Filter templates by name, status and environment
    xbh03.device42.d42_api_appcomptemplate_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        name: App-Comp-Template-T2
        enabled: yes
        rule_type: Windows

- name: Get a specific template by ID filter
    xbh03.device42.d42_api_appcomptemplate_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        template_id: 13
"""

RETURN = r"""
api_appcomp_templates:
    description: Raw response from Device42 application component templates endpoint.
    type: dict
    returned: always
    sample:
        app_component_templates:
            - id: 13
              name: App-Comp-Template-T2
              enabled: yes
              rule_type: Windows
              application_category_name: Application Layer
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.application_components.d42_appcomptemplate import (
        d42_appcomptemplate,
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
            enabled=dict(type="str", required=False),
            rule_type=dict(type="str", required=False),
            rule_type_id=dict(type="int", required=False),
            service_id=dict(type="int", required=False),
            service_listening_port=dict(type="int", required=False),
            app_name_pattern=dict(type="str", required=False),
            related_services_listening_port=dict(type="int", required=False),
            config_file_location=dict(type="str", required=False),
            traverse_subdirectories=dict(type="str", required=False),
            filename_filter=dict(type="str", required=False),
            application_category_id=dict(type="int", required=False),
            application_category_name=dict(type="str", required=False),
            what=dict(type="str", required=False),
            customer_id=dict(type="int", required=False),
            customer=dict(type="str", required=False),
            last_changed_lt=dict(type="str", required=False),
            last_changed_gt=dict(type="str", required=False),
            service_cmd_arg_match=dict(type="str", required=False),
            tags=dict(type="str", required=False),
            match_type=dict(type="str", required=False),
            match_type_id=dict(type="int", required=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    helper = d42_appcomptemplate(
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

    api_appcomp_templates = helper.d42_get_appcomp_templates(
            template_id=module.params["template_id"],
            name=module.params["name"],
            enabled=module.params["enabled"],
            rule_type=module.params["rule_type"],
            rule_type_id=module.params["rule_type_id"],
            service_id=module.params["service_id"],
            service_listening_port=module.params["service_listening_port"],
            app_name_pattern=module.params["app_name_pattern"],
            related_services_listening_port=module.params["related_services_listening_port"],
            config_file_location=module.params["config_file_location"],
            traverse_subdirectories=module.params["traverse_subdirectories"],
            filename_filter=module.params["filename_filter"],
            application_category_id=module.params["application_category_id"],
            application_category_name=module.params["application_category_name"],
            what=module.params["what"],
            customer_id=module.params["customer_id"],
            customer=module.params["customer"],
            last_changed_lt=module.params["last_changed_lt"],
            last_changed_gt=module.params["last_changed_gt"],
            service_cmd_arg_match=module.params["service_cmd_arg_match"],
            tags=module.params["tags"],
            match_type=module.params["match_type"],
            match_type_id=module.params["match_type_id"],
    )

    result["api_appcomp_templates"] = api_appcomp_templates
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
