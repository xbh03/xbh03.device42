#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_asset_device_lifecycle_info
short_description: Get Device42 asset and device lifecycle events
description:
    - Retrieve lifecycle events from Device42.
    - If C(event_id) is provided, returns a specific lifecycle event by ID.
    - Otherwise returns lifecycle events with optional filters.
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
    event_id:
        description:
            - Lifecycle event ID.
            - When set, the module retrieves only that event.
        required: false
        type: int
    event_type:
        description:
            - Filter by lifecycle event type.
            - Ignored when C(event_id) is set.
        required: false
        type: str
        aliases:
            - type
    device:
        description:
            - Filter by device name.
            - Ignored when C(event_id) is set.
        required: false
        type: str
    asset:
        description:
            - Filter by asset name.
            - Ignored when C(event_id) is set.
        required: false
        type: str
    asset_id:
        description:
            - Filter by asset ID.
            - Ignored when C(event_id) is set.
        required: false
        type: int
    enduser:
        description:
            - Filter by end user name.
            - Ignored when C(event_id) is set.
        required: false
        type: str
    date_gt:
        description:
            - Filter by date greater than C(YYYY-MM-DD).
            - Ignored when C(event_id) is set.
        required: false
        type: str
    date_lt:
        description:
            - Filter by date less than C(YYYY-MM-DD).
            - Ignored when C(event_id) is set.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all lifecycle events
    xbh03.device42.d42_api_asset_device_lifecycle_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get lifecycle events filtered by type and date
    xbh03.device42.d42_api_asset_device_lifecycle_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        event_type: Purchased
        date_gt: 2024-01-01

- name: Get specific lifecycle event by ID
    xbh03.device42.d42_api_asset_device_lifecycle_info:
        host: device42.example.internal
        userid: admin
        password: secret123
        event_id: 4
"""

RETURN = r"""
api_lifecycle_events:
    description: Raw response from Device42 lifecycle events list endpoint.
    type: dict
    returned: when C(event_id) is not set
    sample:
        lifecycle_events:
            - id: 4
              type: Purchased
              asset_id: 224
              asset_name: heart of gold
api_lifecycle_event:
    description: Raw response from Device42 specific lifecycle event endpoint.
    type: dict
    returned: when C(event_id) is set
    sample:
        lifecycle_event:
            id: 1
            type: Inventoried
            date: 2021-11-15T20:37:32Z
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.asset_device_lifecycle.d42_asset_device_lifecycle import (
    d42_asset_device_lifecycle,
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
        event_id=dict(type="int", required=False),
        event_type=dict(type="str", required=False, aliases=["type"]),
        device=dict(type="str", required=False),
        asset=dict(type="str", required=False),
        asset_id=dict(type="int", required=False),
        enduser=dict(type="str", required=False),
        date_gt=dict(type="str", required=False),
        date_lt=dict(type="str", required=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.params["event_id"] is not None and any(
        [
            module.params["event_type"] is not None,
            module.params["device"] is not None,
            module.params["asset"] is not None,
            module.params["asset_id"] is not None,
            module.params["enduser"] is not None,
            module.params["date_gt"] is not None,
            module.params["date_lt"] is not None,
        ]
    ):
        module.fail_json(msg="event_id endpoint is separate from list filters; use either event_id or list filters.")

    helper = d42_asset_device_lifecycle(
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

    if module.params["event_id"] is not None:
        result["api_lifecycle_event"] = helper.d42_get_lifecycle_event_by_id(
            event_id=module.params["event_id"]
        )
    else:
        result["api_lifecycle_events"] = helper.d42_get_lifecycle_events(
            event_type=module.params["event_type"],
            device=module.params["device"],
            asset=module.params["asset"],
            asset_id=module.params["asset_id"],
            enduser=module.params["enduser"],
            date_gt=module.params["date_gt"],
            date_lt=module.params["date_lt"],
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
