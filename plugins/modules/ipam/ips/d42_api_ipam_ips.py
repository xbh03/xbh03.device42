#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_ips
short_description: Manage Device42 IPAM IP addresses
description:
    - Create, update, or delete Device42 IP addresses.
    - Supports C(POST /api/2.0/ips/) and C(DELETE /api/1.0/ips/{id}/).
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
            - Desired state of the IP address.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    force_update:
        description:
            - Force POST call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    id:
        description:
            - Device42 IP address ID.
            - Required when C(state=absent).
        required: false
        type: int
    ipaddress:
        description:
            - IP address.
            - Required when C(state=present).
        required: false
        type: str
    label:
        description:
            - Label for the interface.
        required: false
        type: str
    subnet:
        description:
            - Subnet unique name. Used for new IP creation when VRF is not provided.
        required: false
        type: str
    macaddress:
        description:
            - MAC address.
        required: false
        type: str
    type:
        description:
            - IP allocation type.
        required: false
        type: str
        choices:
            - static
            - dhcp
            - reserved
    notes:
        description:
            - Additional notes.
        required: false
        type: str
    vrf_group_id:
        description:
            - VRF group ID.
        required: false
        type: int
    vrf_group:
        description:
            - VRF group name.
        required: false
        type: str
    available:
        description:
            - Mark IP availability.
        required: false
        type: str
        choices:
            - yes
            - no
    clear_all:
        description:
            - Clear device and MAC associations and reset label/notes when C(yes).
        required: false
        type: str
        choices:
            - yes
            - no
    tags:
        description:
            - Update IP address tags.
        required: false
        type: str
    devices:
        description:
            - Comma-separated device names to associate.
        required: false
        type: str
    device_ids:
        description:
            - Comma-separated device IDs to associate.
        required: false
        type: str
    remove_devices:
        description:
            - Comma-separated device names to remove, or C(*) to remove all.
        required: false
        type: str
    remove_device_ids:
        description:
            - Comma-separated device IDs to remove, or C(*) to remove all.
        required: false
        type: str
    locked:
        description:
            - Lock or unlock passed device mappings.
        required: false
        type: str
        choices:
            - yes
            - no
"""

EXAMPLES = r"""
- name: Create or update IP address
    xbh03.device42.ipam.ips.d42_api_ipam_ips:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        ipaddress: 192.168.1.10
        label: app-vip
        vrf_group: production
        devices: app01,app02

- name: Mark IP available and clear associations
    xbh03.device42.ipam.ips.d42_api_ipam_ips:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        ipaddress: 192.168.1.10
        available: yes
        clear_all: yes

- name: Delete IP by ID
    xbh03.device42.ipam.ips.d42_api_ipam_ips:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        id: 114
"""

RETURN = r"""
api_ip:
    description: Current or resulting IP address data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.ips.d42_ipam_ips import (
    d42_ipam_ips,
)


def _extract_ip_id_from_response(response):
    if not isinstance(response, dict):
        return None

    msg = response.get("msg")
    if isinstance(msg, list) and len(msg) > 1:
        try:
            return int(msg[1])
        except (TypeError, ValueError):
            return None

    if response.get("id") is not None:
        try:
            return int(response.get("id"))
        except (TypeError, ValueError):
            return None

    return None


def _find_existing_ip(helper, ipaddress, vrf_group_id=None, vrf_group=None):
    payload = helper.d42_get_ips(ipaddress=ipaddress)
    entries = payload.get("ips", []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        return None

    for entry in entries:
        if str(entry.get("ipaddress")) != str(ipaddress):
            continue

        if vrf_group_id is not None and str(entry.get("vrf_group_id")) != str(vrf_group_id):
            continue

        if vrf_group is not None:
            entry_vrf = entry.get("vrf_group") or entry.get("vrf")
            if str(entry_vrf) != str(vrf_group):
                continue

        return entry

    return None


def _build_post_payload(params):
    payload = {
        "ipaddress": params.get("ipaddress"),
        "label": params.get("label"),
        "subnet": params.get("subnet"),
        "macaddress": params.get("macaddress"),
        "ip_type": params.get("type"),
        "notes": params.get("notes"),
        "vrf_group_id": params.get("vrf_group_id"),
        "vrf_group": params.get("vrf_group"),
        "available": params.get("available"),
        "clear_all": params.get("clear_all"),
        "tags": params.get("tags"),
        "devices": params.get("devices"),
        "device_ids": params.get("device_ids"),
        "remove_devices": params.get("remove_devices"),
        "remove_device_ids": params.get("remove_device_ids"),
        "locked": params.get("locked"),
    }
    return payload


def _needs_update(existing, payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    for key in (
        "label",
        "macaddress",
        "type",
        "notes",
        "available",
        "tags",
    ):
        desired = payload.get("ip_type") if key == "type" else payload.get(key)
        if desired is None:
            continue

        current = existing.get(key)
        if str(current) != str(desired):
            return True

    for operation_key in ("clear_all", "devices", "device_ids", "remove_devices", "remove_device_ids", "locked"):
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
        id=dict(type="int", required=False),
        ipaddress=dict(type="str", required=False),
        label=dict(type="str", required=False),
        subnet=dict(type="str", required=False),
        macaddress=dict(type="str", required=False),
        type=dict(type="str", required=False, choices=["static", "dhcp", "reserved"]),
        notes=dict(type="str", required=False),
        vrf_group_id=dict(type="int", required=False),
        vrf_group=dict(type="str", required=False),
        available=dict(type="str", required=False, choices=["yes", "no"]),
        clear_all=dict(type="str", required=False, choices=["yes", "no"]),
        tags=dict(type="str", required=False),
        devices=dict(type="str", required=False),
        device_ids=dict(type="str", required=False),
        remove_devices=dict(type="str", required=False),
        remove_device_ids=dict(type="str", required=False),
        locked=dict(type="str", required=False, choices=["yes", "no"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    helper = d42_ipam_ips(
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
    ip_id = module.params["id"]
    ipaddress = module.params["ipaddress"]

    if state == "absent":
        if ip_id is None:
            module.fail_json(msg="id is required when state=absent.")

        result["changed"] = True
        result["api_ip"] = {"id": ip_id}

        if module.check_mode:
            result["msg"] = "IP address would be deleted"
            module.exit_json(**result)

        result["response"] = helper.d42_delete_ip_by_id(id=ip_id)
        module.exit_json(**result)

    if ipaddress is None:
        module.fail_json(msg="ipaddress is required when state=present.")

    post_payload = _build_post_payload(module.params)
    existing = _find_existing_ip(
        helper=helper,
        ipaddress=ipaddress,
        vrf_group_id=module.params["vrf_group_id"],
        vrf_group=module.params["vrf_group"],
    )

    needs_change = _needs_update(
        existing=existing,
        payload=post_payload,
        force_update=module.params["force_update"],
    )

    if not needs_change:
        result["api_ip"] = existing
        result["msg"] = "IP address already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "IP address would be created/updated"
        if existing is not None:
            result["api_ip"] = existing
        module.exit_json(**result)

    response = helper.d42_post_ips(**post_payload)
    result["response"] = response

    resolved_id = _extract_ip_id_from_response(response)
    result["api_ip"] = _find_existing_ip(
        helper=helper,
        ipaddress=ipaddress,
        vrf_group_id=module.params["vrf_group_id"],
        vrf_group=module.params["vrf_group"],
    )
    if result["api_ip"] is None and resolved_id is not None:
        result["api_ip"] = {"id": resolved_id, "ipaddress": ipaddress}

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
