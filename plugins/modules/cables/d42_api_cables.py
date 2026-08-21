#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_cables
short_description: Manage Device42 cables
description:
    - Create, update, or delete Device42 cables.
    - Supports C(POST /api/1.0/cables/) and C(DELETE /api/1.0/cables/{id}/).
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
            - Desired state of the cable.
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
    cable_pk:
        description:
            - Device42 numeric cable ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [id]
    cable_id:
        description:
            - Cable ID/Name.
            - Required when C(state=present).
        required: false
        type: str
    vendor:
        description:
            - Cable vendor.
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
    room_id:
        description:
            - Room ID.
        required: false
        type: int
    room:
        description:
            - Room name.
        required: false
        type: str
    origin_clear:
        description:
            - Option to clean up cable origin, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    origin_type:
        description:
            - Type of origin point.
        required: false
        type: str
        choices:
            - cable
            - circuit
            - switchport
            - tap_port
            - patch_panel_port
    origin_id:
        description:
            - ID of origin point. Must be used with C(origin_type).
        required: false
        type: int
    origin_connector_type:
        description:
            - Origin connector type.
        required: false
        type: str
    origin_cable_type:
        description:
            - Origin cable type.
        required: false
        type: str
    origin_cable_color:
        description:
            - Origin cable color.
        required: false
        type: str
    origin_optic_type:
        description:
            - Origin optic type.
        required: false
        type: str
    origin_back_patch_panel:
        description:
            - Origin back patch panel flag.
        required: false
        type: str
    end_clear:
        description:
            - Option to clean up cable endpoint, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    end_point_type:
        description:
            - Type of end point.
        required: false
        type: str
        choices:
            - cable
            - circuit
            - switchport
            - tap_port
            - patch_panel_port
            - vendor
    end_point_id:
        description:
            - ID of end point. Must be used with C(end_point_type).
        required: false
        type: int
    end_connector_type:
        description:
            - End connector type.
        required: false
        type: str
    end_cable_type:
        description:
            - End cable type.
        required: false
        type: str
    end_cable_color:
        description:
            - End cable color.
        required: false
        type: str
    end_optic_type:
        description:
            - End optic type.
        required: false
        type: str
    end_point_back_patch_panel:
        description:
            - End back patch panel flag.
        required: false
        type: str
    end_point_multiple:
        description:
            - Allow multiple endpoints, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    cable_length:
        description:
            - Cable length.
        required: false
        type: str
    cable_length_units:
        description:
            - Cable length units.
        required: false
        type: str
        choices:
            - m
            - ft
"""

EXAMPLES = r"""
- name: Create cable
    xbh03.device42.cables.d42_api_cables:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        cable_id: Fiber 1:Multi
        origin_type: switchport
        origin_id: 899
        end_point_type: cable
        end_point_id: 3

- name: Update cable by numeric ID
    xbh03.device42.cables.d42_api_cables:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        cable_pk: 9
        cable_id: Cable #9 [new Cable]
        vendor: MyVendor
        notes: Updated by Ansible

- name: Delete cable
    xbh03.device42.cables.d42_api_cables:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        cable_pk: 89
"""

RETURN = r"""
api_cable:
    description: Current or resulting cable data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.cables.d42_cables import (
        d42_cables,
)


def _extract_cable_pk_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and len(msg) > 1:
                try:
                        return int(msg[1])
                except (TypeError, ValueError):
                        return None

        for key in ("id", "cable_pk"):
                if response.get(key) is not None:
                        try:
                                return int(response.get(key))
                        except (TypeError, ValueError):
                                return None

        return None


def _get_cables(helper, cable_id=None):
        payload = helper.d42_get_cables(cable_id=cable_id)
        cables = payload.get("cable", [])
        return cables if isinstance(cables, list) else []


def _find_cable(helper, cable_pk=None, cable_id=None):
        if cable_pk is not None:
                for cable in _get_cables(helper):
                        try:
                                if int(cable.get("id")) == int(cable_pk):
                                        return cable
                        except (TypeError, ValueError):
                                continue

        if cable_id is not None:
                for cable in _get_cables(helper, cable_id=cable_id):
                        if str(cable.get("cable_id")) == str(cable_id):
                                return cable

        return None


def _existing_value(existing, payload_key):
        alias_map = {
                "end_point_back_patch_panel": ["end_point_back_patch_panel", "end_back_patch_panel"],
                "origin_back_patch_panel": ["origin_back_patch_panel"],
                "cable_pk": ["id"],
        }

        for key in alias_map.get(payload_key, [payload_key]):
                if key in existing:
                        return existing.get(key)
        return None


def _needs_update(existing, payload, force_update=False):
        if force_update:
                return True

        if existing is None:
                return True

        always_change_keys = {"groups", "origin_clear", "end_clear"}

        for key, desired in payload.items():
                if key == "id":
                        continue
                if key in always_change_keys:
                        return True

                current = _existing_value(existing, key)
                if str(current) != str(desired):
                        return True

        return False


def _build_post_payload(params):
        keys = [
                "id",
                "cable_id",
                "vendor",
                "notes",
                "groups",
                "room_id",
                "room",
                "origin_clear",
                "origin_type",
                "origin_id",
                "origin_connector_type",
                "origin_cable_type",
                "origin_cable_color",
                "origin_optic_type",
                "origin_back_patch_panel",
                "end_clear",
                "end_point_type",
                "end_point_id",
                "end_connector_type",
                "end_cable_type",
                "end_cable_color",
                "end_optic_type",
                "end_point_back_patch_panel",
                "end_point_multiple",
                "cable_length",
                "cable_length_units",
        ]

        payload = {}
        for key in keys:
                value = params.get(key)
                if value is not None:
                        payload[key] = value

        return payload


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
                cable_pk=dict(type="int", required=False, aliases=["id"]),
                cable_id=dict(type="str", required=False),
                vendor=dict(type="str", required=False),
                notes=dict(type="str", required=False),
                groups=dict(type="str", required=False),
                room_id=dict(type="int", required=False),
                room=dict(type="str", required=False),
                origin_clear=dict(type="str", required=False, choices=["yes", "no"]),
                origin_type=dict(type="str", required=False, choices=["cable", "circuit", "switchport", "tap_port", "patch_panel_port"]),
                origin_id=dict(type="int", required=False),
                origin_connector_type=dict(type="str", required=False),
                origin_cable_type=dict(type="str", required=False),
                origin_cable_color=dict(type="str", required=False),
                origin_optic_type=dict(type="str", required=False),
                origin_back_patch_panel=dict(type="str", required=False),
                end_clear=dict(type="str", required=False, choices=["yes", "no"]),
                end_point_type=dict(type="str", required=False, choices=["cable", "circuit", "switchport", "tap_port", "patch_panel_port", "vendor"]),
                end_point_id=dict(type="int", required=False),
                end_connector_type=dict(type="str", required=False),
                end_cable_type=dict(type="str", required=False),
                end_cable_color=dict(type="str", required=False),
                end_optic_type=dict(type="str", required=False),
                end_point_back_patch_panel=dict(type="str", required=False),
                end_point_multiple=dict(type="str", required=False, choices=["yes", "no"]),
                cable_length=dict(type="str", required=False),
                cable_length_units=dict(type="str", required=False, choices=["m", "ft"]),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_cables(
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

        if (module.params["origin_type"] is None) ^ (module.params["origin_id"] is None):
                module.fail_json(msg="origin_type and origin_id must be provided together.")
        if (module.params["end_point_type"] is None) ^ (module.params["end_point_id"] is None):
                module.fail_json(msg="end_point_type and end_point_id must be provided together.")

        state = module.params["state"]

        existing = _find_cable(
                helper=helper,
                cable_pk=module.params["cable_pk"],
                cable_id=module.params["cable_id"],
        )

        if state == "absent":
                if module.params["cable_pk"] is None:
                        module.fail_json(msg="cable_pk (or id) is required when state=absent.")

                if existing is None:
                        result["msg"] = "Cable already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_cable"] = existing

                if module.check_mode:
                        result["msg"] = "Cable would be deleted"
                        module.exit_json(**result)

                response = helper.d42_delete_cable(cable_pk=module.params["cable_pk"])
                result["response"] = response
                module.exit_json(**result)

        if module.params["cable_id"] is None:
                module.fail_json(msg="cable_id is required when state=present.")

        post_payload = _build_post_payload(
                {
                        "id": module.params["cable_pk"],
                        "cable_id": module.params["cable_id"],
                        "vendor": module.params["vendor"],
                        "notes": module.params["notes"],
                        "groups": module.params["groups"],
                        "room_id": module.params["room_id"],
                        "room": module.params["room"],
                        "origin_clear": module.params["origin_clear"],
                        "origin_type": module.params["origin_type"],
                        "origin_id": module.params["origin_id"],
                        "origin_connector_type": module.params["origin_connector_type"],
                        "origin_cable_type": module.params["origin_cable_type"],
                        "origin_cable_color": module.params["origin_cable_color"],
                        "origin_optic_type": module.params["origin_optic_type"],
                        "origin_back_patch_panel": module.params["origin_back_patch_panel"],
                        "end_clear": module.params["end_clear"],
                        "end_point_type": module.params["end_point_type"],
                        "end_point_id": module.params["end_point_id"],
                        "end_connector_type": module.params["end_connector_type"],
                        "end_cable_type": module.params["end_cable_type"],
                        "end_cable_color": module.params["end_cable_color"],
                        "end_optic_type": module.params["end_optic_type"],
                        "end_point_back_patch_panel": module.params["end_point_back_patch_panel"],
                        "end_point_multiple": module.params["end_point_multiple"],
                        "cable_length": module.params["cable_length"],
                        "cable_length_units": module.params["cable_length_units"],
                }
        )

        needs_change = _needs_update(
                existing=existing,
                payload=post_payload,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_cable"] = existing
                result["msg"] = "Cable already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Cable would be created/updated"
                if existing is not None:
                        result["api_cable"] = existing
                module.exit_json(**result)

        response = helper.d42_post_cables(**post_payload)
        result["response"] = response

        resolved_cable_pk = _extract_cable_pk_from_response(response)
        if resolved_cable_pk is None:
                resolved_cable_pk = module.params["cable_pk"]

        result["api_cable"] = _find_cable(
                helper=helper,
                cable_pk=resolved_cable_pk,
                cable_id=module.params["cable_id"],
        )

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
