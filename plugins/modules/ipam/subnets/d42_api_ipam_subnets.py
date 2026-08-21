#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_subnets
short_description: Manage Device42 IPAM subnets
description:
    - Create, update, or delete Device42 subnets.
    - Supports C(POST /api/1.0/subnets/), C(PUT /api/1.0/subnets/), and C(DELETE /api/1.0/subnets/{subnet_id}/).
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
            - Desired state of the subnet.
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
    subnet_id:
        description:
            - Device42 subnet ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [id]
    merge_associated:
        description:
            - For C(state=absent), merge child subnets/IPs into parent when C(yes).
        required: false
        type: str
        choices:
            - yes
            - no
    network:
        description:
            - Subnet network address.
            - Required for creation when C(subnet_id) is not provided.
        required: false
        type: str
    mask_bits:
        description:
            - Subnet mask bits.
            - Required for creation when C(subnet_id) is not provided.
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
    name:
        description:
            - Subnet display name.
        required: false
        type: str
    type:
        description:
            - Subnet type.
        required: false
        type: str
        choices:
            - Static
            - DHCP
            - Reserved
            - D42_NULL
    type_id:
        description:
            - Subnet type ID.
        required: false
        type: int
    service_level:
        description:
            - Service level name.
        required: false
        type: str
    service_level_id:
        description:
            - Service level ID.
        required: false
        type: int
    description:
        description:
            - Subnet description.
        required: false
        type: str
    gateway:
        description:
            - Gateway.
        required: false
        type: str
    range_begin:
        description:
            - IP range begin.
        required: false
        type: str
    range_end:
        description:
            - IP range end.
        required: false
        type: str
    parent_vlan_id:
        description:
            - Parent VLAN ID.
        required: false
        type: str
    parent_subnet_id:
        description:
            - Parent subnet ID.
        required: false
        type: str
    customer_id:
        description:
            - Customer ID.
        required: false
        type: str
    notes:
        description:
            - Additional notes.
        required: false
        type: str
    assigned:
        description:
            - Mark subnet as assigned.
        required: false
        type: str
        choices:
            - yes
            - no
    allocated:
        description:
            - Mark subnet as allocated.
        required: false
        type: str
        choices:
            - yes
            - no
    auto_add_ips:
        description:
            - Automatically add IPs in range (POST endpoint support).
        required: false
        type: str
        choices:
            - yes
            - no
    category:
        description:
            - Category or multitenancy access string.
        required: false
        type: str
    new_category:
        description:
            - New category name to replace existing category.
        required: false
        type: str
    category_id:
        description:
            - Category ID.
        required: false
        type: str
    new_category_id:
        description:
            - New category ID to replace existing category ID.
        required: false
        type: str
    parent_subnet_name:
        description:
            - Parent subnet name.
        required: false
        type: str
    parent_subnet:
        description:
            - Parent subnet in C(network/mask) format.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create subnet
    xbh03.device42.ipam.subnets.d42_api_ipam_subnets:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        network: 10.10.10.0
        mask_bits: "24"
        name: Infra
        service_level: Production

- name: Update subnet by ID
    xbh03.device42.ipam.subnets.d42_api_ipam_subnets:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        subnet_id: 4
        description: Infrastructure Devices
        gateway: 10.10.10.1

- name: Delete subnet and merge children
    xbh03.device42.ipam.subnets.d42_api_ipam_subnets:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        subnet_id: 114
        merge_associated: yes
"""

RETURN = r"""
api_subnet:
    description: Current or resulting subnet data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete operations.
    type: dict
    returned: when changed
"""

import re

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.subnets.d42_ipam_subnets import (
    d42_ipam_subnets,
)


def _extract_subnet_id_from_response(response):
    if not isinstance(response, dict):
        return None

    msg = response.get("msg")
    if isinstance(msg, list):
        for item in msg:
            try:
                return int(item)
            except (TypeError, ValueError):
                if isinstance(item, str):
                    match = re.search(r"'?(\\d+)'?", item)
                    if match is not None:
                        return int(match.group(1))

    if response.get("id") is not None:
        try:
            return int(response.get("id"))
        except (TypeError, ValueError):
            return None

    return None


def _get_subnet_by_id(helper, subnet_id):
    if subnet_id is None:
        return None

    payload = helper.d42_get_subnet_by_id(subnet_id=subnet_id)
    if isinstance(payload, dict) and payload.get("subnet_id") is not None:
        return payload

    return None


def _find_subnet(helper, subnet_id=None, network=None, mask_bits=None, vrf_group_id=None, vrf_group=None):
    if subnet_id is not None:
        return _get_subnet_by_id(helper, subnet_id=subnet_id)

    if network is None:
        return None

    payload = helper.d42_get_subnets(
        network=network,
        mask_bits=mask_bits,
        vrf_group_id=vrf_group_id,
        vrf_group=vrf_group,
        limit=100,
        offset=0,
    )
    entries = payload.get("subnets", []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        return None

    for entry in entries:
        if str(entry.get("network")) != str(network):
            continue
        if mask_bits is not None and str(entry.get("mask_bits")) != str(mask_bits):
            continue
        if vrf_group_id is not None and str(entry.get("vrf_group_id")) != str(vrf_group_id):
            continue
        if vrf_group is not None:
            entry_vrf = entry.get("vrf_group") or entry.get("vrf_group_name")
            if str(entry_vrf) != str(vrf_group):
                continue
        return entry

    return None


def _build_payload(params):
    return {
        "network": params.get("network"),
        "mask_bits": params.get("mask_bits"),
        "vrf_group_id": params.get("vrf_group_id"),
        "vrf_group": params.get("vrf_group"),
        "name": params.get("name"),
        "subnet_type": params.get("type"),
        "type_id": params.get("type_id"),
        "service_level": params.get("service_level"),
        "service_level_id": params.get("service_level_id"),
        "description": params.get("description"),
        "gateway": params.get("gateway"),
        "range_begin": params.get("range_begin"),
        "range_end": params.get("range_end"),
        "parent_vlan_id": params.get("parent_vlan_id"),
        "parent_subnet_id": params.get("parent_subnet_id"),
        "customer_id": params.get("customer_id"),
        "notes": params.get("notes"),
        "assigned": params.get("assigned"),
        "allocated": params.get("allocated"),
        "auto_add_ips": params.get("auto_add_ips"),
        "category": params.get("category"),
        "new_category": params.get("new_category"),
        "category_id": params.get("category_id"),
        "new_category_id": params.get("new_category_id"),
        "parent_subnet_name": params.get("parent_subnet_name"),
        "parent_subnet": params.get("parent_subnet"),
    }


def _needs_update(existing, payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    for desired_key, existing_key in (
        ("vrf_group_id", "vrf_group_id"),
        ("vrf_group", "vrf_group_name"),
        ("name", "name"),
        ("subnet_type", "type"),
        ("type_id", "type_id"),
        ("service_level", "service_level"),
        ("service_level_id", "service_level_id"),
        ("description", "description"),
        ("gateway", "gateway"),
        ("range_begin", "range_begin"),
        ("range_end", "range_end"),
        ("parent_vlan_id", "parent_vlan_id"),
        ("parent_subnet_id", "parent_subnet_id"),
        ("customer_id", "customer_id"),
        ("notes", "notes"),
        ("assigned", "assigned"),
        ("allocated", "allocated"),
        ("category", "category_name"),
        ("category_id", "category_id"),
    ):
        desired = payload.get(desired_key)
        if desired is None:
            continue
        current = existing.get(existing_key)
        if str(current) != str(desired):
            return True

    for operation_key in ("auto_add_ips", "new_category", "new_category_id", "parent_subnet_name", "parent_subnet"):
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
        subnet_id=dict(type="int", required=False, aliases=["id"]),
        merge_associated=dict(type="str", required=False, choices=["yes", "no"]),
        network=dict(type="str", required=False),
        mask_bits=dict(type="str", required=False),
        vrf_group_id=dict(type="int", required=False),
        vrf_group=dict(type="str", required=False),
        name=dict(type="str", required=False),
        type=dict(type="str", required=False, choices=["Static", "DHCP", "Reserved", "D42_NULL"]),
        type_id=dict(type="int", required=False),
        service_level=dict(type="str", required=False),
        service_level_id=dict(type="int", required=False),
        description=dict(type="str", required=False),
        gateway=dict(type="str", required=False),
        range_begin=dict(type="str", required=False),
        range_end=dict(type="str", required=False),
        parent_vlan_id=dict(type="str", required=False),
        parent_subnet_id=dict(type="str", required=False),
        customer_id=dict(type="str", required=False),
        notes=dict(type="str", required=False),
        assigned=dict(type="str", required=False, choices=["yes", "no"]),
        allocated=dict(type="str", required=False, choices=["yes", "no"]),
        auto_add_ips=dict(type="str", required=False, choices=["yes", "no"]),
        category=dict(type="str", required=False),
        new_category=dict(type="str", required=False),
        category_id=dict(type="str", required=False),
        new_category_id=dict(type="str", required=False),
        parent_subnet_name=dict(type="str", required=False),
        parent_subnet=dict(type="str", required=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    helper = d42_ipam_subnets(
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
    subnet_id = module.params["subnet_id"]

    if state == "absent":
        if subnet_id is None:
            module.fail_json(msg="subnet_id (or id) is required when state=absent.")

        existing = _find_subnet(helper=helper, subnet_id=subnet_id)
        if existing is None:
            result["msg"] = "Subnet already absent"
            module.exit_json(**result)

        result["changed"] = True
        result["api_subnet"] = existing

        if module.check_mode:
            result["msg"] = "Subnet would be deleted"
            module.exit_json(**result)

        result["response"] = helper.d42_delete_subnet(
            subnet_id=subnet_id,
            merge_associated=module.params["merge_associated"],
        )
        module.exit_json(**result)

    if subnet_id is None and (module.params["network"] is None or module.params["mask_bits"] is None):
        module.fail_json(msg="network and mask_bits are required when state=present and subnet_id is not provided.")

    payload = _build_payload(module.params)
    existing = _find_subnet(
        helper=helper,
        subnet_id=subnet_id,
        network=module.params["network"],
        mask_bits=module.params["mask_bits"],
        vrf_group_id=module.params["vrf_group_id"],
        vrf_group=module.params["vrf_group"],
    )

    if not _needs_update(existing=existing, payload=payload, force_update=module.params["force_update"]):
        result["api_subnet"] = existing
        result["msg"] = "Subnet already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Subnet would be created/updated"
        if existing is not None:
            result["api_subnet"] = existing
        module.exit_json(**result)

    target_subnet_id = subnet_id or (existing or {}).get("subnet_id")

    if target_subnet_id is not None:
        put_payload = dict(payload)
        put_payload.pop("network", None)
        put_payload.pop("mask_bits", None)
        result["response"] = helper.d42_put_subnets(id=target_subnet_id, **put_payload)
    else:
        result["response"] = helper.d42_post_subnets(**payload)

    resolved_id = _extract_subnet_id_from_response(result["response"])
    if resolved_id is None:
        resolved_id = target_subnet_id

    if resolved_id is not None:
        result["api_subnet"] = _find_subnet(helper=helper, subnet_id=resolved_id)
    else:
        result["api_subnet"] = _find_subnet(
            helper=helper,
            network=module.params["network"],
            mask_bits=module.params["mask_bits"],
            vrf_group_id=module.params["vrf_group_id"],
            vrf_group=module.params["vrf_group"],
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
