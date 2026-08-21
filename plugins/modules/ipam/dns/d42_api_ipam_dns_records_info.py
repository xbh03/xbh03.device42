#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_dns_records_info
short_description: Get Device42 IPAM DNS records
description:
    - Retrieve DNS records from Device42.
    - Supports filtering and pagination for C(/api/1.0/dns/records/).
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
    domain:
        description:
            - Domain name filter.
        required: false
        type: str
    record_type:
        description:
            - DNS record type filter (for example C(AAAA)).
        required: false
        type: str
    content_contains:
        description:
            - Return records whose content contains this value.
        required: false
        type: str
    name:
        description:
            - DNS record name filter.
        required: false
        type: str
    nameserver:
        description:
            - Nameserver filter.
        required: false
        type: str
    content:
        description:
            - Content filter (for example IP address for type A).
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
    dns_zone:
        description:
            - DNS zone filter.
        required: false
        type: str
    ttl:
        description:
            - TTL value filter.
        required: false
        type: str
    change_date:
        description:
            - Change date filter.
        required: false
        type: str
    limit:
        description:
            - Number of DNS records to return.
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
            - Retrieve all DNS records using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get DNS records
    xbh03.device42.d42_ipam_dns_records_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get DNS records by domain and type
    xbh03.device42.d42_ipam_dns_records_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        domain: device42.pvt
        record_type: SOA

- name: Filter DNS records by content and nameserver
    xbh03.device42.d42_ipam_dns_records_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        content_contains: hostmaster
        nameserver: 192.168.11.161

- name: Get all DNS records with automatic pagination
    xbh03.device42.d42_ipam_dns_records_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
ipam_dns_records:
    description: Raw response from Device42 DNS records endpoint.
    type: dict
    returned: success
    sample: |
        total_count: 39
        records:
            - id: 1
                name: "@"
                dns_zone: device42.pvt
                content: nh-win2k8r2-vm-03 hostmaster 107489 900 600 86400 3600
                ttl: 3600
                nameserver: 192.168.11.161
                type: SOA
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
                domain=dict(type="str", required=False),
                record_type=dict(type="str", required=False),
                content_contains=dict(type="str", required=False),
                name=dict(type="str", required=False),
                nameserver=dict(type="str", required=False),
                content=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_and=dict(type="str", required=False),
                dns_zone=dict(type="str", required=False),
                ttl=dict(type="str", required=False),
                change_date=dict(type="str", required=False),
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
                domain=module.params["domain"],
                record_type=module.params["record_type"],
                content_contains=module.params["content_contains"],
                name=module.params["name"],
                nameserver=module.params["nameserver"],
                content=module.params["content"],
                tags=module.params["tags"],
                tags_and=module.params["tags_and"],
                dns_zone=module.params["dns_zone"],
                ttl=module.params["ttl"],
                change_date=module.params["change_date"],
        )

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_dns_records(limit=page_size, offset=offset, **base_filters)
                        page_records = page.get("records", [])
                        merged.extend(page_records)

                        page_total = _to_int_or_none(page.get("total_count"))
                        if page_total is not None:
                                total_count = page_total

                        if not page_records:
                                break

                        offset += len(page_records)
                        if total_count is not None and offset >= total_count:
                                break

                ipam_dns_records = {
                        "records": merged,
                        "total_count": total_count if total_count is not None else len(merged),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                ipam_dns_records = helper.d42_get_dns_records(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                        **base_filters
                )

        result["ipam_dns_records"] = ipam_dns_records
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
