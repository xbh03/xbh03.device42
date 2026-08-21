#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_ips_info
short_description: Get Device42 IPAM IPs
description:
    - Retrieve IP addresses from Device42 API v2.
    - Supports filtering and pagination for C(/api/2.0/ips/).
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
    offset:
        description:
            - Start position for pagination.
        required: false
        type: int
        default: 0
    limit:
        description:
            - Number of IPs to return.
        required: false
        type: int
        default: 1000
    subnet_id:
        description:
            - Subnet ID filter.
        required: false
        type: int
    subnet:
        description:
            - Subnet name filter.
        required: false
        type: str
    device:
        description:
            - Device name filter.
        required: false
        type: str
    mac:
        description:
            - MAC address filter.
        required: false
        type: str
    available:
        description:
            - Availability filter.
            - Allowed values are C(yes) and C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    ip_type:
        description:
            - IP type filter.
            - Allowed values are C(static), C(dhcp), C(reserved).
        required: false
        type: str
        choices:
            - static
            - dhcp
            - reserved
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
    ip:
        description:
            - IP address filter.
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
    ip_id:
        description:
            - Device42 IP ID filter.
        required: false
        type: int
    label:
        description:
            - Label filter.
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
    total_count:
        description:
            - Optional total_count query parameter as supported by API.
        required: false
        type: int
    is_shared:
        description:
            - Filter shared IPs.
            - Allowed values are C(yes) and C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    fetch_all:
        description:
            - Retrieve all IPs using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get IPs
    xbh03.device42.d42_ipam_ips_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter IPs by subnet and type
    xbh03.device42.d42_ipam_ips_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        subnet_id: 5
        ip_type: reserved

- name: Filter IPs by availability and shared status
    xbh03.device42.d42_ipam_ips_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        available: no
        is_shared: yes

- name: Get all IPs with automatic pagination
    xbh03.device42.d42_ipam_ips_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
ipam_ips:
    description: Raw response from Device42 IPs endpoint.
    type: dict
    returned: success
    sample: |
        ips:
            - id: 38
                ip: 10.1.10.5
                subnet_id: 5
                type: Reserved
                available: "no"
        limit: 4
        offset: 0
        total_count: 1004
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.ips.d42_ipam_ips import (
        d42_ipam_ips,
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
                offset=dict(type="int", required=False, default=0),
                limit=dict(type="int", required=False, default=1000),
                subnet_id=dict(type="int", required=False),
                subnet=dict(type="str", required=False),
                device=dict(type="str", required=False),
                mac=dict(type="str", required=False),
                available=dict(type="str", required=False, choices=["yes", "no"]),
                ip_type=dict(type="str", required=False, choices=["static", "dhcp", "reserved"]),
                last_updated_lt=dict(type="str", required=False),
                last_updated_gt=dict(type="str", required=False),
                ip=dict(type="str", required=False),
                first_added_lt=dict(type="str", required=False),
                first_added_gt=dict(type="str", required=False),
                ip_id=dict(type="int", required=False),
                label=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_and=dict(type="str", required=False),
                custom_fields_and=dict(type="str", required=False),
                custom_fields_or=dict(type="str", required=False),
                total_count=dict(type="int", required=False),
                is_shared=dict(type="str", required=False, choices=["yes", "no"]),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_ipam_ips(
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
                subnet_id=module.params["subnet_id"],
                subnet=module.params["subnet"],
                device=module.params["device"],
                mac=module.params["mac"],
                available=module.params["available"],
                ip_type=module.params["ip_type"],
                last_updated_lt=module.params["last_updated_lt"],
                last_updated_gt=module.params["last_updated_gt"],
                ip=module.params["ip"],
                first_added_lt=module.params["first_added_lt"],
                first_added_gt=module.params["first_added_gt"],
                ip_id=module.params["ip_id"],
                label=module.params["label"],
                tags=module.params["tags"],
                tags_and=module.params["tags_and"],
                custom_fields_and=module.params["custom_fields_and"],
                custom_fields_or=module.params["custom_fields_or"],
                total_count=module.params["total_count"],
                is_shared=module.params["is_shared"],
        )

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count_value = None

                while True:
                        page = helper.d42_get_ips(limit=page_size, offset=offset, **base_filters)
                        page_ips = page.get("ips", [])
                        merged.extend(page_ips)

                        page_total = _to_int_or_none(page.get("total_count"))
                        if page_total is not None:
                                total_count_value = page_total

                        if not page_ips:
                                break

                        offset += len(page_ips)
                        if total_count_value is not None and offset >= total_count_value:
                                break

                ipam_ips = {
                        "ips": merged,
                        "total_count": total_count_value if total_count_value is not None else len(merged),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                ipam_ips = helper.d42_get_ips(
                        offset=module.params["offset"],
                        limit=module.params["limit"],
                        **base_filters
                )

        result["ipam_ips"] = ipam_ips
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
