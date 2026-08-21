#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_tags_info
short_description: Get Device42 tags
description:
    - Retrieve tags from Device42.
    - Supports pagination for C(/api/1.0/tags/).
    - Can automatically fetch all pages.
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
    limit:
        description:
            - Number of tags to return.
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
            - Retrieve all tags using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get Device42 tags (single page)
    xbh03.device42.tags.d42_api_tags_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get Device42 tags with explicit paging
    xbh03.device42.tags.d42_api_tags_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        limit: 200
        offset: 400

- name: Get all Device42 tags
    xbh03.device42.tags.d42_api_tags_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
api_tags:
    description: Raw response from Device42 tags endpoint.
    type: dict
    returned: success
    sample:
        total_count: 30
        limit: 1000
        offset: 0
        tags:
            - name: 1 tag
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.tags.d42_tags import (
        d42_tags,
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
                limit=dict(type="int", required=False, default=1000),
                offset=dict(type="int", required=False, default=0),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_tags(
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

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_tags(limit=page_size, offset=offset)
                        page_tags = page.get("tags", [])
                        merged.extend(page_tags)

                        page_total = _to_int_or_none(page.get("total_count"))
                        if page_total is not None:
                                total_count = page_total

                        if not page_tags:
                                break

                        offset += len(page_tags)
                        if total_count is not None and offset >= total_count:
                                break

                api_tags = {
                        "tags": merged,
                        "total_count": total_count if total_count is not None else len(merged),
                        "limit": len(merged),
                        "offset": 0,
                }
        else:
                api_tags = helper.d42_get_tags(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                )

        result["api_tags"] = api_tags
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
