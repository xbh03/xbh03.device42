#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_clients_info
short_description: Get Device42 API clients
description:
  - Retrieve API clients from Device42.
  - If client_id is provided, returns a single API client by ID.
  - Otherwise returns paginated API clients.
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
  client_id:
    description:
      - API client ID.
      - When set, the module retrieves only that API client.
    required: false
    type: int
  limit:
    description:
      - Number of API clients to return when client_id is not set.
    required: false
    type: int
    default: 1000
  offset:
    description:
      - Start position for pagination when client_id is not set.
    required: false
    type: int
    default: 0
  fetch_all:
    description:
      - Retrieve all API clients using automatic pagination.
      - Ignored when C(client_id) is set.
      - When true, C(limit) and C(offset) are ignored.
    required: false
    type: bool
    default: true
"""

EXAMPLES = r"""
- name: Get all Device42 API clients
  xbh03.device42.d42_api_clients_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123

- name: Get Device42 API client by ID
  xbh03.device42.d42_api_clients_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    client_id: 2

- name: Get Device42 API clients with pagination
  xbh03.device42.d42_api_clients_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    limit: 100
    offset: 200

- name: Get all Device42 API clients with automatic pagination
  xbh03.device42.d42_api_clients_info:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    fetch_all: true
"""

RETURN = r"""
api_clients:
  description: Raw response from Device42 API clients endpoint.
  type: dict
  returned: success
  sample:
    api_client:
      - id: 2
        client_key: e230e6edfc5b4781a3f2600272506278
        active: true
    total_count: 1
    limit: 1000
    offset: 0
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.admin_users_groups.d42_clients import (
    d42_clients,
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
        client_id=dict(type="int", required=False),
        limit=dict(type="int", required=False, default=1000),
        offset=dict(type="int", required=False, default=0),
        fetch_all=dict(type="bool", required=False, default=True),
    )

    result = dict(changed=False)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    helper = d42_clients(
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

    if module.params["client_id"] is not None:
        api_clients = helper.d42_get_api_client(client_id=module.params["client_id"])
    elif module.params["fetch_all"]:
      page_size = 1000
      offset = 0
      merged = []

      while True:
        page = helper.d42_get_api_clients(limit=page_size, offset=offset)
        page_clients = page.get("api_client", [])
        merged.extend(page_clients)

        total_count = page.get("total_count")
        try:
          total_count = int(total_count)
        except (TypeError, ValueError):
          total_count = None

        if not page_clients:
          break

        offset += len(page_clients)
        if total_count is not None and offset >= total_count:
          break

      api_clients = {
        "api_client": merged,
        "total_count": len(merged),
        "limit": len(merged),
        "offset": 0,
      }
    else:
        api_clients = helper.d42_get_api_clients(
            limit=module.params["limit"],
            offset=module.params["offset"],
        )

    result["api_clients"] = api_clients
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
