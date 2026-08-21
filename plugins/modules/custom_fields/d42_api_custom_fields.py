#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_custom_fields
short_description: Manage Device42 custom fields
description:
    - Create, update, or delete Device42 custom fields.
    - Supports C(PUT /api/2.0/custom_fields/) and C(DELETE /api/2.0/custom_fields/).
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
            - Desired state of the custom field.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    force_update:
        description:
            - Force PUT call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    object_name:
        description:
            - Name of the Device42 object model.
        required: true
        type: str
        choices:
            - application_group
            - application_group_calculation_rule
            - appcomp
            - appcomp_template
            - asset
            - building
            - business_service
            - cable
            - certificate
            - circuit
            - cloud_account
            - customer
            - device
            - dns_records
            - dns_zone
            - endusers
            - hardware_model
            - ip_address
            - part
            - partmodel
            - pdu
            - port
            - purchase
            - rack
            - resource
            - room
            - secret
            - service
            - service_instance
            - software
            - software_instance
            - subnet
            - vendor
            - vlan
            - vrfgroup
    id:
        description:
            - Custom field numeric ID.
            - Required with C(state=absent) if C(key) is not provided.
        required: false
        type: int
    key:
        description:
            - Custom field key/name.
            - Required with C(state=present).
            - Required with C(state=absent) if C(id) is not provided.
        required: false
        type: str
    type:
        description:
            - Custom field type used with C(state=present).
        required: false
        type: str
        choices:
            - text
            - number
            - date
            - related_field
            - boolean
            - url
            - picklist
            - json
            - markup
    mandatory:
        description:
            - Is custom field mandatory, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    filterable:
        description:
            - Is custom field filterable, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    log_for_api:
        description:
            - Log custom field, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    add_to_picklist:
        description:
            - Comma-separated values to add to picklist.
        required: false
        type: str
    remove_from_picklist:
        description:
            - Comma-separated values to remove from picklist.
        required: false
        type: str
    delete_in_use:
        description:
            - For C(state=absent), pass C(true) or C(false) to delete in-use custom fields.
            - For C(state=present), pass C(yes), C(no), C(true), or C(false) when used with C(remove_from_picklist).
        required: false
        type: str
        choices:
            - yes
            - no
            - true
            - false
    multi_select:
        description:
            - Applies only to picklist fields, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    include_in_context_popups:
        description:
            - Applies only to device custom fields, C(true) or C(false).
        required: false
        type: str
        choices:
            - true
            - false
    related_field_name:
        description:
            - Required when C(type=related_field).
        required: false
        type: str
        choices:
            - appcomp
            - building
            - businessapp
            - certificate
            - circuit
            - cloudinfrastructure
            - costcenter
            - customer
            - device
            - dns_zone
            - endusers
            - hardware
            - ip_address
            - netport
            - organisation
            - os
            - pdu
            - pdu_model
            - powercircuit
            - purchase
            - rack
            - room
            - servicecategory
            - software_category
            - software
            - vlan
"""

EXAMPLES = r"""
- name: Create custom field
    xbh03.device42.custom_fields.d42_api_custom_fields:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        object_name: device
        key: owner
        type: text
        mandatory: no
        filterable: yes

- name: Update picklist custom field
    xbh03.device42.custom_fields.d42_api_custom_fields:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        object_name: asset
        key: environment
        type: picklist
        add_to_picklist: prod,qa,dev

- name: Delete custom field by key
    xbh03.device42.custom_fields.d42_api_custom_fields:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        object_name: building
        key: room

- name: Delete custom field by id including in-use fields
    xbh03.device42.custom_fields.d42_api_custom_fields:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        object_name: device
        id: 182
        delete_in_use: true
"""

RETURN = r"""
api_custom_field:
    description: Current or resulting custom field data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for PUT/DELETE operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.custom_fields.d42_custom_fields import (
        d42_custom_fields,
)


def _to_bool_string(value):
        if value is None:
                return None
        value = str(value).strip().lower()
        if value in ("yes", "true"):
                return "true"
        if value in ("no", "false"):
                return "false"
        return None


def _to_yes_no(value):
        if value is None:
                return None
        value = str(value).strip().lower()
        if value in ("yes", "true"):
                return "yes"
        if value in ("no", "false"):
                return "no"
        return None


def _as_bool(value):
        normalized = _to_bool_string(value)
        if normalized is None:
                return None
        return normalized == "true"


def _get_custom_fields(helper, object_name, custom_field_id=None, key=None):
        payload = helper.d42_get_custom_fields(object_name=object_name, id=custom_field_id, key=key)
        custom_fields = payload.get("custom_fields", [])
        return custom_fields if isinstance(custom_fields, list) else []


def _find_custom_field(helper, object_name, custom_field_id=None, key=None):
        for custom_field in _get_custom_fields(helper, object_name=object_name, custom_field_id=custom_field_id, key=key):
                if custom_field_id is not None:
                        try:
                                if int(custom_field.get("id")) == int(custom_field_id):
                                        return custom_field
                        except (TypeError, ValueError):
                                continue

                if key is not None and str(custom_field.get("key")) == str(key):
                        return custom_field

        return None


def _needs_update(existing, params, force_update=False):
        if force_update or existing is None:
                return True

        if params.get("add_to_picklist") is not None or params.get("remove_from_picklist") is not None:
                return True

        if params.get("include_in_context_popups") is not None or params.get("related_field_name") is not None:
                return True

        desired_type = params.get("type")
        if desired_type is not None and str(existing.get("type", "")).strip().lower() != str(desired_type).strip().lower():
                return True

        for desired_key, existing_key in (
                ("mandatory", "mandatory"),
                ("filterable", "filterable"),
                ("log_for_api", "log_for_api"),
                ("multi_select", "is_multi"),
        ):
            desired_val = params.get(desired_key)
            if desired_val is None:
                    continue

            desired_bool = _to_bool_string(desired_val)
            current_bool = _to_bool_string(existing.get(existing_key))
            if desired_bool != current_bool:
                    return True

        return False


def _build_put_payload(params):
        payload = {
                "object_name": params.get("object_name"),
                "key": params.get("key"),
        }

        for key in (
                "type",
                "mandatory",
                "filterable",
                "log_for_api",
                "add_to_picklist",
                "remove_from_picklist",
                "multi_select",
                "include_in_context_popups",
                "related_field_name",
        ):
            if params.get(key) is not None:
                    payload[key] = params.get(key)

        delete_in_use = _to_yes_no(params.get("delete_in_use"))
        if delete_in_use is not None:
                payload["delete_in_use"] = delete_in_use

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
                object_name=dict(
                        type="str",
                        required=True,
                        choices=[
                                "application_group",
                                "application_group_calculation_rule",
                                "appcomp",
                                "appcomp_template",
                                "asset",
                                "building",
                                "business_service",
                                "cable",
                                "certificate",
                                "circuit",
                                "cloud_account",
                                "customer",
                                "device",
                                "dns_records",
                                "dns_zone",
                                "endusers",
                                "hardware_model",
                                "ip_address",
                                "part",
                                "partmodel",
                                "pdu",
                                "port",
                                "purchase",
                                "rack",
                                "resource",
                                "room",
                                "secret",
                                "service",
                                "service_instance",
                                "software",
                                "software_instance",
                                "subnet",
                                "vendor",
                                "vlan",
                                "vrfgroup",
                        ],
                ),
                id=dict(type="int", required=False),
                key=dict(type="str", required=False),
                type=dict(
                        type="str",
                        required=False,
                        choices=["text", "number", "date", "related_field", "boolean", "url", "picklist", "json", "markup"],
                ),
                mandatory=dict(type="str", required=False, choices=["yes", "no"]),
                filterable=dict(type="str", required=False, choices=["yes", "no"]),
                log_for_api=dict(type="str", required=False, choices=["yes", "no"]),
                add_to_picklist=dict(type="str", required=False),
                remove_from_picklist=dict(type="str", required=False),
                delete_in_use=dict(type="str", required=False, choices=["yes", "no", "true", "false"]),
                multi_select=dict(type="str", required=False, choices=["yes", "no"]),
                include_in_context_popups=dict(type="str", required=False, choices=["true", "false"]),
                related_field_name=dict(
                        type="str",
                        required=False,
                        choices=[
                                "appcomp",
                                "building",
                                "businessapp",
                                "certificate",
                                "circuit",
                                "cloudinfrastructure",
                                "costcenter",
                                "customer",
                                "device",
                                "dns_zone",
                                "endusers",
                                "hardware",
                                "ip_address",
                                "netport",
                                "organisation",
                                "os",
                                "pdu",
                                "pdu_model",
                                "powercircuit",
                                "purchase",
                                "rack",
                                "room",
                                "servicecategory",
                                "software_category",
                                "software",
                                "vlan",
                        ],
                ),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_custom_fields(
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
        object_name = module.params["object_name"]
        custom_field_id = module.params["id"]
        key = module.params["key"]

        existing = _find_custom_field(
                helper=helper,
                object_name=object_name,
                custom_field_id=custom_field_id,
                key=key,
        )

        if state == "absent":
                if custom_field_id is None and key is None:
                        module.fail_json(msg="id or key is required when state=absent.")

                if existing is None:
                        result["msg"] = "Custom field already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_custom_field"] = existing

                if module.check_mode:
                        result["msg"] = "Custom field would be deleted"
                        module.exit_json(**result)

                response = helper.d42_delete_custom_field(
                        object_name=object_name,
                        id=custom_field_id,
                        key=key,
                        delete_in_use=_as_bool(module.params["delete_in_use"]),
                )
                result["response"] = response
                module.exit_json(**result)

        if key is None:
                module.fail_json(msg="key is required when state=present.")

        if module.params["type"] == "related_field" and module.params["related_field_name"] is None:
                module.fail_json(msg="related_field_name is required when type=related_field.")

        put_payload = _build_put_payload(module.params)
        needs_change = _needs_update(
                existing=existing,
                params=module.params,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_custom_field"] = existing
                result["msg"] = "Custom field already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Custom field would be created/updated"
                if existing is not None:
                        result["api_custom_field"] = existing
                module.exit_json(**result)

        response = helper.d42_put_custom_field(**put_payload)
        result["response"] = response
        result["api_custom_field"] = _find_custom_field(
                helper=helper,
                object_name=object_name,
                custom_field_id=custom_field_id,
                key=key,
        )

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
