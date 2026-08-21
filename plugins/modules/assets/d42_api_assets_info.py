#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_assets_info
short_description: Get Device42 assets
description:
  - Retrieve basic information about Device42 assets.
  - Supports list endpoint C(/api/1.0/assets/) and specific endpoint C(/api/1.0/assets/{id}/).
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
      - Select which assets endpoint to query.
      - Use C(list) for C(/api/1.0/assets/).
      - Use C(specific) for C(/api/1.0/assets/{id}/).
    required: false
    type: str
    default: list
    choices:
      - list
      - specific
  asset_no:
    description:
      - Filter by asset number.
    required: false
    type: str
  serial_no:
    description:
      - Filter by serial number.
    required: false
    type: str
  last_updated_lt:
    description:
      - Filter by last updated date less than this value (YYYY-MM-DD).
    required: false
    type: str
  last_updated_gt:
    description:
      - Filter by last updated date greater or equal to this value (YYYY-MM-DD).
    required: false
    type: str
  first_added_lt:
    description:
      - Filter by first added date less than this value (YYYY-MM-DD).
    required: false
    type: str
  first_added_gt:
    description:
      - Filter by first added date greater or equal to this value (YYYY-MM-DD).
    required: false
    type: str
  asset_type:
    description:
      - Filter by asset type.
    required: false
    type: str
  asset_id:
    description:
      - Filter by asset ID.
    required: false
    type: int
  service_level:
    description:
      - Filter by service level name.
    required: false
    type: str
  customer:
    description:
      - Filter by customer name.
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
  asset_no_contains:
    description:
      - Filter by partial asset number match.
    required: false
    type: str
  custom_fields_and:
    description:
      - AND filter by custom fields in format key1:value1,key2:value2.
    required: false
    type: str
  custom_fields_or:
    description:
      - OR filter by custom fields in format key1:value1,key2:value2.
    required: false
    type: str
  related_device_id:
    description:
      - Filter by related device ID.
    required: false
    type: int
  include_cols:
    description:
      - Return only specified columns, comma separated.
    required: false
    type: str
  limit:
    description:
      - Number of assets to return.
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
      - Retrieve all assets using automatic pagination.
      - When true, C(limit) and C(offset) are ignored.
    required: false
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Get all Device42 assets (single page)
  xbh03.device42.d42_api_assets_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123

- name: Get all Device42 assets with automatic pagination
  xbh03.device42.d42_api_assets_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    fetch_all: true

- name: Filter Device42 assets by asset number
  xbh03.device42.d42_api_assets_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    asset_no: "0075"

- name: Get specific Device42 asset by ID
  xbh03.device42.d42_api_assets_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    query_type: specific
    asset_id: 16
    include_cols: name,asset_id,asset_no,serial_no,type,rack,start_at

- name: Filter Device42 assets by tags and include specific columns
  xbh03.device42.d42_api_assets_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    tags: prod,dmz
    include_cols: name,asset_no,serial_no,rack

- name: Paginate Device42 assets manually
  xbh03.device42.d42_api_assets_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    limit: 100
    offset: 200
"""

RETURN = r"""
api_assets:
  description: Raw response from Device42 assets endpoint.
  type: dict
  returned: when query_type=list
  sample:
    assets:
      - asset_id: 16
        asset_no: "0075"
        name: DC1R5PP1
        type: Patch Panel
    limit: 2
    offset: 0
    total_count: 209
api_asset:
  description: Raw response from Device42 specific asset endpoint.
  type: dict
  returned: when query_type=specific
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.assets.d42_assets import (
    d42_assets,
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
        asset_no=dict(type="str", required=False),
        serial_no=dict(type="str", required=False),
        last_updated_lt=dict(type="str", required=False),
        last_updated_gt=dict(type="str", required=False),
        first_added_lt=dict(type="str", required=False),
        first_added_gt=dict(type="str", required=False),
        asset_type=dict(type="str", required=False),
        asset_id=dict(type="int", required=False),
        service_level=dict(type="str", required=False),
        customer=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        tags_and=dict(type="str", required=False),
        asset_no_contains=dict(type="str", required=False),
        custom_fields_and=dict(type="str", required=False),
        custom_fields_or=dict(type="str", required=False),
        related_device_id=dict(type="int", required=False),
        include_cols=dict(type="str", required=False),
        limit=dict(type="int", required=False, default=1000),
        offset=dict(type="int", required=False, default=0),
        fetch_all=dict(type="bool", required=False, default=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    helper = d42_assets(
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
        asset_no=module.params["asset_no"],
        serial_no=module.params["serial_no"],
        last_updated_lt=module.params["last_updated_lt"],
        last_updated_gt=module.params["last_updated_gt"],
        first_added_lt=module.params["first_added_lt"],
        first_added_gt=module.params["first_added_gt"],
        asset_type=module.params["asset_type"],
        asset_id=module.params["asset_id"],
        service_level=module.params["service_level"],
        customer=module.params["customer"],
        tags=module.params["tags"],
        tags_and=module.params["tags_and"],
        asset_no_contains=module.params["asset_no_contains"],
        custom_fields_and=module.params["custom_fields_and"],
        custom_fields_or=module.params["custom_fields_or"],
        related_device_id=module.params["related_device_id"],
        include_cols=module.params["include_cols"],
    )

    query_type = module.params["query_type"]

    if query_type == "specific":
        if module.params["asset_id"] is None:
            module.fail_json(msg="asset_id is required when query_type=specific.")
        if module.params["fetch_all"]:
            module.fail_json(msg="fetch_all is not supported when query_type=specific.")

        result["api_asset"] = helper.d42_get_asset_by_id(
            asset_id=module.params["asset_id"],
            include_cols=module.params["include_cols"],
        )
        module.exit_json(**result)

    if module.params["fetch_all"]:
        page_size = 1000
        offset = 0
        merged = []
        total_count = None

        while True:
            page = helper.d42_get_assets(limit=page_size, offset=offset, **base_filters)
            page_assets = page.get("assets", [])
            merged.extend(page_assets)

            page_total = page.get("total_count")
            try:
                page_total = int(page_total)
            except (TypeError, ValueError):
                page_total = None

            if page_total is not None:
                total_count = page_total

            if not page_assets:
                break

            offset += len(page_assets)
            if total_count is not None and offset >= total_count:
                break

        api_assets = {
            "assets": merged,
            "total_count": total_count if total_count is not None else len(merged),
            "limit": len(merged),
            "offset": 0,
        }
    else:
        api_assets = helper.d42_get_assets(
            limit=module.params["limit"],
            offset=module.params["offset"],
            **base_filters
        )

    result["api_assets"] = api_assets
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
