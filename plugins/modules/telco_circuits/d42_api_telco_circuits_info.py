#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_telco_circuits_info
short_description: Get Device42 telco circuits
description:
    - Retrieve telco circuits from Device42.
    - Supports filters for C(/api/1.0/circuits/).
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
    id:
        description:
            - Device42 numeric ID of the circuit.
        required: false
        type: int
    circuit_id:
        description:
            - Circuit identifier.
        required: false
        type: str
    type:
        description:
            - Type of circuit.
        required: false
        type: str
    origin_type:
        description:
            - Type of origin point.
        required: false
        type: str
        choices:
            - cable
            - circuit
            - switchport
            - vendor
            - patch_panel_port
    origin_id:
        description:
            - ID of the origin point.
        required: false
        type: int
    end_point_type:
        description:
            - Type of end point.
        required: false
        type: str
        choices:
            - cable
            - circuit
            - switchport
            - vendor
            - patch_panel_port
    end_point_id:
        description:
            - ID of the end point.
        required: false
        type: int
"""

EXAMPLES = r"""
- name: Get all telco circuits
    xbh03.device42.telco_circuits.d42_api_telco_circuits_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter circuits by type and origin
    xbh03.device42.telco_circuits.d42_api_telco_circuits_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        type: Dedicated Ethernet
        origin_type: vendor
        origin_id: 193

"""

RETURN = r"""
api_telco_circuits:
    description: Raw response from Device42 circuits endpoint.
    type: dict
    returned: success
    sample:
        circuits:
            - ID: 1
              circuit_id: L3-01
              type: Dedicated Ethernet
              origin_type: vendor
              origin_id: 193
              end_point_type: patch_panel_port
              end_point_id: 124
              customer: ABC Inc.
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.telco_circuits.d42_telco_circuits import (
        d42_telco_circuits,
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
                id=dict(type="int", required=False),
                circuit_id=dict(type="str", required=False),
                type=dict(type="str", required=False),
                origin_type=dict(
                        type="str",
                        required=False,
                        choices=["cable", "circuit", "switchport", "vendor", "patch_panel_port"],
                ),
                origin_id=dict(type="int", required=False),
                end_point_type=dict(
                        type="str",
                        required=False,
                        choices=["cable", "circuit", "switchport", "vendor", "patch_panel_port"],
                ),
                end_point_id=dict(type="int", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_telco_circuits(
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

        base_filters = dict(
                id=module.params["id"],
                circuit_id=module.params["circuit_id"],
                circuit_type=module.params["type"],
                origin_type=module.params["origin_type"],
                origin_id=module.params["origin_id"],
                end_point_type=module.params["end_point_type"],
                end_point_id=module.params["end_point_id"],
        )

        api_telco_circuits = helper.d42_get_circuits(**base_filters)

        result["api_telco_circuits"] = api_telco_circuits
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
