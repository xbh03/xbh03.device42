#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_dns_zones_info
short_description: Get Device42 IPAM DNS zones
description:
    - Retrieve DNS zones from Device42.
    - Supports filtering and pagination for C(/api/1.0/dns/zones/).
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
    cloud_infra_id:
        description:
            - Cloud infrastructure ID.
        required: false
        type: int
    domain:
        description:
            - DNS domain name.
        required: false
        type: str
    dns_zone_id:
        description:
            - DNS zone ID.
        required: false
        type: int
    nameserver:
        description:
            - IP address or hostname of name server.
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
    include_cols:
        description:
            - Return only specified columns.
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
    limit:
        description:
            - Number of DNS zones to return.
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
            - Retrieve all DNS zones using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get DNS zones
    xbh03.device42.d42_ipam_dns_zones_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get DNS zone by ID
    xbh03.device42.d42_ipam_dns_zones_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        dns_zone_id: 3

- name: Filter DNS zones by nameserver and tags
    xbh03.device42.d42_ipam_dns_zones_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        nameserver: AWS Route53
        tags: m2m,no

- name: Get all DNS zones with automatic pagination
    xbh03.device42.d42_ipam_dns_zones_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
ipam_dns_zones:
    description: Raw response from Device42 DNS zones endpoint.
    type: dict
    returned: success
    sample: |
        limit: 1000
        total_count: 4
        offset: 0
        dns_zones:
            - id: 3
                name: lab.device42.net
                nameserver: AWS Route53
                cloud_infra_id: 1
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.dns.d42_ipam_dns import (
        d42_ipam_dns,
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
                cloud_infra_id=dict(type="int", required=False),
                domain=dict(type="str", required=False),
                dns_zone_id=dict(type="int", required=False),
                nameserver=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_and=dict(type="str", required=False),
                include_cols=dict(type="str", required=False),
                custom_fields_and=dict(type="str", required=False),
                custom_fields_or=dict(type="str", required=False),
                limit=dict(type="int", required=False, default=1000),
                offset=dict(type="int", required=False, default=0),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_ipam_dns(
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
                cloud_infra_id=module.params["cloud_infra_id"],
                domain=module.params["domain"],
                dns_zone_id=module.params["dns_zone_id"],
                nameserver=module.params["nameserver"],
                tags=module.params["tags"],
                tags_and=module.params["tags_and"],
                include_cols=module.params["include_cols"],
                custom_fields_and=module.params["custom_fields_and"],
                custom_fields_or=module.params["custom_fields_or"],
        )

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_dns_zones(limit=page_size, offset=offset, **base_filters)
                        page_zones = page.get("dns_zones", [])
                        merged.extend(page_zones)

                        page_total = _to_int_or_none(page.get("total_count"))
                        if page_total is not None:
                                total_count = page_total

                        if not page_zones:
                                break

                        offset += len(page_zones)
                        if total_count is not None and offset >= total_count:
                                break

                ipam_dns_zones = {
                        "dns_zones": merged,
                        "total_count": total_count if total_count is not None else len(merged),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                ipam_dns_zones = helper.d42_get_dns_zones(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                        **base_filters
                )

        result["ipam_dns_zones"] = ipam_dns_zones
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
