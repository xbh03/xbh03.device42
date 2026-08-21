#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_appcomps_info
short_description: Get Device42 application components
description:
    - Retrieve application components from Device42.
    - If C(appcomp_id) is provided, returns a specific application component by ID.
    - Otherwise returns application components with optional filters.
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
    appcomp_id:
        description:
            - Application component ID.
            - When set, the module retrieves only that component.
        required: false
        type: int
    device_id:
        description:
            - Filter by device ID.
            - Ignored when C(appcomp_id) is set.
        required: false
        type: int
    device:
        description:
            - Filter by device name.
            - Ignored when C(appcomp_id) is set.
        required: false
        type: str
    name:
        description:
            - Partial name filter for application components.
            - Ignored when C(appcomp_id) is set.
        required: false
        type: str
    resource_id:
        description:
            - Filter by resource ID.
            - Ignored when C(appcomp_id) is set.
        required: false
        type: int
    category_id:
        description:
            - Filter by application category ID.
            - Ignored when C(appcomp_id) is set.
        required: false
        type: int
    include_cols:
        description:
            - Comma-separated list of columns to include in the response.
            - Ignored when C(appcomp_id) is set.
        required: false
        type: str
    category:
        description:
            - Filter by application category.
            - Ignored when C(appcomp_id) is set.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all Device42 application components
    xbh03.device42.d42_api_appcomps_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get Device42 application components filtered by category
    xbh03.device42.d42_api_appcomps_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        category: Application Layer
        include_cols: custom_fields,depends_on,dependent,device,category,tags

- name: Get specific Device42 application component by ID
    xbh03.device42.d42_api_appcomps_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        appcomp_id: 15
"""

RETURN = r"""
api_appcomps:
    description: Raw response from Device42 application components endpoint.
    type: dict
    returned: when C(appcomp_id) is not set
    sample: |
        appcomps:
            - appcomp_id: 33
                appcomp_url: /api/1.0/appcomps/33/
                name: Device42 Production
api_appcomp:
    description: Raw response from Device42 specific application component endpoint.
    type: dict
    returned: when C(appcomp_id) is set
    sample: |
        appcomp_id: 15
        name: VMWare Farm
        device: USNHCTVMWPROD
        depends_on: Apache Tomcat Server
        dependent: mobileapp.com - prodserver-001
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.application_components.d42_appcomps import (
        d42_appcomps,
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
                appcomp_id=dict(type="int", required=False),
                device_id=dict(type="int", required=False),
                device=dict(type="str", required=False),
                name=dict(type="str", required=False),
                resource_id=dict(type="int", required=False),
                category_id=dict(type="int", required=False),
                include_cols=dict(type="str", required=False),
                category=dict(type="str", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_appcomps(
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

        if module.params["appcomp_id"] is not None:
                api_appcomp = helper.d42_get_appcomp_by_id(appcomp_id=module.params["appcomp_id"])
                result["api_appcomp"] = api_appcomp
        else:
                api_appcomps = helper.d42_get_appcomps(
                        device_id=module.params["device_id"],
                        device=module.params["device"],
                        name=module.params["name"],
                        resource_id=module.params["resource_id"],
                        category_id=module.params["category_id"],
                        include_cols=module.params["include_cols"],
                        category=module.params["category"],
                )
                result["api_appcomps"] = api_appcomps

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
