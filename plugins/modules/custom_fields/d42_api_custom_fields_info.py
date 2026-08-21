#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_custom_fields_info
short_description: Get Device42 custom fields
description:
    - Retrieve custom fields for a Device42 model from C(/api/2.0/custom_fields/).
    - The C(object_name) parameter is required.
    - Optional filters C(id), C(type), and C(key) are supported.
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
    object_name:
        description:
            - Name of the Device42 object model.
        required: true
        type: str
        choices:
            - application_group
            - application_group_calculation_rule
            - appcomp
            - appcomp_template
            - asset
            - building
            - business_service
            - cable
            - certificate
            - circuit
            - cloud_account
            - customer
            - device
            - dns_records
            - dns_zone
            - endusers
            - hardware_model
            - ip_address
            - part
            - partmodel
            - pdu
            - port
            - purchase
            - rack
            - resource
            - room
            - secret
            - service
            - service_instance
            - software
            - software_instance
            - subnet
            - vendor
            - vlan
            - vrfgroup
    id:
        description:
            - Filter by custom field ID.
        required: false
        type: int
    type:
        description:
            - Filter by custom field type.
        required: false
        type: str
        choices:
            - text
            - number
            - date
            - related_field
            - boolean
            - url
            - picklist
            - json
            - markup
    key:
        description:
            - Filter by custom field key/name.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all custom fields for device model
    xbh03.device42.custom_fields.d42_api_custom_fields_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        object_name: device

- name: Get one custom field by key for building model
    xbh03.device42.custom_fields.d42_api_custom_fields_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        object_name: building
        key: room

- name: Get one custom field by ID for asset model
    xbh03.device42.custom_fields.d42_api_custom_fields_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        object_name: asset
        id: 2
"""

RETURN = r"""
api_custom_fields:
    description: Raw response from Device42 custom fields endpoint.
    type: dict
    returned: success
    sample: |
        custom_fields:
            - id: 2
                key: room
                type: Text
                filterable: "false"
                mandatory: "true"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.custom_fields.d42_custom_fields import (
        d42_custom_fields,
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
                object_name=dict(
                        type="str",
                        required=True,
                        choices=[
                                "application_group",
                                "application_group_calculation_rule",
                                "appcomp",
                                "appcomp_template",
                                "asset",
                                "building",
                                "business_service",
                                "cable",
                                "certificate",
                                "circuit",
                                "cloud_account",
                                "customer",
                                "device",
                                "dns_records",
                                "dns_zone",
                                "endusers",
                                "hardware_model",
                                "ip_address",
                                "part",
                                "partmodel",
                                "pdu",
                                "port",
                                "purchase",
                                "rack",
                                "resource",
                                "room",
                                "secret",
                                "service",
                                "service_instance",
                                "software",
                                "software_instance",
                                "subnet",
                                "vendor",
                                "vlan",
                                "vrfgroup",
                        ],
                ),
                id=dict(type="int", required=False),
                type=dict(
                        type="str",
                        required=False,
                        choices=["text", "number", "date", "related_field", "boolean", "url", "picklist", "json", "markup"],
                ),
                key=dict(type="str", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_custom_fields(
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

        result["api_custom_fields"] = helper.d42_get_custom_fields(
                object_name=module.params["object_name"],
                id=module.params["id"],
                type=module.params["type"],
                key=module.params["key"],
        )

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
