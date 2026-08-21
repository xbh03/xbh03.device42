#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_switchports
short_description: Manage Device42 IPAM switch ports
description:
    - Create, update, or delete Device42 switch ports.
    - Supports C(POST /api/1.0/switchports/) and C(DELETE /api/1.0/switchports/{id}/).
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
            - Desired state of the switch port.
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
            - Switch port ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [switchport_id]
    switch_port:
        description:
            - Switch port name.
            - Required when C(state=present) if C(hwaddress) is not provided.
        required: false
        type: str
        aliases: [port_name]
    port_id:
        description:
            - Existing switch port ID for updates.
        required: false
        type: int
    hwaddress:
        description:
            - MAC address or WWN.
            - Required when C(state=present) if C(switch_port) is not provided.
        required: false
        type: str
    new_port:
        description:
            - Rename existing port.
        required: false
        type: str
    switch:
        description:
            - Switch name.
        required: false
        type: str
    description:
        description:
            - Port description.
        required: false
        type: str
    type:
        description:
            - Port type.
        required: false
        type: str
    vlan_id:
        description:
            - VLAN ID.
        required: false
        type: str
    vlan:
        description:
            - Primary VLAN name.
        required: false
        type: str
    vlan_ids:
        description:
            - Comma separated VLAN IDs.
        required: false
        type: str
    vlans:
        description:
            - Comma separated VLAN names.
        required: false
        type: str
    clear_vlan_ids:
        description:
            - Comma separated VLAN IDs to remove.
        required: false
        type: str
    clear_vlans:
        description:
            - Comma separated VLAN names to remove.
        required: false
        type: str
    up:
        description:
            - Port operational status.
        required: false
        type: str
        choices:
            - yes
            - no
    up_admin:
        description:
            - Port administrative status.
        required: false
        type: str
        choices:
            - yes
            - no
    count:
        description:
            - Include the port in total count.
        required: false
        type: str
        choices:
            - yes
            - no
    remote_port_id:
        description:
            - ID of remote connected switch port.
        required: false
        type: str
    remote_device:
        description:
            - Remote connected switch name.
        required: false
        type: str
    remote_port:
        description:
            - Remote connected switch port name.
        required: false
        type: str
    module:
        description:
            - Blade module name this port belongs to.
        required: false
        type: str
    device2:
        description:
            - Device2 name this port belongs to.
        required: false
        type: str
    device:
        description:
            - Directly connected device name.
        required: false
        type: str
    label:
        description:
            - Port label.
        required: false
        type: str
    tags:
        description:
            - Add or update tags.
        required: false
        type: str
    tags_remove:
        description:
            - Remove tags.
        required: false
        type: str
    mtu:
        description:
            - MTU value.
        required: false
        type: str
    name:
        description:
            - Port name attribute.
        required: false
        type: str
    speed:
        description:
            - Port speed.
        required: false
        type: str
    remote_port_clear:
        description:
            - Clear remote port association.
        required: false
        type: str
        choices:
            - yes
            - no
    parent_port:
        description:
            - Parent port name.
        required: false
        type: str
    parent_port_device:
        description:
            - Parent port device.
        required: false
        type: str
    slave_ports:
        description:
            - Comma separated slave port names.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create switch port
    xbh03.device42.ipam.switches.d42_api_ipam_switchports:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        switch_port: child0
        switch: nh-lab-switch-01

- name: Update switch port by port_id
    xbh03.device42.ipam.switches.d42_api_ipam_switchports:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        port_id: 73685
        description: FastEthernet0/21
        tags: production,network

- name: Delete switch port by ID
    xbh03.device42.ipam.switches.d42_api_ipam_switchports:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        id: 114
"""

RETURN = r"""
api_switchport:
    description: Current or resulting switch port data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.switches.d42_ipam_switchports import (
    d42_ipam_switchports,
)


def _extract_switchport_id_from_response(response):
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


def _find_switchport_by_id(helper, switchport_id):
    if switchport_id is None:
        return None

    offset = 0
    limit = 1000
    while True:
        payload = helper.d42_get_switchports(limit=limit, offset=offset)
        switchports = payload.get("switchports", []) if isinstance(payload, dict) else []
        if not isinstance(switchports, list) or len(switchports) == 0:
            return None

        for entry in switchports:
            if str(entry.get("switchport_id")) == str(switchport_id):
                return entry

        offset += len(switchports)
        total_count = payload.get("total_count") if isinstance(payload, dict) else None
        if total_count is not None:
            try:
                if offset >= int(total_count):
                    return None
            except (TypeError, ValueError):
                pass


def _find_switchport_by_port_and_switch(helper, switch_port=None, switch=None):
    if switch_port is None:
        return None

    offset = 0
    limit = 1000
    while True:
        payload = helper.d42_get_switchports(limit=limit, offset=offset)
        switchports = payload.get("switchports", []) if isinstance(payload, dict) else []
        if not isinstance(switchports, list) or len(switchports) == 0:
            return None

        for entry in switchports:
            if str(entry.get("port")) != str(switch_port):
                continue

            if switch is not None:
                switch_obj = entry.get("switch") if isinstance(entry.get("switch"), dict) else {}
                if str(switch_obj.get("name")) != str(switch):
                    continue

            return entry

        offset += len(switchports)
        total_count = payload.get("total_count") if isinstance(payload, dict) else None
        if total_count is not None:
            try:
                if offset >= int(total_count):
                    return None
            except (TypeError, ValueError):
                pass


def _build_post_payload(params):
    return {
        "port": params.get("switch_port"),
        "port_id": params.get("port_id"),
        "hwaddress": params.get("hwaddress"),
        "new_port": params.get("new_port"),
        "switch": params.get("switch"),
        "description": params.get("description"),
        "type": params.get("type"),
        "vlan_id": params.get("vlan_id"),
        "vlan": params.get("vlan"),
        "vlan_ids": params.get("vlan_ids"),
        "vlans": params.get("vlans"),
        "clear_vlan_ids": params.get("clear_vlan_ids"),
        "clear_vlans": params.get("clear_vlans"),
        "up": params.get("up"),
        "up_admin": params.get("up_admin"),
        "count": params.get("count"),
        "remote_port_id": params.get("remote_port_id"),
        "remote_device": params.get("remote_device"),
        "remote_port": params.get("remote_port"),
        "module": params.get("module"),
        "device2": params.get("device2"),
        "device": params.get("device"),
        "label": params.get("label"),
        "tags": params.get("tags"),
        "tags_remove": params.get("tags_remove"),
        "mtu": params.get("mtu"),
        "name": params.get("name"),
        "speed": params.get("speed"),
        "remote_port_clear": params.get("remote_port_clear"),
        "parent_port": params.get("parent_port"),
        "parent_port_device": params.get("parent_port_device"),
        "slave_ports": params.get("slave_ports"),
    }


def _needs_update(existing, payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    for desired_key, existing_key in (
        ("description", "description"),
        ("type", "type"),
        ("label", "obj_label"),
    ):
        desired = payload.get(desired_key)
        if desired is None:
            continue
        current = existing.get(existing_key)
        if str(current) != str(desired):
            return True

    for operation_key in (
        "new_port",
        "vlan_id",
        "vlan",
        "vlan_ids",
        "vlans",
        "clear_vlan_ids",
        "clear_vlans",
        "up",
        "up_admin",
        "count",
        "remote_port_id",
        "remote_device",
        "remote_port",
        "module",
        "device2",
        "device",
        "tags",
        "tags_remove",
        "mtu",
        "name",
        "speed",
        "remote_port_clear",
        "parent_port",
        "parent_port_device",
        "slave_ports",
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
        id=dict(type="int", required=False, aliases=["switchport_id"]),
        switch_port=dict(type="str", required=False, aliases=["port_name"]),
        port_id=dict(type="int", required=False),
        hwaddress=dict(type="str", required=False),
        new_port=dict(type="str", required=False),
        switch=dict(type="str", required=False),
        description=dict(type="str", required=False),
        type=dict(type="str", required=False),
        vlan_id=dict(type="str", required=False),
        vlan=dict(type="str", required=False),
        vlan_ids=dict(type="str", required=False),
        vlans=dict(type="str", required=False),
        clear_vlan_ids=dict(type="str", required=False),
        clear_vlans=dict(type="str", required=False),
        up=dict(type="str", required=False, choices=["yes", "no"]),
        up_admin=dict(type="str", required=False, choices=["yes", "no"]),
        count=dict(type="str", required=False, choices=["yes", "no"]),
        remote_port_id=dict(type="str", required=False),
        remote_device=dict(type="str", required=False),
        remote_port=dict(type="str", required=False),
        module=dict(type="str", required=False),
        device2=dict(type="str", required=False),
        device=dict(type="str", required=False),
        label=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        tags_remove=dict(type="str", required=False),
        mtu=dict(type="str", required=False),
        name=dict(type="str", required=False),
        speed=dict(type="str", required=False),
        remote_port_clear=dict(type="str", required=False, choices=["yes", "no"]),
        parent_port=dict(type="str", required=False),
        parent_port_device=dict(type="str", required=False),
        slave_ports=dict(type="str", required=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    helper = d42_ipam_switchports(
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
    switchport_id = module.params["id"]
    switch_port = module.params["switch_port"]

    if state == "absent":
        if switchport_id is None:
            module.fail_json(msg="id (or switchport_id) is required when state=absent.")

        existing = _find_switchport_by_id(helper=helper, switchport_id=switchport_id)
        if existing is None:
            result["msg"] = "Switch port already absent"
            module.exit_json(**result)

        result["changed"] = True
        result["api_switchport"] = existing

        if module.check_mode:
            result["msg"] = "Switch port would be deleted"
            module.exit_json(**result)

        result["response"] = helper.d42_delete_switchport(id=switchport_id)
        module.exit_json(**result)

    if switch_port is None and module.params["hwaddress"] is None:
        module.fail_json(msg="switch_port (or hwaddress) is required when state=present.")

    payload = _build_post_payload(module.params)
    lookup_id = module.params["port_id"]
    existing = _find_switchport_by_id(helper=helper, switchport_id=lookup_id)
    if existing is None:
        existing = _find_switchport_by_port_and_switch(
            helper=helper,
            switch_port=switch_port,
            switch=module.params["switch"],
        )

    if not _needs_update(existing=existing, payload=payload, force_update=module.params["force_update"]):
        result["api_switchport"] = existing
        result["msg"] = "Switch port already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Switch port would be created/updated"
        if existing is not None:
            result["api_switchport"] = existing
        module.exit_json(**result)

    result["response"] = helper.d42_post_switchports(**payload)

    resolved_id = _extract_switchport_id_from_response(result["response"])
    if resolved_id is None:
        resolved_id = lookup_id

    result["api_switchport"] = _find_switchport_by_id(helper=helper, switchport_id=resolved_id)
    if result["api_switchport"] is None:
        result["api_switchport"] = _find_switchport_by_port_and_switch(
            helper=helper,
            switch_port=switch_port,
            switch=module.params["switch"],
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
