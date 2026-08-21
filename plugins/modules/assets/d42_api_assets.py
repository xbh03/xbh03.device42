#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_assets
short_description: Manage Device42 assets
description:
    - Create, update, or delete Device42 assets.
    - Supports C(POST /api/1.0/assets/), C(PUT /api/1.0/assets/), C(PUT /api/1.0/assets/{id}/),
        C(DELETE /api/1.0/assets/{id}/), and C(PUT /api/1.0/custom_fields/asset/).
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
            - Desired state of the asset.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    present_endpoint:
        description:
            - Endpoint used when C(state=present).
            - C(post) uses C(/api/1.0/assets/).
            - C(put) uses C(/api/1.0/assets/) modify mode.
            - C(put_by_id) uses C(/api/1.0/assets/{id}/).
            - C(custom_fields) uses C(/api/1.0/custom_fields/asset/).
        required: false
        type: str
        default: post
        choices:
            - post
            - put
            - put_by_id
            - custom_fields
    force_update:
        description:
            - Force update call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    asset_id:
        description:
            - Asset ID.
        required: false
        type: int
    asset:
        description:
            - Asset name identifier used by C(PUT /api/1.0/assets/).
        required: false
        type: str
    name:
        description:
            - Asset name.
        required: false
        type: str
    asset_type:
        description:
            - Asset type.
        required: false
        type: str
    service_level:
        description:
            - Service level name.
        required: false
        type: str
    back_connection_type:
        description:
            - Back connection type.
        required: false
        type: str
    tap_module_model_id:
        description:
            - Tap module model ID.
        required: false
        type: int
    tap_module_model:
        description:
            - Tap module model name.
        required: false
        type: str
    tap_module_host_id:
        description:
            - Tap module host ID.
        required: false
        type: int
    tap_module_host:
        description:
            - Tap module host name.
        required: false
        type: str
    object_category:
        description:
            - Object category.
        required: false
        type: str
    new_object_category:
        description:
            - New object category.
        required: false
        type: str
    storage_room:
        description:
            - Storage room name.
        required: false
        type: str
    in_service:
        description:
            - In service status.
        required: false
        type: str
        choices:
            - yes
            - no
    device_ids:
        description:
            - Comma-separated related device IDs.
        required: false
        type: str
    device_name:
        description:
            - Related device name.
        required: false
        type: str
    reversed:
        description:
            - Whether the asset is reversed in rack.
        required: false
        type: str
        choices:
            - yes
            - no
    building:
        description:
            - Building name.
        required: false
        type: str
    serial_no:
        description:
            - Asset serial number.
        required: false
        type: str
    asset_no:
        description:
            - Asset number.
        required: false
        type: str
    customer:
        description:
            - Customer name.
        required: false
        type: str
    storage_room_id:
        description:
            - Storage room ID.
        required: false
        type: int
    location:
        description:
            - Location or region.
        required: false
        type: str
    notes:
        description:
            - Asset notes.
        required: false
        type: str
    vendor:
        description:
            - Vendor name.
        required: false
        type: str
    imgfile_id:
        description:
            - Front image file ID.
        required: false
        type: int
    img:
        description:
            - Front image filename.
        required: false
        type: str
    back_image_id:
        description:
            - Back image file ID.
        required: false
        type: int
    back_image:
        description:
            - Back image filename.
        required: false
        type: str
    rack:
        description:
            - Rack name.
        required: false
        type: str
    rack_id:
        description:
            - Rack ID.
        required: false
        type: int
    start_at:
        description:
            - U start location.
        required: false
        type: str
    size:
        description:
            - Asset rack size in U.
        required: false
        type: int
    orientation:
        description:
            - Orientation in rack.
        required: false
        type: str
    where:
        description:
            - Rack placement location.
        required: false
        type: str
    x_pos:
        description:
            - X position in rack units.
        required: false
        type: int
    depth:
        description:
            - Depth value.
        required: false
        type: str
    device_id:
        description:
            - Related device ID.
        required: false
        type: int
    tags:
        description:
            - Comma-separated tags to add/set.
        required: false
        type: str
    tags_remove:
        description:
            - Comma-separated tags to remove.
        required: false
        type: str
    patch_panel_model_id:
        description:
            - Patch panel model ID.
        required: false
        type: int
    patch_panel_model:
        description:
            - Patch panel model name.
        required: false
        type: str
    numbering_start_from:
        description:
            - Starting number for patch panel ports.
        required: false
        type: int
    patch_panel_module_model_id:
        description:
            - Patch panel module model ID.
        required: false
        type: int
    patch_panel_module_model:
        description:
            - Patch panel module model name.
        required: false
        type: str
    module_host_id:
        description:
            - Module host ID.
        required: false
        type: int
    module_host:
        description:
            - Module host name.
        required: false
        type: str
    slot_no:
        description:
            - Slot number.
        required: false
        type: int
    width_ratio:
        description:
            - Width ratio.
        required: false
        type: str
    category:
        description:
            - Category used by C(PUT /api/1.0/assets/{id}/).
        required: false
        type: str
    custom_field_key:
        description:
            - Custom field key for C(custom_fields).
        required: false
        type: str
    custom_field_type:
        description:
            - Custom field type.
        required: false
        type: str
    custom_field_mandatory:
        description:
            - Whether custom field is mandatory, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_filterable:
        description:
            - Whether custom field is filterable, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_log_for_api:
        description:
            - Whether custom field is logged for API, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_related_field_name:
        description:
            - Related field name for related_field custom type.
        required: false
        type: str
    custom_field_add_to_picklist:
        description:
            - Comma-separated values to add to picklist.
        required: false
        type: str
    custom_field_remove_from_picklist:
        description:
            - Comma-separated values to remove from picklist.
        required: false
        type: str
    custom_field_delete_in_use:
        description:
            - Delete in-use picklist values, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_related_field_value_by_id:
        description:
            - Set related field by ID, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_value:
        description:
            - Custom field value.
        required: false
        type: str
    custom_field_clear_value:
        description:
            - Clear custom field value, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_notes:
        description:
            - Custom field notes.
        required: false
        type: str
    custom_field_clear_notes:
        description:
            - Clear custom field notes, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    custom_field_bulk_fields:
        description:
            - Bulk custom key:value pairs.
        required: false
        type: str
    custom_field_multi_select:
        description:
            - Picklist multi-select, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
"""

EXAMPLES = r"""
- name: Create asset using POST endpoint
    xbh03.device42.d42_api_assets:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: post
        asset_type: Patch Panel
        name: test_api_asset

- name: Modify asset using PUT endpoint by asset name
    xbh03.device42.d42_api_assets:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        present_endpoint: put
        asset: test_api_asset
        notes: Managed by Ansible

- name: Modify asset using PUT by ID endpoint
    xbh03.device42.d42_api_assets:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: put_by_id
        asset_id: 54
        category: Prod_East

- name: Update asset custom field
    xbh03.device42.d42_api_assets:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: custom_fields
        asset_id: 54
        custom_field_key: Lifecycle
        custom_field_type: text
        custom_field_value: Active

- name: Delete asset by ID
    xbh03.device42.d42_api_assets:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        asset_id: 54
"""

RETURN = r"""
api_asset:
    description: Current or resulting asset data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create, update, delete, or custom field operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.assets.d42_assets import (
        d42_assets,
)


def _normalize_multi_value(value):
        if value is None:
                return []
        if isinstance(value, (list, tuple, set)):
                items = value
        else:
                items = str(value).split(",")

        normalized = []
        for item in items:
                text = str(item).strip()
                if text:
                        normalized.append(text)

        seen = set()
        result = []
        for item in normalized:
                if item not in seen:
                        seen.add(item)
                        result.append(item)
        return result


def _find_asset(helper, asset_id=None, name=None, asset_no=None, serial_no=None):
        if asset_id is not None:
                try:
                        return helper.d42_get_asset_by_id(asset_id=int(asset_id))
                except Exception:
                        return None

        if asset_no is not None:
                payload = helper.d42_get_assets(asset_no=asset_no, limit=100, offset=0)
                for candidate in payload.get("assets", []):
                        if candidate.get("asset_no") == asset_no:
                                candidate_id = candidate.get("asset_id")
                                if candidate_id is not None:
                                        return helper.d42_get_asset_by_id(asset_id=int(candidate_id))

        if serial_no is not None:
                payload = helper.d42_get_assets(serial_no=serial_no, limit=100, offset=0)
                for candidate in payload.get("assets", []):
                        if candidate.get("serial_no") == serial_no:
                                candidate_id = candidate.get("asset_id")
                                if candidate_id is not None:
                                        return helper.d42_get_asset_by_id(asset_id=int(candidate_id))

        if name is not None:
                payload = helper.d42_get_assets(limit=1000, offset=0)
                for candidate in payload.get("assets", []):
                        if candidate.get("name") == name:
                                candidate_id = candidate.get("asset_id")
                                if candidate_id is not None:
                                        return helper.d42_get_asset_by_id(asset_id=int(candidate_id))

        return None


def _resolve_asset_id(candidate, fallback=None):
        if isinstance(candidate, dict):
                for key in ("asset_id", "id"):
                        if candidate.get(key) is not None:
                                try:
                                        return int(candidate.get(key))
                                except (TypeError, ValueError):
                                        pass

        if fallback is not None:
                try:
                        return int(fallback)
                except (TypeError, ValueError):
                        return None

        return None


def _extract_asset_id_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and msg:
                first = msg[0]
                if isinstance(first, list) and len(first) > 1:
                        try:
                                return int(first[1])
                        except (TypeError, ValueError):
                                return None

        for key in ("asset_id", "id"):
                if response.get(key) is not None:
                        try:
                                return int(response.get(key))
                        except (TypeError, ValueError):
                                return None

        return None


def _build_asset_payload(params, include_asset_name=False, include_category=False):
        keys = [
                "name",
                "asset_type",
                "service_level",
                "back_connection_type",
                "tap_module_model_id",
                "tap_module_model",
                "tap_module_host_id",
                "tap_module_host",
                "object_category",
                "new_object_category",
                "storage_room",
                "in_service",
                "device_ids",
                "device_name",
                "reversed",
                "building",
                "serial_no",
                "asset_no",
                "customer",
                "storage_room_id",
                "location",
                "notes",
                "vendor",
                "imgfile_id",
                "img",
                "back_image_id",
                "back_image",
                "rack",
                "rack_id",
                "start_at",
                "size",
                "orientation",
                "where",
                "x_pos",
                "depth",
                "device_id",
                "tags",
                "tags_remove",
                "patch_panel_model_id",
                "patch_panel_model",
                "numbering_start_from",
                "patch_panel_module_model_id",
                "patch_panel_module_model",
                "module_host_id",
                "module_host",
                "slot_no",
                "width_ratio",
        ]

        payload = {}
        for key in keys:
                value = params.get(key)
                if value is not None:
                        payload[key] = value

        if include_asset_name and params.get("asset") is not None:
                payload["asset"] = params.get("asset")

        if include_category and params.get("category") is not None:
                payload["category"] = params.get("category")

        return payload


def _existing_value(existing, payload_key):
        alias_map = {
                "asset_type": ["type", "asset_type"],
                "x_pos": ["x_pos", "xpos"],
                "imgfile_id": ["imgfile_id", "imagefile_id"],
        }

        for key in alias_map.get(payload_key, [payload_key]):
                if key in existing:
                        return existing.get(key)
        return None


def _equal_value(desired, current, key):
        if desired is None:
                return True

        if isinstance(desired, str) and desired.lower() == "d42null":
                return current in (None, "", "null")

        list_like_keys = {"tags", "tags_remove", "device_ids"}
        if key in list_like_keys:
                desired_set = set(_normalize_multi_value(desired))
                current_set = set(_normalize_multi_value(current))
                return desired_set == current_set

        int_like_keys = {
                "asset_id",
                "tap_module_model_id",
                "tap_module_host_id",
                "storage_room_id",
                "imgfile_id",
                "back_image_id",
                "rack_id",
                "size",
                "x_pos",
                "device_id",
                "patch_panel_model_id",
                "numbering_start_from",
                "patch_panel_module_model_id",
                "module_host_id",
                "slot_no",
        }
        if key in int_like_keys:
                try:
                        return int(current) == int(desired)
                except (TypeError, ValueError):
                        return False

        return str(current) == str(desired)


def _needs_update(existing, payload, force_update=False):
        if force_update:
                return True

        if existing is None:
                return True

        always_change_keys = {
                "tags_remove",
                "new_object_category",
                "custom_field_key",
        }

        for key, desired in payload.items():
                if key in always_change_keys:
                        return True

                current = _existing_value(existing, key)
                if not _equal_value(desired=desired, current=current, key=key):
                        return True

        return False


def _build_custom_field_payload(params):
        payload = {
                "key": params.get("custom_field_key"),
                "asset_id": params.get("asset_id"),
                "name": params.get("name"),
                "type": params.get("custom_field_type"),
                "mandatory": params.get("custom_field_mandatory"),
                "filterable": params.get("custom_field_filterable"),
                "log_for_api": params.get("custom_field_log_for_api"),
                "related_field_name": params.get("custom_field_related_field_name"),
                "add_to_picklist": params.get("custom_field_add_to_picklist"),
                "remove_from_picklist": params.get("custom_field_remove_from_picklist"),
                "delete_in_use": params.get("custom_field_delete_in_use"),
                "related_field_value_by_id": params.get("custom_field_related_field_value_by_id"),
                "value": params.get("custom_field_value"),
                "clear_value": params.get("custom_field_clear_value"),
                "notes": params.get("custom_field_notes"),
                "clear_notes": params.get("custom_field_clear_notes"),
                "bulk_fields": params.get("custom_field_bulk_fields"),
                "multi_select": params.get("custom_field_multi_select"),
        }

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
                present_endpoint=dict(type="str", required=False, default="post", choices=["post", "put", "put_by_id", "custom_fields"]),
                force_update=dict(type="bool", required=False, default=False),
                asset_id=dict(type="int", required=False),
                asset=dict(type="str", required=False),
                name=dict(type="str", required=False),
                asset_type=dict(type="str", required=False),
                service_level=dict(type="str", required=False),
                back_connection_type=dict(type="str", required=False),
                tap_module_model_id=dict(type="int", required=False),
                tap_module_model=dict(type="str", required=False),
                tap_module_host_id=dict(type="int", required=False),
                tap_module_host=dict(type="str", required=False),
                object_category=dict(type="str", required=False),
                new_object_category=dict(type="str", required=False),
                storage_room=dict(type="str", required=False),
                in_service=dict(type="str", required=False, choices=["yes", "no"]),
                device_ids=dict(type="str", required=False),
                device_name=dict(type="str", required=False),
                reversed=dict(type="str", required=False, choices=["yes", "no"]),
                building=dict(type="str", required=False),
                serial_no=dict(type="str", required=False),
                asset_no=dict(type="str", required=False),
                customer=dict(type="str", required=False),
                storage_room_id=dict(type="int", required=False),
                location=dict(type="str", required=False),
                notes=dict(type="str", required=False),
                vendor=dict(type="str", required=False),
                imgfile_id=dict(type="int", required=False),
                img=dict(type="str", required=False),
                back_image_id=dict(type="int", required=False),
                back_image=dict(type="str", required=False),
                rack=dict(type="str", required=False),
                rack_id=dict(type="int", required=False),
                start_at=dict(type="str", required=False),
                size=dict(type="int", required=False),
                orientation=dict(type="str", required=False),
                where=dict(type="str", required=False),
                x_pos=dict(type="int", required=False),
                depth=dict(type="str", required=False),
                device_id=dict(type="int", required=False),
                tags=dict(type="str", required=False),
                tags_remove=dict(type="str", required=False),
                patch_panel_model_id=dict(type="int", required=False),
                patch_panel_model=dict(type="str", required=False),
                numbering_start_from=dict(type="int", required=False),
                patch_panel_module_model_id=dict(type="int", required=False),
                patch_panel_module_model=dict(type="str", required=False),
                module_host_id=dict(type="int", required=False),
                module_host=dict(type="str", required=False),
                slot_no=dict(type="int", required=False),
                width_ratio=dict(type="str", required=False),
                category=dict(type="str", required=False),
                custom_field_key=dict(type="str", required=False),
                custom_field_type=dict(type="str", required=False),
                custom_field_mandatory=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_filterable=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_log_for_api=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_related_field_name=dict(type="str", required=False),
                custom_field_add_to_picklist=dict(type="str", required=False),
                custom_field_remove_from_picklist=dict(type="str", required=False),
                custom_field_delete_in_use=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_related_field_value_by_id=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_value=dict(type="str", required=False),
                custom_field_clear_value=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_notes=dict(type="str", required=False),
                custom_field_clear_notes=dict(type="str", required=False, choices=["yes", "no"]),
                custom_field_bulk_fields=dict(type="str", required=False),
                custom_field_multi_select=dict(type="str", required=False, choices=["yes", "no"]),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_assets(
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

        lookup_name = module.params["name"] or module.params["asset"]
        existing = _find_asset(
                helper=helper,
                asset_id=module.params["asset_id"],
                name=lookup_name,
                asset_no=module.params["asset_no"],
                serial_no=module.params["serial_no"],
        )

        if state == "absent":
                resolved_asset_id = _resolve_asset_id(existing, fallback=module.params["asset_id"])
                if resolved_asset_id is None:
                        result["msg"] = "Asset already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_asset"] = existing

                if module.check_mode:
                        result["msg"] = "Asset would be deleted"
                        module.exit_json(**result)

                response = helper.d42_delete_asset(asset_id=resolved_asset_id)
                result["response"] = response
                module.exit_json(**result)

        if present_endpoint == "custom_fields":
                cf_payload = _build_custom_field_payload(module.params)
                if not cf_payload.get("key"):
                        module.fail_json(msg="custom_field_key is required when present_endpoint=custom_fields.")
                if cf_payload.get("asset_id") is None and cf_payload.get("name") is None:
                        module.fail_json(msg="asset_id or name is required when present_endpoint=custom_fields.")

                result["changed"] = True
                if module.check_mode:
                        result["msg"] = "Asset custom fields would be updated"
                        if existing is not None:
                                result["api_asset"] = existing
                        module.exit_json(**result)

                response = helper.d42_put_custom_field_asset(**cf_payload)
                result["response"] = response

                resolved_asset_id = _resolve_asset_id(existing, fallback=module.params["asset_id"])
                if resolved_asset_id is None:
                        resolved_asset_id = _extract_asset_id_from_response(response)
                if resolved_asset_id is not None:
                        result["api_asset"] = helper.d42_get_asset_by_id(asset_id=resolved_asset_id)
                else:
                        result["api_asset"] = existing
                module.exit_json(**result)

        post_payload = _build_asset_payload(module.params)
        put_payload = _build_asset_payload(module.params, include_asset_name=True)
        put_by_id_payload = _build_asset_payload(module.params, include_category=True)

        if present_endpoint == "post":
                if not post_payload:
                        module.fail_json(msg="At least one parameter is required when present_endpoint=post.")
                if existing is None and post_payload.get("asset_type") is None:
                        module.fail_json(msg="asset_type is required to create a new asset when present_endpoint=post.")
                payload_for_drift = post_payload
        elif present_endpoint == "put":
                if not put_payload:
                        module.fail_json(msg="At least one parameter is required when present_endpoint=put.")
                if module.params["asset_id"] is None and module.params["asset"] is None:
                        module.fail_json(msg="asset_id or asset is required when present_endpoint=put.")
                payload_for_drift = put_payload
        else:
                if not put_by_id_payload:
                        module.fail_json(msg="At least one parameter is required when present_endpoint=put_by_id.")
                if module.params["asset_id"] is None:
                        module.fail_json(msg="asset_id is required when present_endpoint=put_by_id.")
                payload_for_drift = put_by_id_payload

        needs_change = _needs_update(
                existing=existing,
                payload=payload_for_drift,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_asset"] = existing
                result["msg"] = "Asset already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Asset would be created/updated"
                if existing is not None:
                        result["api_asset"] = existing
                module.exit_json(**result)

        if present_endpoint == "post":
                response = helper.d42_post_assets(**post_payload)
        elif present_endpoint == "put":
                response = helper.d42_put_assets_modify(
                        asset_id=module.params["asset_id"],
                        **put_payload,
                )
        else:
                response = helper.d42_put_asset_by_id(
                        asset_id=module.params["asset_id"],
                        **put_by_id_payload,
                )

        result["response"] = response

        resolved_asset_id = _extract_asset_id_from_response(response)
        if resolved_asset_id is None:
                resolved_asset_id = _resolve_asset_id(existing, fallback=module.params["asset_id"])

        if resolved_asset_id is not None:
                result["api_asset"] = helper.d42_get_asset_by_id(asset_id=resolved_asset_id)
        else:
                result["api_asset"] = _find_asset(
                        helper=helper,
                        asset_id=module.params["asset_id"],
                        name=lookup_name,
                        asset_no=module.params["asset_no"],
                        serial_no=module.params["serial_no"],
                )

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
