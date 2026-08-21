#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_switchports_info
short_description: Get Device42 IPAM switch ports
description:
    - Retrieve switch ports from Device42 IPAM.
    - Supports filtering and pagination for C(/api/1.0/switchports/).
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
    switch_id:
        description:
            - ID of the network device where the port is on.
        required: false
        type: int
    include_cols:
        description:
            - Comma separated list of extra attributes to include.
        required: false
        type: str
    switch2_id:
        description:
            - ID of the second network device where the port is on.
        required: false
        type: int
    last_updated_lt:
        description:
            - Filter by last updated date less than value (YYYY-MM-DD).
        required: false
        type: str
    last_updated_gt:
        description:
            - Filter by last updated date greater than or equal to value (YYYY-MM-DD).
        required: false
        type: str
    first_added_lt:
        description:
            - Filter by first added date less than value (YYYY-MM-DD).
        required: false
        type: str
    first_added_gt:
        description:
            - Filter by first added date greater than or equal to value (YYYY-MM-DD).
        required: false
        type: str
    tags:
        description:
            - OR filter by tags (comma separated).
        required: false
        type: str
    tags_and:
        description:
            - AND filter by tags (comma separated).
        required: false
        type: str
    limit:
        description:
            - Number of switch ports to return.
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
            - Retrieve all switch ports using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get switch ports
    xbh03.device42.ipam.switches.d42_api_ipam_switchports_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get switch ports with filters
    xbh03.device42.ipam.switches.d42_api_ipam_switchports_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        switch_id: 1
        include_cols: primary_vlan,primary_vlan_id,speed,name,mtu,port_type,full_path_list
        tags_and: production,network

- name: Get all switch ports with automatic pagination
    xbh03.device42.ipam.switches.d42_api_ipam_switchports_info:
        host: device42.example.internal
        userid: admin
        password: secret123
        fetch_all: true
"""

RETURN = r"""
ipam_switchports:
    description: Raw response from Device42 switchports endpoint.
    type: dict
    returned: success
    sample:
        limit: 3
        offset: 0
        total_count: 349
        switchports:
            - switchport_id: 10
              port: FastEthernet0/21
              description: FastEthernet0/21
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.switches.d42_ipam_switchports import (
    d42_ipam_switchports,
)


def _to_int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


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
        switch_id=dict(type="int", required=False),
        include_cols=dict(type="str", required=False),
        switch2_id=dict(type="int", required=False),
        last_updated_lt=dict(type="str", required=False),
        last_updated_gt=dict(type="str", required=False),
        first_added_lt=dict(type="str", required=False),
        first_added_gt=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        tags_and=dict(type="str", required=False),
        limit=dict(type="int", required=False, default=1000),
        offset=dict(type="int", required=False, default=0),
        fetch_all=dict(type="bool", required=False, default=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    helper = d42_ipam_switchports(
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
        switch_id=module.params["switch_id"],
        include_cols=module.params["include_cols"],
        switch2_id=module.params["switch2_id"],
        last_updated_lt=module.params["last_updated_lt"],
        last_updated_gt=module.params["last_updated_gt"],
        first_added_lt=module.params["first_added_lt"],
        first_added_gt=module.params["first_added_gt"],
        tags=module.params["tags"],
        tags_and=module.params["tags_and"],
    )

    if module.params["fetch_all"]:
        page_size = 1000
        offset = 0
        merged = []
        total_count = None

        while True:
            page = helper.d42_get_switchports(limit=page_size, offset=offset, **base_filters)
            page_switchports = page.get("switchports", [])
            merged.extend(page_switchports if isinstance(page_switchports, list) else [])

            page_total = _to_int_or_none(page.get("total_count"))
            if page_total is not None:
                total_count = page_total

            if not page_switchports:
                break

            offset += len(page_switchports)
            if total_count is not None and offset >= total_count:
                break

        ipam_switchports = {
            "switchports": merged,
            "total_count": total_count if total_count is not None else len(merged),
            "limit": len(merged),
            "offset": 0,
        }
    else:
        ipam_switchports = helper.d42_get_switchports(
            limit=module.params["limit"],
            offset=module.params["offset"],
            **base_filters
        )

    result["ipam_switchports"] = ipam_switchports
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
