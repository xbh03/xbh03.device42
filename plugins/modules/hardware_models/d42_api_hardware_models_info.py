#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_hardware_models_info
short_description: Get Device42 hardware models
description:
    - Retrieve hardware models from Device42.
    - Supports list endpoint C(/api/2.0/hardwares/) and specific endpoint C(/api/2.0/hardwares/{id}/).
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
    query_type:
        description:
            - Select which hardware models endpoint to query.
            - Use C(list) for C(/api/2.0/hardwares/).
            - Use C(specific) for C(/api/2.0/hardwares/{id}/).
        required: false
        type: str
        default: list
        choices:
            - list
            - specific
    hardware_id:
        description:
            - Hardware model ID.
            - Used as list filter or required when C(query_type=specific).
        required: false
        type: int
    name:
        description:
            - Filter by hardware model name.
        required: false
        type: str
    physicalsubtype_id:
        description:
            - Physical subtype ID.
        required: false
        type: int
    physicalsubtype:
        description:
            - Physical subtype name.
        required: false
        type: str
    size:
        description:
            - Filter by exact size.
        required: false
        type: str
    blade_size_id:
        description:
            - Blade size ID.
        required: false
        type: int
    blade_size:
        description:
            - Blade size.
        required: false
        type: str
    depth_id:
        description:
            - Depth ID.
        required: false
        type: int
    depth:
        description:
            - Depth name.
        required: false
        type: str
    width_ratio_id:
        description:
            - Width ratio ID.
        required: false
        type: int
    width_ratio:
        description:
            - Width ratio.
        required: false
        type: str
    part_number:
        description:
            - Filter by part number.
        required: false
        type: str
    network_device:
        description:
            - Filter by network device flag, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    blade_host:
        description:
            - Filter by blade host flag, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    watts:
        description:
            - Filter by watts.
        required: false
        type: int
    vendor_id:
        description:
            - Hardware model vendor ID.
        required: false
        type: int
    vendor:
        description:
            - Hardware model vendor name.
        required: false
        type: str
    custom_fields_and:
        description:
            - AND custom field filters, format C(key1:value1,key2:value2).
        required: false
        type: str
    custom_fields_or:
        description:
            - OR custom field filters, format C(key1:value1,key2:value2).
        required: false
        type: str
    device_id:
        description:
            - Filter by device ID.
        required: false
        type: int
    include_cols:
        description:
            - Return only specified columns, comma separated.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all hardware models
    xbh03.device42.hardware_models.d42_api_hardware_models_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter hardware models by vendor and subtype
    xbh03.device42.hardware_models.d42_api_hardware_models_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        vendor: APC Inc.
        physicalsubtype: Branch Circuit Power Meter

- name: Get specific hardware model by ID
    xbh03.device42.hardware_models.d42_api_hardware_models_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: specific
        hardware_id: 1
"""

RETURN = r"""
api_hardware_models:
    description: Raw response from Device42 hardware models list endpoint.
    type: dict
    returned: when query_type=list
    sample: |
        hardware_models:
            - hardware_id: 1
                name: PowerLogic
                vendor_id: 269
                watts: 1000
api_hardware_model:
    description: Raw response from Device42 specific hardware model endpoint.
    type: dict
    returned: when query_type=specific
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.hardware_models.d42_hardware_models import (
        d42_hardware_models,
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
                query_type=dict(type="str", required=False, default="list", choices=["list", "specific"]),
                hardware_id=dict(type="int", required=False),
                name=dict(type="str", required=False),
                physicalsubtype_id=dict(type="int", required=False),
                physicalsubtype=dict(type="str", required=False),
                size=dict(type="str", required=False),
                blade_size_id=dict(type="int", required=False),
                blade_size=dict(type="str", required=False),
                depth_id=dict(type="int", required=False),
                depth=dict(type="str", required=False),
                width_ratio_id=dict(type="int", required=False),
                width_ratio=dict(type="str", required=False),
                part_number=dict(type="str", required=False),
                network_device=dict(type="str", required=False, choices=["yes", "no"]),
                blade_host=dict(type="str", required=False, choices=["yes", "no"]),
                watts=dict(type="int", required=False),
                vendor_id=dict(type="int", required=False),
                vendor=dict(type="str", required=False),
                custom_fields_and=dict(type="str", required=False),
                custom_fields_or=dict(type="str", required=False),
                device_id=dict(type="int", required=False),
                include_cols=dict(type="str", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_hardware_models(
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

        if module.params["query_type"] == "specific":
                if module.params["hardware_id"] is None:
                        module.fail_json(msg="hardware_id is required when query_type=specific.")

                result["api_hardware_model"] = helper.d42_get_hardware_model_by_id(
                        hardware_id=module.params["hardware_id"],
                )
                module.exit_json(**result)

        result["api_hardware_models"] = helper.d42_get_hardware_models(
                hardware_id=module.params["hardware_id"],
                name=module.params["name"],
                physicalsubtype_id=module.params["physicalsubtype_id"],
                physicalsubtype=module.params["physicalsubtype"],
                size=module.params["size"],
                blade_size_id=module.params["blade_size_id"],
                blade_size=module.params["blade_size"],
                depth_id=module.params["depth_id"],
                depth=module.params["depth"],
                width_ratio_id=module.params["width_ratio_id"],
                width_ratio=module.params["width_ratio"],
                part_number=module.params["part_number"],
                network_device=module.params["network_device"],
                blade_host=module.params["blade_host"],
                watts=module.params["watts"],
                vendor_id=module.params["vendor_id"],
                vendor=module.params["vendor"],
                custom_fields_and=module.params["custom_fields_and"],
                custom_fields_or=module.params["custom_fields_or"],
                device_id=module.params["device_id"],
                include_cols=module.params["include_cols"],
        )
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
