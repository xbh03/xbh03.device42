#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_subnets_info
short_description: Get Device42 IPAM subnets
description:
    - Retrieve subnets from Device42 IPAM.
    - Supports filtering and pagination for C(/api/1.0/subnets/).
    - Supports specific subnet retrieval for C(/api/1.0/subnets/{subnet_id}/).
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
    query_type:
        description:
            - Query mode.
            - Use C(list) for list endpoint or C(specific) for subnet-by-id endpoint.
        required: false
        type: str
        default: list
        choices:
            - list
            - specific
    name:
        description:
            - Subnet name filter.
        required: false
        type: str
    vrf_group_id:
        description:
            - VRF group ID.
        required: false
        type: int
    vrf_group:
        description:
            - VRF group name.
        required: false
        type: str
    parent_subnet_id:
        description:
            - Parent subnet ID.
        required: false
        type: int
    parent_subnet:
        description:
            - Parent subnet name.
        required: false
        type: str
    customer_id:
        description:
            - Customer ID.
        required: false
        type: int
    customer:
        description:
            - Customer name filter.
        required: false
        type: str
    subnet_id:
        description:
            - Subnet ID.
            - Required when C(query_type=specific).
        required: false
        type: int
    mask_bits:
        description:
            - Exact mask bits filter.
        required: false
        type: int
    mask_bits_lt:
        description:
            - Mask bits less than value.
        required: false
        type: int
    mask_bits_gt:
        description:
            - Mask bits greater than value.
        required: false
        type: int
    description:
        description:
            - Description match filter.
        required: false
        type: str
    range_begin:
        description:
            - Range begin filter.
        required: false
        type: str
    range_end:
        description:
            - Range end filter.
        required: false
        type: str
    gateway:
        description:
            - Gateway filter.
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
    custom_fields_and:
        description:
            - AND filter by custom fields, format key1:value1,key2:value2.
        required: false
        type: str
    custom_fields_or:
        description:
            - OR filter by custom fields, format key1:value1,key2:value2.
        required: false
        type: str
    service_level:
        description:
            - Service level name filter.
        required: false
        type: str
    category:
        description:
            - Category name filter.
        required: false
        type: str
    category_id:
        description:
            - Category ID filter.
        required: false
        type: int
    vlan_id:
        description:
            - VLAN ID filter.
        required: false
        type: int
    network:
        description:
            - Network filter.
        required: false
        type: str
    limit:
        description:
            - Number of subnets to return.
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
            - Retrieve all subnets using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get all subnets
    xbh03.device42.d42_ipam_subnets_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: list

- name: Get subnet by ID
    xbh03.device42.d42_ipam_subnets_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: specific
        subnet_id: 4

- name: Filter subnets by VRF and service level
    xbh03.device42.d42_ipam_subnets_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        vrf_group_id: 1
        service_level: Production

- name: Filter subnets by mask and category
    xbh03.device42.d42_ipam_subnets_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        mask_bits: 24
        category: Infrastructure

- name: Get all subnets with automatic pagination
    xbh03.device42.d42_ipam_subnets_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
ipam_subnets:
    description: Raw response from Device42 subnets endpoint.
    type: dict
    returned: success
    sample: |
        limit: 2
        offset: 0
        subnets:
            - subnet_id: 4
                name: Infra
                network: 10.1.10.0
                mask_bits: 24
                service_level: Production
        total_count: 32
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.subnets.d42_ipam_subnets import (
        d42_ipam_subnets,
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
                query_type=dict(type="str", required=False, default="list", choices=["list", "specific"]),
                name=dict(type="str", required=False),
                vrf_group_id=dict(type="int", required=False),
                vrf_group=dict(type="str", required=False),
                parent_subnet_id=dict(type="int", required=False),
                parent_subnet=dict(type="str", required=False),
                customer_id=dict(type="int", required=False),
                customer=dict(type="str", required=False),
                subnet_id=dict(type="int", required=False),
                mask_bits=dict(type="int", required=False),
                mask_bits_lt=dict(type="int", required=False),
                mask_bits_gt=dict(type="int", required=False),
                description=dict(type="str", required=False),
                range_begin=dict(type="str", required=False),
                range_end=dict(type="str", required=False),
                gateway=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_and=dict(type="str", required=False),
                custom_fields_and=dict(type="str", required=False),
                custom_fields_or=dict(type="str", required=False),
                service_level=dict(type="str", required=False),
                category=dict(type="str", required=False),
                category_id=dict(type="int", required=False),
                vlan_id=dict(type="int", required=False),
                network=dict(type="str", required=False),
                limit=dict(type="int", required=False, default=1000),
                offset=dict(type="int", required=False, default=0),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_ipam_subnets(
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
            if module.params["subnet_id"] is None:
                module.fail_json(msg="subnet_id is required when query_type=specific.")

            result["ipam_subnets"] = helper.d42_get_subnet_by_id(subnet_id=module.params["subnet_id"])
            module.exit_json(**result)

        base_filters = dict(
                name=module.params["name"],
                vrf_group_id=module.params["vrf_group_id"],
                vrf_group=module.params["vrf_group"],
                parent_subnet_id=module.params["parent_subnet_id"],
                parent_subnet=module.params["parent_subnet"],
                customer_id=module.params["customer_id"],
                customer=module.params["customer"],
                subnet_id=module.params["subnet_id"],
                mask_bits=module.params["mask_bits"],
                mask_bits_lt=module.params["mask_bits_lt"],
                mask_bits_gt=module.params["mask_bits_gt"],
                description=module.params["description"],
                range_begin=module.params["range_begin"],
                range_end=module.params["range_end"],
                gateway=module.params["gateway"],
                tags=module.params["tags"],
                tags_and=module.params["tags_and"],
                custom_fields_and=module.params["custom_fields_and"],
                custom_fields_or=module.params["custom_fields_or"],
                service_level=module.params["service_level"],
                category=module.params["category"],
                category_id=module.params["category_id"],
                vlan_id=module.params["vlan_id"],
                network=module.params["network"],
        )

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_subnets(limit=page_size, offset=offset, **base_filters)
                        page_subnets = page.get("subnets", [])
                        merged.extend(page_subnets)

                        page_total = _to_int_or_none(page.get("total_count"))
                        if page_total is not None:
                                total_count = page_total

                        if not page_subnets:
                                break

                        offset += len(page_subnets)
                        if total_count is not None and offset >= total_count:
                                break

                ipam_subnets = {
                        "subnets": merged,
                        "total_count": total_count if total_count is not None else len(merged),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                ipam_subnets = helper.d42_get_subnets(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                        **base_filters
                )

        result["ipam_subnets"] = ipam_subnets
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
