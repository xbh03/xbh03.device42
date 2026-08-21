#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_rooms
short_description: Manage Device42 rooms
description:
    - Create, update, or delete Device42 rooms.
    - Supports C(POST /api/1.0/rooms/), C(PUT /api/1.0/rooms/{ID}/),
        and C(DELETE /api/1.0/rooms/{ID}/).
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
            - Desired state of the room.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    present_endpoint:
        description:
            - Endpoint used when C(state=present).
            - C(post) uses C(POST /api/1.0/rooms/) to create or update by name.
            - C(put) uses C(PUT /api/1.0/rooms/{ID}/) to update an existing room by ID.
        required: false
        type: str
        default: post
        choices:
            - post
            - put
    force_update:
        description:
            - Force update call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    room_id:
        description:
            - Room numeric ID.
            - Required when C(state=absent) or C(present_endpoint=put).
        required: false
        type: int
        aliases: [id]
    name:
        description:
            - Room name.
            - Required when C(present_endpoint=post).
        required: false
        type: str
    building_id:
        description:
            - Existing building ID.
            - Required with C(present_endpoint=post) if C(building) is not provided for new rooms.
        required: false
        type: int
    building:
        description:
            - Existing building name.
            - Required with C(present_endpoint=post) if C(building_id) is not provided for new rooms.
        required: false
        type: str
    notes:
        description:
            - Additional notes.
        required: false
        type: str
    horizontal_grid_numbering:
        description:
            - Horizontal grid numbering style.
        required: false
        type: str
        choices:
            - numeric
            - alphabetic
            - alphabetic_doubled
    horizontal_grid_start:
        description:
            - Starting value for horizontal grid numbering.
        required: false
        type: str
    vertical_grid_numbering:
        description:
            - Vertical grid numbering style.
        required: false
        type: str
        choices:
            - numeric
            - alphabetic
            - alphabetic_doubled
    vertical_grid_start:
        description:
            - Starting value for vertical grid numbering.
        required: false
        type: str
    uom:
        description:
            - Unit of measurement, C(m) for meters or C(in) for inches.
        required: false
        type: str
        choices:
            - m
            - in
    height:
        description:
            - Room height.
        required: false
        type: str
    grid_rows:
        description:
            - Number of rows in the room grid.
        required: false
        type: str
    grid_cols:
        description:
            - Number of columns in the room grid.
        required: false
        type: str
    raised_floor:
        description:
            - Whether the room has a raised floor, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    raised_floor_height:
        description:
            - Height of the raised floor.
        required: false
        type: str
    groups:
        description:
            - Multitenancy admin groups access string.
        required: false
        type: str
    reverse_xaxis:
        description:
            - Reverse numbering on the x-axis, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    reverse_yaxis:
        description:
            - Reverse numbering on the y-axis, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    tags:
        description:
            - Comma-separated tags to add.
        required: false
        type: str
    tags_remove:
        description:
            - Comma-separated tags to remove.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create room
    xbh03.device42.rooms.d42_rooms:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: 1st floor
        building: New Haven DC
        grid_rows: "9"
        grid_cols: "10"

- name: Update room by ID
    xbh03.device42.rooms.d42_rooms:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        present_endpoint: put
        room_id: 7
        notes: Updated by Ansible
        raised_floor: yes
        raised_floor_height: "0.5"

- name: Delete room
    xbh03.device42.rooms.d42_rooms:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        room_id: 114
"""

RETURN = r"""
api_room:
    description: Current or resulting room data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.rooms.d42_rooms import (
        d42_rooms,
)


def _extract_room_id_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and len(msg) > 1:
                try:
                        return int(msg[1])
                except (TypeError, ValueError):
                        return None

        for key in ("room_id", "id"):
                if response.get(key) is not None:
                        try:
                                return int(response.get(key))
                        except (TypeError, ValueError):
                                return None

        return None


def _get_room_by_id(helper, room_id):
        payload = helper.d42_get_room_by_id(room_id=room_id)
        return payload if isinstance(payload, dict) else None


def _find_room_by_name(helper, name, building_id=None, building=None):
        payload = helper.d42_get_rooms(name=name, building_id=building_id, building=building)
        rooms = payload.get("rooms", []) if isinstance(payload, dict) else []
        for room in rooms:
                if str(room.get("name")) == str(name):
                        candidate_id = room.get("room_id")
                        if candidate_id is not None:
                                return _get_room_by_id(helper, room_id=int(candidate_id))
        return None


def _find_room(helper, room_id=None, name=None, building_id=None, building=None):
        if room_id is not None:
                return _get_room_by_id(helper, room_id=room_id)
        if name is not None:
                return _find_room_by_name(helper, name=name, building_id=building_id, building=building)
        return None


def _needs_update(existing, params, force_update=False):
        if force_update or existing is None:
                return True

        if params.get("tags_remove") is not None or params.get("groups") is not None:
                return True

        for key in (
                "name",
                "notes",
                "building_id",
                "horizontal_grid_numbering",
                "horizontal_grid_start",
                "vertical_grid_numbering",
                "vertical_grid_start",
                "uom",
                "height",
                "grid_rows",
                "grid_cols",
                "raised_floor",
                "raised_floor_height",
                "reverse_xaxis",
                "reverse_yaxis",
        ):
            desired = params.get(key)
            if desired is None:
                    continue
            if str(existing.get(key)) != str(desired):
                    return True

        return False


def _build_payload(params):
        payload = {}
        for key in (
                "name",
                "building_id",
                "building",
                "notes",
                "horizontal_grid_numbering",
                "horizontal_grid_start",
                "vertical_grid_numbering",
                "vertical_grid_start",
                "uom",
                "height",
                "grid_rows",
                "grid_cols",
                "raised_floor",
                "raised_floor_height",
                "groups",
                "reverse_xaxis",
                "reverse_yaxis",
                "tags",
                "tags_remove",
        ):
            if params.get(key) is not None:
                    payload[key] = params.get(key)
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
                present_endpoint=dict(type="str", required=False, default="post", choices=["post", "put"]),
                force_update=dict(type="bool", required=False, default=False),
                room_id=dict(type="int", required=False, aliases=["id"]),
                name=dict(type="str", required=False),
                building_id=dict(type="int", required=False),
                building=dict(type="str", required=False),
                notes=dict(type="str", required=False),
                horizontal_grid_numbering=dict(type="str", required=False, choices=["numeric", "alphabetic", "alphabetic_doubled"]),
                horizontal_grid_start=dict(type="str", required=False),
                vertical_grid_numbering=dict(type="str", required=False, choices=["numeric", "alphabetic", "alphabetic_doubled"]),
                vertical_grid_start=dict(type="str", required=False),
                uom=dict(type="str", required=False, choices=["m", "in"]),
                height=dict(type="str", required=False),
                grid_rows=dict(type="str", required=False),
                grid_cols=dict(type="str", required=False),
                raised_floor=dict(type="str", required=False, choices=["yes", "no"]),
                raised_floor_height=dict(type="str", required=False),
                groups=dict(type="str", required=False),
                reverse_xaxis=dict(type="str", required=False, choices=["yes", "no"]),
                reverse_yaxis=dict(type="str", required=False, choices=["yes", "no"]),
                tags=dict(type="str", required=False),
                tags_remove=dict(type="str", required=False),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_rooms(
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
        present_endpoint = module.params["present_endpoint"]
        room_id = module.params["room_id"]

        existing = _find_room(
                helper=helper,
                room_id=room_id,
                name=module.params["name"],
                building_id=module.params["building_id"],
                building=module.params["building"],
        )

        # --- state=absent ---
        if state == "absent":
                if room_id is None:
                        module.fail_json(msg="room_id (or id) is required when state=absent.")

                if existing is None:
                        result["msg"] = "Room already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_room"] = existing

                if module.check_mode:
                        result["msg"] = "Room would be deleted"
                        module.exit_json(**result)

                result["response"] = helper.d42_delete_room(room_id=room_id)
                module.exit_json(**result)

        # --- state=present, present_endpoint=put ---
        if present_endpoint == "put":
                if room_id is None:
                        module.fail_json(msg="room_id (or id) is required when present_endpoint=put.")

                payload = _build_payload(module.params)
                # name not required for PUT
                payload.pop("name", None) if module.params["name"] is None else None

                needs_change = _needs_update(
                        existing=existing,
                        params=module.params,
                        force_update=module.params["force_update"],
                )

                if not needs_change:
                        result["api_room"] = existing
                        result["msg"] = "Room already in desired state"
                        module.exit_json(**result)

                result["changed"] = True
                if module.check_mode:
                        result["msg"] = "Room would be updated"
                        if existing is not None:
                                result["api_room"] = existing
                        module.exit_json(**result)

                # build PUT-specific payload (excludes building/building_id per API spec)
                put_payload = {k: v for k, v in payload.items() if k not in ("building",)}
                response = helper.d42_put_room(room_id=room_id, **put_payload)
                result["response"] = response
                result["api_room"] = _find_room(helper=helper, room_id=room_id)
                module.exit_json(**result)

        # --- state=present, present_endpoint=post ---
        if module.params["name"] is None:
                module.fail_json(msg="name is required when present_endpoint=post.")

        if existing is None and module.params["building_id"] is None and module.params["building"] is None:
                module.fail_json(msg="building_id or building is required when creating a new room.")

        post_payload = _build_payload(module.params)
        needs_change = _needs_update(
                existing=existing,
                params=module.params,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_room"] = existing
                result["msg"] = "Room already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Room would be created/updated"
                if existing is not None:
                        result["api_room"] = existing
                module.exit_json(**result)

        response = helper.d42_post_rooms(**post_payload)
        result["response"] = response

        resolved_room_id = _extract_room_id_from_response(response)
        if resolved_room_id is None:
                resolved_room_id = room_id

        result["api_room"] = _find_room(
                helper=helper,
                room_id=resolved_room_id,
                name=module.params["name"],
                building_id=module.params["building_id"],
                building=module.params["building"],
        )
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
