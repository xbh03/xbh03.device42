#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_clients
short_description: Manage Device42 API clients
description:
  - Create, update, or delete Device42 API clients.
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
  state:
    description:
      - Desired state of the API client.
    required: false
    type: str
    default: present
    choices:
      - present
      - absent
  client_id:
    description:
      - API client ID.
      - Required when C(state=absent).
    required: false
    type: int
  client_key:
    description:
      - Unique API client key.
      - Required when C(state=present).
    required: false
    type: str
  client_secret_key:
    description:
      - Unique API client secret key.
      - Required when C(state=present).
    required: false
    type: str
  resource_owner:
    description:
      - Username of a Device42 non-staff user.
      - Required when C(state=present).
    required: false
    type: str
  token_ttl:
    description:
      - Token time to live in seconds.
    required: false
    type: int
  active:
    description:
      - Set API client as active/inactive.
    required: false
    type: bool
  force_update:
    description:
      - Force update call for existing API client in C(state=present).
      - Useful when rotating C(client_secret_key), because secret value is not returned by GET.
    required: false
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Create API client
  xbh03.device42.d42_api_clients:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: present
    client_key: abc123
    client_secret_key: secret123
    resource_owner: apiclient
    token_ttl: 60
    active: true

- name: Update API client and force secret rotation
  xbh03.device42.d42_api_clients:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: present
    client_key: abc123
    client_secret_key: newsecret456
    resource_owner: apiclient
    force_update: true

- name: Delete API client
  xbh03.device42.d42_api_clients:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: absent
    client_id: 2
"""

RETURN = r"""
api_client:
  description: Current or resulting API client data when available.
  type: dict
  returned: success
response:
  description: Raw response from Device42 for create/update/delete operations.
  type: dict
  returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.admin_users_groups.d42_clients import (
    d42_clients,
)


def _normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _find_api_client_by_key(helper, client_key, page_size=1000):
  offset = 0

  while True:
    payload = helper.d42_get_api_clients(limit=page_size, offset=offset)
    clients = payload.get("api_client", [])

    for client in clients:
      if client.get("client_key") == client_key:
        return client

    total_count = payload.get("total_count")
    try:
      total_count = int(total_count)
    except (TypeError, ValueError):
      total_count = None

    if not clients:
      return None

    offset += len(clients)
    if total_count is not None and offset >= total_count:
      return None


def _find_api_client_by_id(helper, client_id, page_size=1000):
  offset = 0

  while True:
    payload = helper.d42_get_api_clients(limit=page_size, offset=offset)
    clients = payload.get("api_client", [])

    for client in clients:
      try:
        current_id = int(client.get("id", -1))
      except (TypeError, ValueError):
        current_id = -1
      if current_id == int(client_id):
        return client

    total_count = payload.get("total_count")
    try:
      total_count = int(total_count)
    except (TypeError, ValueError):
      total_count = None

    if not clients:
      return None

    offset += len(clients)
    if total_count is not None and offset >= total_count:
      return None


def run_module():
    module_args = dict(
        host=dict(type="str", required=True),
        userid=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        proto=dict(type="str", required=False, default="https", choices=["http", "https"]),
        port=dict(type="int", required=False, default=443),
        sslverify=dict(type="bool", required=False, default=True),
        debug=dict(type="bool", required=False, default=False),
        state=dict(type="str", required=False, default="present", choices=["present", "absent"]),
        client_id=dict(type="int", required=False),
        client_key=dict(type="str", required=False),
        client_secret_key=dict(type="str", required=False, no_log=True),
        resource_owner=dict(type="str", required=False),
        token_ttl=dict(type="int", required=False),
        active=dict(type="bool", required=False),
        force_update=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["client_key", "client_secret_key", "resource_owner"]),
            ("state", "absent", ["client_id"]),
        ],
    )

    result = dict(changed=False)

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

    state = module.params["state"]

    if state == "absent":
        client_id = module.params["client_id"]
        existing = _find_api_client_by_id(helper=helper, client_id=client_id)

        if not existing:
            result["msg"] = "API client already absent"
            module.exit_json(**result)

        result["api_client"] = existing
        result["changed"] = True

        if module.check_mode:
            result["msg"] = "API client would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_api_client(client_id=client_id)
        result["response"] = response
        module.exit_json(**result)

    desired_client_key = module.params["client_key"]
    existing = _find_api_client_by_key(helper=helper, client_key=desired_client_key)

    needs_change = False
    if not existing:
        needs_change = True
    else:
        if existing.get("resource_owner") != module.params["resource_owner"]:
            needs_change = True

        if module.params["token_ttl"] is not None:
            current_ttl = existing.get("token_ttl")
            try:
                current_ttl = int(current_ttl)
            except (TypeError, ValueError):
                current_ttl = None
            if current_ttl != int(module.params["token_ttl"]):
                needs_change = True

        if module.params["active"] is not None:
            current_active = _normalize_bool(existing.get("active"))
            if current_active != bool(module.params["active"]):
                needs_change = True

        if module.params["force_update"]:
            needs_change = True

    if not needs_change:
        result["api_client"] = existing
        result["msg"] = "API client already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "API client would be created/updated"
        if existing:
            result["api_client"] = existing
        module.exit_json(**result)

    response = helper.d42_post_api_client(
        client_key=module.params["client_key"],
        client_secret_key=module.params["client_secret_key"],
        resource_owner=module.params["resource_owner"],
        token_ttl=module.params["token_ttl"],
        active=module.params["active"],
    )

    result["response"] = response

    result["api_client"] = _find_api_client_by_key(
      helper=helper,
      client_key=module.params["client_key"],
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
