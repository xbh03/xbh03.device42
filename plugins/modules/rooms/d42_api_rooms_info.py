#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_rooms_info
short_description: Get Device42 rooms
description:
    - Retrieve information about Device42 rooms.
    - Supports list endpoint C(/api/1.0/rooms/) and specific endpoint C(/api/1.0/rooms/{ID}/).
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
            - Select which rooms endpoint to query.
            - Use C(list) for C(/api/1.0/rooms/).
            - Use C(specific) for C(/api/1.0/rooms/{ID}/).
        required: false
        type: str
        default: list
        choices:
            - list
            - specific
    name:
        description:
            - Filter by room name for list endpoint.
        required: false
        type: str
    building_id:
        description:
            - Filter by building ID for list endpoint.
        required: false
        type: int
    building:
        description:
            - Filter by building name for list endpoint.
        required: false
        type: str
    room_id:
        description:
            - Room ID for specific endpoint.
        required: false
        type: int
"""

EXAMPLES = r"""
- name: Get all Device42 rooms
    xbh03.device42.rooms.d42_rooms_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter rooms by building name
    xbh03.device42.rooms.d42_rooms_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        building: New Haven DC

- name: Filter rooms by building ID
    xbh03.device42.rooms.d42_rooms_info:
        host: device42.example.internal
        userid: admin
        password: secret123
        building_id: 1

- name: Get specific room by ID
    xbh03.device42.rooms.d42_rooms_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: specific
        room_id: 1
"""

RETURN = r"""
api_rooms:
    description: Raw response from Device42 rooms list endpoint.
    type: dict
    returned: when query_type=list
    sample: |
        rooms:
            - room_id: 1
                name: 1st floor
                building: New Haven DC
                building_id: 1
api_room:
    description: Raw response from Device42 specific room endpoint.
    type: dict
    returned: when query_type=specific
    sample: |
        room_id: 1
        name: NHDC1
        building: New Haven
        building_id: 1
        grid_rows: 9
        grid_cols: 10
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.rooms.d42_rooms import (
        d42_rooms,
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
                building_id=dict(type="int", required=False),
                building=dict(type="str", required=False),
                room_id=dict(type="int", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_rooms(
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
                if module.params["room_id"] is None:
                        module.fail_json(msg="room_id is required when query_type=specific.")

                result["api_room"] = helper.d42_get_room_by_id(room_id=module.params["room_id"])
                module.exit_json(**result)

        result["api_rooms"] = helper.d42_get_rooms(
                name=module.params["name"],
                building_id=module.params["building_id"],
                building=module.params["building"],
        )
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
