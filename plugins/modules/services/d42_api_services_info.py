#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_services_info
short_description: Get Device42 services
description:
    - Retrieve services from Device42 v2 API.
    - Supports filtering and pagination for C(/api/2.0/services/).
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
    service_id:
        description:
            - Device42 service ID.
        required: false
        type: int
    displayname:
        description:
            - Service display name.
        required: false
        type: str
    category:
        description:
            - Service category name.
        required: false
        type: str
    vendor:
        description:
            - Service vendor name.
        required: false
        type: str
    limit:
        description:
            - Number of services to return.
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
            - Retrieve all services using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get Device42 services
    xbh03.device42.d42_api_services_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get Device42 service by ID
    xbh03.device42.d42_api_services_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        service_id: 2

- name: Filter Device42 services by display name and vendor
    xbh03.device42.d42_api_services_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        displayname: apport-autoreport
        vendor: Example Vendor

- name: Get all Device42 services with automatic pagination
    xbh03.device42.d42_api_services_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
api_services:
    description: Raw response from Device42 services endpoint.
    type: dict
    returned: success
    sample: |
        services:
            - category: ""
                vendor: ""
                description: ""
                tags: []
                notes: ""
                service-type: "null"
                displayname: apport-autoreport
                id: 2
        total_count: 2
        limit: 1000
        offset: 0
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.services.d42_services import (
        d42_services,
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
                service_id=dict(type="int", required=False),
                displayname=dict(type="str", required=False),
                category=dict(type="str", required=False),
                vendor=dict(type="str", required=False),
                limit=dict(type="int", required=False, default=1000),
                offset=dict(type="int", required=False, default=0),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_services(
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
                service_id=module.params["service_id"],
                displayname=module.params["displayname"],
                category=module.params["category"],
                vendor=module.params["vendor"],
        )

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_services(limit=page_size, offset=offset, **base_filters)
                        page_services = page.get("services", [])
                        merged.extend(page_services)

                        page_total = page.get("total_count")
                        try:
                                page_total = int(page_total)
                        except (TypeError, ValueError):
                                page_total = None

                        if page_total is not None:
                                total_count = page_total

                        if not page_services:
                                break

                        offset += len(page_services)
                        if total_count is not None and offset >= total_count:
                                break

                api_services = {
                        "services": merged,
                        "total_count": total_count if total_count is not None else len(merged),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                api_services = helper.d42_get_services(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                        **base_filters
                )

        result["api_services"] = api_services
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
