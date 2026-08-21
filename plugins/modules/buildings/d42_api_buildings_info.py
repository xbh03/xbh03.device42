#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_buildings_info
short_description: Get Device42 buildings
description:
    - Retrieve information about Device42 buildings.
    - Supports list endpoint C(/api/1.0/buildings/) and specific endpoint C(/api/1.0/buildings/{id}/).
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
            - Select which buildings endpoint to query.
            - Use C(list) for C(/api/1.0/buildings/).
            - Use C(specific) for C(/api/1.0/buildings/{id}/).
        required: false
        type: str
        default: list
        choices:
            - list
            - specific
    name:
        description:
            - Filter by building name for list endpoint.
        required: false
        type: str
    include_cols:
        description:
            - Return only specified columns, comma separated.
        required: false
        type: str
    building_id:
        description:
            - Building ID for specific endpoint.
        required: false
        type: int
"""

EXAMPLES = r"""
- name: Get all Device42 buildings
    xbh03.device42.buildings.d42_api_buildings_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter Device42 buildings by name
    xbh03.device42.buildings.d42_api_buildings_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        name: Las Vegas Office

- name: Get specific Device42 building by ID
    xbh03.device42.buildings.d42_api_buildings_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: specific
        building_id: 3
        include_cols: name,building_id,address,contact_name,contact_phone,notes,tags,custom_fields,latitude,longitude,image_url
"""

RETURN = r"""
api_buildings:
    description: Raw response from Device42 buildings endpoint.
    type: dict
    returned: when query_type=list
    sample: |
        buildings:
            - building_id: 3
                name: Las Vegas Office
                address: 879 main st
                contact_name: roger
api_building:
    description: Raw response from Device42 specific building endpoint.
    type: dict
    returned: when query_type=specific
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.buildings.d42_buildings import (
        d42_buildings,
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
                name=dict(type="str", required=False),
                include_cols=dict(type="str", required=False),
                building_id=dict(type="int", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_buildings(
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

        query_type = module.params["query_type"]

        if query_type == "specific":
                if module.params["building_id"] is None:
                        module.fail_json(msg="building_id is required when query_type=specific.")

                result["api_building"] = helper.d42_get_building_by_id(
                        building_id=module.params["building_id"],
                        include_cols=module.params["include_cols"],
                )
                module.exit_json(**result)

        result["api_buildings"] = helper.d42_get_buildings(
                name=module.params["name"],
                include_cols=module.params["include_cols"],
        )
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
