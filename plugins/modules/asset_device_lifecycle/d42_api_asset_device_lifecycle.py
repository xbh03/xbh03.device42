#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_asset_device_lifecycle
short_description: Manage Device42 asset and device lifecycle events
description:
    - Create, update, or delete lifecycle events for Device42 assets and devices.
    - Uses PUT C(/api/1.0/lifecycle_event/) for create/update and DELETE C(/api/1.0/lifecycle_event/{id}/).
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
    state:
        description:
            - Desired state of the lifecycle event.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    event_id:
        description:
            - Lifecycle event ID.
            - Required when C(state=absent).
        required: false
        type: int
    date:
        description:
            - Lifecycle event date in C(YYYY-MM-DD) or C(YYYY-MM-DD HH:MM).
        required: false
        type: str
    new_date:
        description:
            - New date to overwrite current lifecycle event date.
        required: false
        type: str
    event_type:
        description:
            - Lifecycle event type. Must already exist in Device42.
        required: false
        type: str
    device:
        description:
            - Device name targeted by the lifecycle event.
        required: false
        type: str
    device_id:
        description:
            - Device ID targeted by the lifecycle event.
        required: false
        type: int
    asset_no:
        description:
            - Asset number of the targeted device.
        required: false
        type: str
    serial_no:
        description:
            - Serial number of the targeted device.
        required: false
        type: str
    asset_id:
        description:
            - Asset ID targeted by the lifecycle event.
        required: false
        type: int
    fully_qualified_username:
        description:
            - Fully qualified username.
        required: false
        type: str
    tags:
        description:
            - Comma-separated tags to add to the lifecycle event.
        required: false
        type: str
    tags_remove:
        description:
            - Comma-separated tags to remove from the lifecycle event.
        required: false
        type: str
    enduser_id:
        description:
            - End user ID.
        required: false
        type: int
    user:
        description:
            - End user name.
        required: false
        type: str
    notes:
        description:
            - Additional notes for the lifecycle event.
        required: false
        type: str
    force_update:
        description:
            - Force PUT update when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Create lifecycle event for a device
    xbh03.device42.d42_api_asset_device_lifecycle:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        date: 2024-01-01
        event_type: Purchased
        device: app-server-01
        notes: Purchased for production cluster

- name: Update lifecycle event by ID
    xbh03.device42.d42_api_asset_device_lifecycle:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        event_id: 4
        new_date: 2024-01-15
        event_type: Installed

- name: Delete lifecycle event
    xbh03.device42.d42_api_asset_device_lifecycle:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        event_id: 4
"""

RETURN = r"""
api_lifecycle_event:
    description: Current or resulting lifecycle event data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create, update, or delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.asset_device_lifecycle.d42_asset_device_lifecycle import (
    d42_asset_device_lifecycle,
)


def _existing_event_payload(existing):
    if isinstance(existing, dict) and isinstance(existing.get("lifecycle_event"), dict):
        return existing.get("lifecycle_event")
    return existing


def _needs_update(existing, desired_params, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    current = _existing_event_payload(existing)
    if not isinstance(current, dict):
        return True

    for key, desired_value in desired_params.items():
        if desired_value is None:
            continue

        existing_key = key
        if key == "event_type":
            existing_key = "type"

        if existing_key not in current:
            continue

        if current.get(existing_key) != desired_value:
            return True

    return False


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
        state=dict(type="str", required=False, default="present", choices=["present", "absent"]),
        event_id=dict(type="int", required=False),
        date=dict(type="str", required=False),
        new_date=dict(type="str", required=False),
        event_type=dict(type="str", required=False),
        device=dict(type="str", required=False),
        device_id=dict(type="int", required=False),
        asset_no=dict(type="str", required=False),
        serial_no=dict(type="str", required=False),
        asset_id=dict(type="int", required=False),
        fully_qualified_username=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        tags_remove=dict(type="str", required=False),
        enduser_id=dict(type="int", required=False),
        user=dict(type="str", required=False),
        notes=dict(type="str", required=False),
        force_update=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

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

    state = module.params["state"]
    event_id = module.params["event_id"]

    if state == "absent":
        if event_id is None:
            module.fail_json(msg="event_id is required when state=absent.")

        result["changed"] = True
        if module.check_mode:
            result["msg"] = "Lifecycle event would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_lifecycle_event(event_id=event_id)
        result["response"] = response
        module.exit_json(**result)

    existing = None
    if event_id is not None:
        existing = helper.d42_get_lifecycle_event_by_id(event_id=event_id)

    needs_change = _needs_update(
        existing=existing,
        desired_params=dict(
            event_type=module.params["event_type"],
            date=module.params["date"],
            new_date=module.params["new_date"],
            device=module.params["device"],
            device_id=module.params["device_id"],
            asset_no=module.params["asset_no"],
            serial_no=module.params["serial_no"],
            asset_id=module.params["asset_id"],
            fully_qualified_username=module.params["fully_qualified_username"],
            tags=module.params["tags"],
            tags_remove=module.params["tags_remove"],
            enduser_id=module.params["enduser_id"],
            user=module.params["user"],
            notes=module.params["notes"],
        ),
        force_update=module.params["force_update"],
    )

    if not needs_change:
        result["api_lifecycle_event"] = _existing_event_payload(existing)
        result["msg"] = "Lifecycle event already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Lifecycle event would be created/updated"
        if existing is not None:
            result["api_lifecycle_event"] = _existing_event_payload(existing)
        module.exit_json(**result)

    response = helper.d42_put_lifecycle_event(
        event_id=event_id,
        date=module.params["date"],
        new_date=module.params["new_date"],
        event_type=module.params["event_type"],
        device=module.params["device"],
        device_id=module.params["device_id"],
        asset_no=module.params["asset_no"],
        serial_no=module.params["serial_no"],
        asset_id=module.params["asset_id"],
        fully_qualified_username=module.params["fully_qualified_username"],
        tags=module.params["tags"],
        tags_remove=module.params["tags_remove"],
        enduser_id=module.params["enduser_id"],
        user=module.params["user"],
        notes=module.params["notes"],
    )
    result["response"] = response

    if event_id is not None:
        result["api_lifecycle_event"] = _existing_event_payload(
            helper.d42_get_lifecycle_event_by_id(event_id=event_id)
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
