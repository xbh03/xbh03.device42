#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_buildings
short_description: Manage Device42 buildings
description:
    - Create, update, or delete Device42 buildings.
    - Supports C(POST /api/1.0/buildings/), C(DELETE /api/1.0/buildings/{id}/),
        and C(PUT /api/1.0/custom_fields/building/).
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
            - Desired state of the building.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    present_endpoint:
        description:
            - Endpoint used when C(state=present).
            - C(post) uses C(/api/1.0/buildings/).
            - C(custom_fields) uses C(/api/1.0/custom_fields/building/).
        required: false
        type: str
        default: post
        choices:
            - post
            - custom_fields
    force_update:
        description:
            - Force update call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    building_id:
        description:
            - Building ID.
        required: false
        type: int
    name:
        description:
            - Building name.
        required: false
        type: str
    latitude:
        description:
            - North-south position.
        required: false
        type: str
    longitude:
        description:
            - East-west position.
        required: false
        type: str
    address:
        description:
            - Building address.
        required: false
        type: str
    contact_name:
        description:
            - Building contact name.
        required: false
        type: str
    contact_phone:
        description:
            - Building contact phone.
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
    new_name:
        description:
            - New name for renaming an existing building.
        required: false
        type: str
    custom_field_key:
        description:
            - Custom field key for C(present_endpoint=custom_fields).
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
    custom_field_groups:
        description:
            - Multitenancy admin groups access string for custom field update.
        required: false
        type: str
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
- name: Create building
    xbh03.device42.buildings.d42_api_buildings:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: post
        name: main office
        latitude: "30"
        longitude: "60"
        address: 879 main st

- name: Update building
    xbh03.device42.buildings.d42_api_buildings:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        present_endpoint: post
        name: main office
        contact_name: roger
        contact_phone: "+1 555 0100"
        notes: super critical

- name: Rename building
    xbh03.device42.buildings.d42_api_buildings:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: post
        name: old office
        new_name: main office

- name: Update building custom field
    xbh03.device42.buildings.d42_api_buildings:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: custom_fields
        building_id: 3
        custom_field_key: Lifecycle
        custom_field_type: text
        custom_field_value: Active

- name: Delete building
    xbh03.device42.buildings.d42_api_buildings:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        building_id: 114
"""

RETURN = r"""
api_building:
    description: Current or resulting building data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create, update, delete, or custom field operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.buildings.d42_buildings import (
        d42_buildings,
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


def _find_building(helper, building_id=None, name=None):
        if building_id is not None:
                try:
                        return helper.d42_get_building_by_id(building_id=int(building_id))
                except Exception:
                        return None

        if name is not None:
                payload = helper.d42_get_buildings(name=name)
                for candidate in payload.get("buildings", []):
                        if str(candidate.get("name")) == str(name):
                                candidate_id = candidate.get("building_id")
                                if candidate_id is not None:
                                        return helper.d42_get_building_by_id(building_id=int(candidate_id))

        return None


def _extract_building_id_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and len(msg) > 1:
                try:
                        return int(msg[1])
                except (TypeError, ValueError):
                        return None

        for key in ("building_id", "id"):
                if response.get(key) is not None:
                        try:
                                return int(response.get(key))
                        except (TypeError, ValueError):
                                return None

        return None


def _existing_value(existing, payload_key):
        if payload_key == "new_name":
                return existing.get("name")
        return existing.get(payload_key)


def _equal_value(desired, current, key):
        if desired is None:
                return True

        if key == "tags":
                desired_set = set(_normalize_multi_value(desired))
                current_set = set(_normalize_multi_value(current))
                return desired_set == current_set

        return str(current) == str(desired)


def _needs_update(existing, payload, force_update=False):
        if force_update:
                return True

        if existing is None:
                return True

        always_change_keys = {"tags_remove", "groups"}

        for key, desired in payload.items():
                if key in always_change_keys:
                        return True

                current = _existing_value(existing, key)
                if not _equal_value(desired=desired, current=current, key=key):
                        return True

        return False


def _build_post_payload(params):
        keys = [
                "name",
                "latitude",
                "longitude",
                "address",
                "contact_name",
                "contact_phone",
                "notes",
                "groups",
                "tags",
                "tags_remove",
                "new_name",
        ]

        payload = {}
        for key in keys:
                value = params.get(key)
                if value is not None:
                        payload[key] = value

        return payload


def _build_custom_field_payload(params):
        return {
                "key": params.get("custom_field_key"),
                "building_id": params.get("building_id"),
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
                "groups": params.get("custom_field_groups"),
                "bulk_fields": params.get("custom_field_bulk_fields"),
                "multi_select": params.get("custom_field_multi_select"),
        }


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
                present_endpoint=dict(type="str", required=False, default="post", choices=["post", "custom_fields"]),
                force_update=dict(type="bool", required=False, default=False),
                building_id=dict(type="int", required=False),
                name=dict(type="str", required=False),
                latitude=dict(type="str", required=False),
                longitude=dict(type="str", required=False),
                address=dict(type="str", required=False),
                contact_name=dict(type="str", required=False),
                contact_phone=dict(type="str", required=False),
                notes=dict(type="str", required=False),
                groups=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_remove=dict(type="str", required=False),
                new_name=dict(type="str", required=False),
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
                custom_field_groups=dict(type="str", required=False),
                custom_field_bulk_fields=dict(type="str", required=False),
                custom_field_multi_select=dict(type="str", required=False, choices=["yes", "no"]),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_buildings(
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

        lookup_name = module.params["name"]
        existing = _find_building(
                helper=helper,
                building_id=module.params["building_id"],
                name=lookup_name,
        )

        if state == "absent":
                if module.params["building_id"] is None:
                        module.fail_json(msg="building_id is required when state=absent.")

                if existing is None:
                        result["msg"] = "Building already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_building"] = existing

                if module.check_mode:
                        result["msg"] = "Building would be deleted"
                        module.exit_json(**result)

                response = helper.d42_delete_building(building_id=module.params["building_id"])
                result["response"] = response
                module.exit_json(**result)

        if present_endpoint == "custom_fields":
                cf_payload = _build_custom_field_payload(module.params)
                if not cf_payload.get("key"):
                        module.fail_json(msg="custom_field_key is required when present_endpoint=custom_fields.")
                if cf_payload.get("building_id") is None and cf_payload.get("name") is None:
                        module.fail_json(msg="building_id or name is required when present_endpoint=custom_fields.")

                result["changed"] = True
                if module.check_mode:
                        result["msg"] = "Building custom fields would be updated"
                        if existing is not None:
                                result["api_building"] = existing
                        module.exit_json(**result)

                response = helper.d42_put_custom_field_building(**cf_payload)
                result["response"] = response

                resolved_id = cf_payload.get("building_id")
                if resolved_id is None:
                        resolved_id = _extract_building_id_from_response(response)
                if resolved_id is not None:
                        result["api_building"] = _find_building(helper=helper, building_id=resolved_id)
                else:
                        result["api_building"] = _find_building(helper=helper, name=cf_payload.get("name"))
                module.exit_json(**result)

        post_payload = _build_post_payload(module.params)
        if module.params["name"] is None:
                module.fail_json(msg="name is required when present_endpoint=post.")
        if not post_payload:
                module.fail_json(msg="At least one parameter is required when present_endpoint=post.")

        needs_change = _needs_update(
                existing=existing,
                payload=post_payload,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_building"] = existing
                result["msg"] = "Building already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Building would be created/updated"
                if existing is not None:
                        result["api_building"] = existing
                module.exit_json(**result)

        response = helper.d42_post_buildings(**post_payload)
        result["response"] = response

        resolved_id = _extract_building_id_from_response(response)
        if resolved_id is not None:
                result["api_building"] = _find_building(helper=helper, building_id=resolved_id)
        else:
                final_name = module.params["new_name"] or module.params["name"]
                result["api_building"] = _find_building(helper=helper, name=final_name)

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
