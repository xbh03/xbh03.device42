#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_vlans
short_description: Manage Device42 IPAM VLANs
description:
    - Create, update, or delete Device42 VLANs.
    - Supports C(POST /api/1.0/vlans/), C(PUT /api/1.0/vlans/), C(PUT /api/1.0/vlans/{id}/), and C(DELETE /api/1.0/vlans/{id}/).
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
            - Desired state of the VLAN.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    force_update:
        description:
            - Force update call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    id:
        description:
            - Device42 VLAN ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [vlan_id]
    number:
        description:
            - VLAN number.
            - Required when C(state=present) and C(id) is not provided.
        required: false
        type: int
    name:
        description:
            - VLAN name.
        required: false
        type: str
    description:
        description:
            - VLAN description.
        required: false
        type: str
    switch_ids:
        description:
            - Comma separated switch IDs.
        required: false
        type: str
    switches:
        description:
            - Comma separated switch names.
        required: false
        type: str
    clear_switches:
        description:
            - Comma separated switch names to remove.
        required: false
        type: str
    clear_switch_ids:
        description:
            - Comma separated switch IDs to remove.
        required: false
        type: str
    tags:
        description:
            - Add or update VLAN tags.
        required: false
        type: str
    notes:
        description:
            - Additional notes.
        required: false
        type: str
    groups:
        description:
            - Multitenancy admin groups access string.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create VLAN
    xbh03.device42.ipam.vlans.d42_api_ipam_vlans:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        number: 342
        name: CRMConsultant

- name: Update VLAN by ID (id in URL)
    xbh03.device42.ipam.vlans.d42_api_ipam_vlans:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        id: 13
        description: Updated by Ansible

- name: Update VLAN and clear switch mapping (id in form)
    xbh03.device42.ipam.vlans.d42_api_ipam_vlans:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        id: 13
        clear_switch_ids: 1,2

- name: Delete VLAN
    xbh03.device42.ipam.vlans.d42_api_ipam_vlans:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        id: 114
"""

RETURN = r"""
api_vlan:
    description: Current or resulting VLAN data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.vlans.d42_ipam_vlans import (
    d42_ipam_vlans,
)


def _extract_vlan_id_from_response(response):
    if not isinstance(response, dict):
        return None

    msg = response.get("msg")
    if isinstance(msg, list):
        for item in msg:
            try:
                return int(item)
            except (TypeError, ValueError):
                continue

    if response.get("id") is not None:
        try:
            return int(response.get("id"))
        except (TypeError, ValueError):
            return None

    return None


def _find_vlan_by_id(helper, vlan_id):
    if vlan_id is None:
        return None

    payload = helper.d42_get_vlan_by_id(id=vlan_id)
    if isinstance(payload, dict) and payload.get("vlan_id") is not None:
        return payload

    return None


def _find_vlan(helper, vlan_id=None, number=None, name=None):
    if vlan_id is not None:
        return _find_vlan_by_id(helper=helper, vlan_id=vlan_id)

    if number is None and name is None:
        return None

    payload = helper.d42_get_vlans(number=number, name=name)
    entries = payload.get("vlans", []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        return None

    for entry in entries:
        if number is not None and str(entry.get("number")) != str(number):
            continue
        if name is not None and str(entry.get("name")) != str(name):
            continue

        entry_id = entry.get("vlan_id")
        if entry_id is not None:
            return _find_vlan_by_id(helper=helper, vlan_id=entry_id)
        return entry

    return None


def _build_payload(params):
    return {
        "number": params.get("number"),
        "name": params.get("name"),
        "description": params.get("description"),
        "switch_ids": params.get("switch_ids"),
        "switches": params.get("switches"),
        "clear_switches": params.get("clear_switches"),
        "clear_switch_ids": params.get("clear_switch_ids"),
        "tags": params.get("tags"),
        "notes": params.get("notes"),
        "groups": params.get("groups"),
    }


def _needs_update(existing, payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    for desired_key, existing_key in (
        ("number", "number"),
        ("name", "name"),
        ("description", "description"),
        ("notes", "notes"),
    ):
        desired = payload.get(desired_key)
        if desired is None:
            continue

        current = existing.get(existing_key)
        if str(current) != str(desired):
            return True

    # Tag and switch/group mutations are difficult to diff reliably from list responses.
    for operation_key in (
        "switch_ids",
        "switches",
        "clear_switches",
        "clear_switch_ids",
        "tags",
        "groups",
    ):
        if payload.get(operation_key) is not None:
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
        force_update=dict(type="bool", required=False, default=False),
        id=dict(type="int", required=False, aliases=["vlan_id"]),
        number=dict(type="int", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        switch_ids=dict(type="str", required=False),
        switches=dict(type="str", required=False),
        clear_switches=dict(type="str", required=False),
        clear_switch_ids=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        notes=dict(type="str", required=False),
        groups=dict(type="str", required=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    helper = d42_ipam_vlans(
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
    vlan_id = module.params["id"]

    if state == "absent":
        if vlan_id is None:
            module.fail_json(msg="id (or vlan_id) is required when state=absent.")

        existing = _find_vlan(helper=helper, vlan_id=vlan_id)
        if existing is None:
            result["msg"] = "VLAN already absent"
            module.exit_json(**result)

        result["changed"] = True
        result["api_vlan"] = existing

        if module.check_mode:
            result["msg"] = "VLAN would be deleted"
            module.exit_json(**result)

        result["response"] = helper.d42_delete_vlan(id=vlan_id)
        module.exit_json(**result)

    if vlan_id is None and module.params["number"] is None:
        module.fail_json(msg="number is required when state=present and id is not provided.")

    payload = _build_payload(module.params)
    existing = _find_vlan(
        helper=helper,
        vlan_id=vlan_id,
        number=module.params["number"],
        name=module.params["name"],
    )

    if not _needs_update(existing=existing, payload=payload, force_update=module.params["force_update"]):
        result["api_vlan"] = existing
        result["msg"] = "VLAN already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "VLAN would be created/updated"
        if existing is not None:
            result["api_vlan"] = existing
        module.exit_json(**result)

    target_id = vlan_id
    if target_id is None and isinstance(existing, dict):
        target_id = existing.get("vlan_id")

    if target_id is None:
        # Create new VLAN.
        result["response"] = helper.d42_post_vlans(
            number=payload.get("number"),
            name=payload.get("name"),
            description=payload.get("description"),
            switch_ids=payload.get("switch_ids"),
            switches=payload.get("switches"),
            tags=payload.get("tags"),
            notes=payload.get("notes"),
            groups=payload.get("groups"),
        )
    else:
        # If clear_* parameters are used, use PUT /api/1.0/vlans/ form endpoint.
        if payload.get("clear_switches") is not None or payload.get("clear_switch_ids") is not None:
            result["response"] = helper.d42_put_vlans(
                id=target_id,
                number=payload.get("number"),
                name=payload.get("name"),
                switch_ids=payload.get("switch_ids"),
                switches=payload.get("switches"),
                clear_switches=payload.get("clear_switches"),
                clear_switch_ids=payload.get("clear_switch_ids"),
                tags=payload.get("tags"),
                description=payload.get("description"),
                notes=payload.get("notes"),
                groups=payload.get("groups"),
            )
        else:
            result["response"] = helper.d42_put_vlan_by_id(
                id=target_id,
                number=payload.get("number"),
                name=payload.get("name"),
                switch_ids=payload.get("switch_ids"),
                switches=payload.get("switches"),
                tags=payload.get("tags"),
                description=payload.get("description"),
                notes=payload.get("notes"),
                groups=payload.get("groups"),
            )

    resolved_id = _extract_vlan_id_from_response(result["response"])
    if resolved_id is None:
        resolved_id = target_id

    result["api_vlan"] = _find_vlan(helper=helper, vlan_id=resolved_id, number=module.params["number"], name=module.params["name"])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
