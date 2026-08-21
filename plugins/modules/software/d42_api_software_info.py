#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_software_info
short_description: Get Device42 software details
description:
    - Retrieve software component details from Device42.
    - Supports filtering and pagination for C(/api/1.0/software/).
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
            - Filter by software name.
        required: false
        type: str
    category:
        description:
            - Filter by software category.
        required: false
        type: str
    vendor:
        description:
            - Filter by software vendor.
        required: false
        type: str
    licensing_model:
        description:
            - Filter by licensing model.
        required: false
        type: str
    software_type:
        description:
            - Filter by software type.
            - Allowed values are C(managed), C(unmanaged), C(prohibited), C(ignored).
        required: false
        type: str
        choices:
            - managed
            - unmanaged
            - prohibited
            - ignored
    deployment_type:
        description:
            - Filter by deployment type.
            - Allowed values are C(saas), C(mobile), C(desktop), C(server).
        required: false
        type: str
        choices:
            - saas
            - mobile
            - desktop
            - server
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
            - Number of software records to return.
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
            - Retrieve all software records using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get Device42 software details
    xbh03.device42.d42_api_software_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Filter software by name and vendor
    xbh03.device42.d42_api_software_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        name: 2pay
        vendor: cisco

- name: Filter software by type and deployment
    xbh03.device42.d42_api_software_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        software_type: prohibited
        deployment_type: mobile

- name: Get all software with automatic pagination
    xbh03.device42.d42_api_software_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
api_software:
    description: Raw response from Device42 software endpoint.
    type: dict
    returned: success
    sample: |
        total_count: "2016"
        software:
            - name: 2pay
                vendor: cisco
                category: past_time2
                licensing_model: Individual - Device/Perpetual
                software_type: prohibited
                deployment_type: mobile
                id: "583"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.software.d42_software import (
        d42_software,
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
                category=dict(type="str", required=False),
                vendor=dict(type="str", required=False),
                licensing_model=dict(type="str", required=False),
                software_type=dict(
                        type="str",
                        required=False,
                        choices=["managed", "unmanaged", "prohibited", "ignored"],
                ),
                deployment_type=dict(
                        type="str",
                        required=False,
                        choices=["saas", "mobile", "desktop", "server"],
                ),
                tags=dict(type="str", required=False),
                tags_and=dict(type="str", required=False),
                limit=dict(type="int", required=False, default=1000),
                offset=dict(type="int", required=False, default=0),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_software(
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
                category=module.params["category"],
                vendor=module.params["vendor"],
                licensing_model=module.params["licensing_model"],
                software_type=module.params["software_type"],
                deployment_type=module.params["deployment_type"],
                tags=module.params["tags"],
                tags_and=module.params["tags_and"],
        )

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_software(limit=page_size, offset=offset, **base_filters)
                        page_software = page.get("software", [])
                        merged.extend(page_software)

                        page_total = page.get("total_count")
                        try:
                                page_total = int(page_total)
                        except (TypeError, ValueError):
                                page_total = None

                        if page_total is not None:
                                total_count = page_total

                        if not page_software:
                                break

                        offset += len(page_software)
                        if total_count is not None and offset >= total_count:
                                break

                api_software = {
                        "software": merged,
                        "total_count": str(total_count if total_count is not None else len(merged)),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                api_software = helper.d42_get_software(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                        **base_filters
                )

        result["api_software"] = api_software
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
