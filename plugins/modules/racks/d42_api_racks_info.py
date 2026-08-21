#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_racks_info
short_description: Get Device42 racks
description:
    - Retrieve basic information about racks from Device42.
    - Supports filters and pagination for C(/api/1.0/racks/).
version_added: "0.1.0"
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
        required: true
        type: str
    client_secret_key:
        description:
            - Device42 API client secret key used to authenticate.
        required: true
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
            - Filter by rack name.
        required: false
        type: str
    building_id:
        description:
            - Filter by building ID.
        required: false
        type: int
    building:
        description:
            - Filter by building name.
        required: false
        type: str
    room_id:
        description:
            - Filter by room ID.
        required: false
        type: int
    room:
        description:
            - Filter by room name.
            - Effective only when C(room_id) is not set.
        required: false
        type: str
    size:
        description:
            - Filter by rack size in U.
        required: false
        type: int
    row:
        description:
            - Filter by row name.
        required: false
        type: str
    asset_no:
        description:
            - Filter by asset number.
        required: false
        type: str
    manufacturer:
        description:
            - Filter by manufacturer.
        required: false
        type: str
    limit:
        description:
            - Number of racks to return.
        required: false
        type: int
        default: 1000
    offset:
        description:
            - Start position for pagination.
        required: false
        type: int
        default: 0
    fetch_all:
        description:
            - Retrieve all racks using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get Device42 racks
    xbh03.device42.d42_api_racks_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter Device42 racks by building and room
    xbh03.device42.d42_api_racks_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        building: Building
        room: Main room

- name: Get Device42 racks with manual pagination
    xbh03.device42.d42_api_racks_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        limit: 100
        offset: 200

- name: Get all Device42 racks with automatic pagination
    xbh03.device42.d42_api_racks_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
api_racks:
    description: Raw response from Device42 racks endpoint.
    type: dict
    returned: success
    sample: |
        limit: 2
        offset: 0
        racks:
            - rack_id: 255
                name: RA1
                building: Building
                room: Main room
                size: "45"
        total_count: 275
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.racks.d42_racks import (
        d42_racks,
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
                name=dict(type="str", required=False),
                building_id=dict(type="int", required=False),
                building=dict(type="str", required=False),
                room_id=dict(type="int", required=False),
                room=dict(type="str", required=False),
                size=dict(type="int", required=False),
                row=dict(type="str", required=False),
                asset_no=dict(type="str", required=False),
                manufacturer=dict(type="str", required=False),
                limit=dict(type="int", required=False, default=1000),
                offset=dict(type="int", required=False, default=0),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_racks(
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
                name=module.params["name"],
                building_id=module.params["building_id"],
                building=module.params["building"],
                room_id=module.params["room_id"],
                room=module.params["room"],
                size=module.params["size"],
                row=module.params["row"],
                asset_no=module.params["asset_no"],
                manufacturer=module.params["manufacturer"],
        )

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_racks(limit=page_size, offset=offset, **base_filters)
                        page_racks = page.get("racks", [])
                        merged.extend(page_racks)

                        page_total = page.get("total_count")
                        try:
                                page_total = int(page_total)
                        except (TypeError, ValueError):
                                page_total = None

                        if page_total is not None:
                                total_count = page_total

                        if not page_racks:
                                break

                        offset += len(page_racks)
                        if total_count is not None and offset >= total_count:
                                break

                api_racks = {
                        "racks": merged,
                        "total_count": total_count if total_count is not None else len(merged),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                api_racks = helper.d42_get_racks(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                        **base_filters
                )

        result["api_racks"] = api_racks
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
