#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_hardware_models
short_description: Manage Device42 hardware models
description:
    - Create, update, or delete Device42 hardware models.
    - Supports C(POST /api/2.0/hardwares/) and C(DELETE /api/2.0/hardwares/{id}/).
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
            - Desired state of the hardware model.
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
    hardware_id:
        description:
            - Hardware model ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [id]
    name:
        description:
            - Hardware model name.
            - Required when C(state=present) if C(hardware_id) is not provided.
        required: false
        type: str
    physicalsubtype_id:
        description:
            - Hardware model type ID.
        required: false
        type: int
    physicalsubtype:
        description:
            - Hardware model type name.
        required: false
        type: str
    size:
        description:
            - Size in U for non-blade models.
        required: false
        type: str
    depth_id:
        description:
            - Depth ID.
        required: false
        type: int
    depth:
        description:
            - Depth name.
        required: false
        type: str
    width_ratio_id:
        description:
            - Width ratio ID.
        required: false
        type: int
    width_ratio:
        description:
            - Width ratio.
        required: false
        type: str
    blade_size_id:
        description:
            - Blade size ID.
        required: false
        type: int
    blade_size:
        description:
            - Blade size value.
        required: false
        type: str
    vendor_id:
        description:
            - Hardware model vendor ID.
        required: false
        type: int
    vendor:
        description:
            - Hardware model vendor name.
        required: false
        type: str
    front_image_id:
        description:
            - Front image file ID.
        required: false
        type: str
    front_image:
        description:
            - Front image file name.
        required: false
        type: str
    back_image_id:
        description:
            - Back image file ID.
        required: false
        type: int
    back_image:
        description:
            - Back image file name.
        required: false
        type: str
    network_device:
        description:
            - Whether model is a network device.
        required: false
        type: str
        choices:
            - yes
            - no
    blade_host:
        description:
            - Whether model is a blade host.
        required: false
        type: str
        choices:
            - yes
            - no
    add_ports_when_creating_device:
        description:
            - Auto-create ports when creating devices from this model.
        required: false
        type: str
        choices:
            - yes
            - no
    part_number:
        description:
            - Hardware model part number.
        required: false
        type: str
    watts:
        description:
            - Watts per PSU.
        required: false
        type: int
    specification_url:
        description:
            - Specification URL.
        required: false
        type: str
    end_of_life_date:
        description:
            - End of life date in YYYY-MM-DD format.
        required: false
        type: str
    end_of_support_date:
        description:
            - End of support date in YYYY-MM-DD format.
        required: false
        type: str
    notes:
        description:
            - Notes about the hardware model.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create hardware model
    xbh03.device42.hardware_models.d42_api_hardware_models:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: PowerLogic
        physicalsubtype: Branch Circuit Power Meter
        vendor: APC Inc.
        watts: 1000

- name: Update hardware model by ID
    xbh03.device42.hardware_models.d42_api_hardware_models:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        hardware_id: 1
        name: PowerLogic Updated
        notes: hardware notes

- name: Delete hardware model
    xbh03.device42.hardware_models.d42_api_hardware_models:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        hardware_id: 114
"""

RETURN = r"""
api_hardware_model:
    description: Current or resulting hardware model data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.hardware_models.d42_hardware_models import (
        d42_hardware_models,
)


def _extract_hardware_id_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and len(msg) > 1:
                try:
                        return int(msg[1])
                except (TypeError, ValueError):
                        return None

        for key in ("hardware_id", "id"):
                if response.get(key) is not None:
                        try:
                                return int(response.get(key))
                        except (TypeError, ValueError):
                                return None

        return None


def _get_hardware_model_by_id(helper, hardware_id):
        payload = helper.d42_get_hardware_model_by_id(hardware_id=hardware_id)
        if isinstance(payload, dict):
                models = payload.get("models")
                if isinstance(models, list) and len(models) > 0:
                        return models[0]
                return payload
        return None


def _find_hardware_model(helper, hardware_id=None, name=None):
        if hardware_id is not None:
                return _get_hardware_model_by_id(helper, hardware_id=hardware_id)

        if name is not None:
                payload = helper.d42_get_hardware_models(name=name)
                for model in payload.get("hardware_models", []) if isinstance(payload, dict) else []:
                        if str(model.get("name")) == str(name):
                                candidate_id = model.get("hardware_id")
                                if candidate_id is not None:
                                        return _get_hardware_model_by_id(helper, hardware_id=int(candidate_id))

        return None


def _needs_update(existing, params, force_update=False):
        if force_update:
                return True

        if existing is None:
                return True

        for key in (
                "name",
                "physicalsubtype_id",
                "physicalsubtype",
                "size",
                "depth_id",
                "depth",
                "width_ratio_id",
                "width_ratio",
                "blade_size_id",
                "blade_size",
                "vendor_id",
                "vendor",
                "front_image_id",
                "front_image",
                "back_image_id",
                "back_image",
                "network_device",
                "blade_host",
                "add_ports_when_creating_device",
                "part_number",
                "watts",
                "specification_url",
                "end_of_life_date",
                "end_of_support_date",
                "notes",
        ):
            desired = params.get(key)
            if desired is None:
                    continue

            current = existing.get(key)
            if str(current) != str(desired):
                    return True

        return False


def _build_post_payload(params):
        payload = {}
        for key in (
                "name",
                "hardware_id",
                "physicalsubtype_id",
                "physicalsubtype",
                "size",
                "depth_id",
                "depth",
                "width_ratio_id",
                "width_ratio",
                "blade_size_id",
                "blade_size",
                "vendor_id",
                "vendor",
                "front_image_id",
                "front_image",
                "back_image_id",
                "back_image",
                "network_device",
                "blade_host",
                "add_ports_when_creating_device",
                "part_number",
                "watts",
                "specification_url",
                "end_of_life_date",
                "end_of_support_date",
                "notes",
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
                force_update=dict(type="bool", required=False, default=False),
                hardware_id=dict(type="int", required=False, aliases=["id"]),
                name=dict(type="str", required=False),
                physicalsubtype_id=dict(type="int", required=False),
                physicalsubtype=dict(type="str", required=False),
                size=dict(type="str", required=False),
                depth_id=dict(type="int", required=False),
                depth=dict(type="str", required=False),
                width_ratio_id=dict(type="int", required=False),
                width_ratio=dict(type="str", required=False),
                blade_size_id=dict(type="int", required=False),
                blade_size=dict(type="str", required=False),
                vendor_id=dict(type="int", required=False),
                vendor=dict(type="str", required=False),
                front_image_id=dict(type="str", required=False),
                front_image=dict(type="str", required=False),
                back_image_id=dict(type="int", required=False),
                back_image=dict(type="str", required=False),
                network_device=dict(type="str", required=False, choices=["yes", "no"]),
                blade_host=dict(type="str", required=False, choices=["yes", "no"]),
                add_ports_when_creating_device=dict(type="str", required=False, choices=["yes", "no"]),
                part_number=dict(type="str", required=False),
                watts=dict(type="int", required=False),
                specification_url=dict(type="str", required=False),
                end_of_life_date=dict(type="str", required=False),
                end_of_support_date=dict(type="str", required=False),
                notes=dict(type="str", required=False),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_hardware_models(
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
        hardware_id = module.params["hardware_id"]
        name = module.params["name"]

        existing = _find_hardware_model(
                helper=helper,
                hardware_id=hardware_id,
                name=name,
        )

        if state == "absent":
                if hardware_id is None:
                        module.fail_json(msg="hardware_id (or id) is required when state=absent.")

                if existing is None:
                        result["msg"] = "Hardware model already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_hardware_model"] = existing

                if module.check_mode:
                        result["msg"] = "Hardware model would be deleted"
                        module.exit_json(**result)

                result["response"] = helper.d42_delete_hardware_model(hardware_id=hardware_id)
                module.exit_json(**result)

        if name is None and hardware_id is None:
                module.fail_json(msg="name or hardware_id is required when state=present.")

        needs_change = _needs_update(
                existing=existing,
                params=module.params,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_hardware_model"] = existing
                result["msg"] = "Hardware model already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Hardware model would be created/updated"
                if existing is not None:
                        result["api_hardware_model"] = existing
                module.exit_json(**result)

        response = helper.d42_post_hardware_models(**_build_post_payload(module.params))
        result["response"] = response

        resolved_hardware_id = _extract_hardware_id_from_response(response)
        if resolved_hardware_id is None:
                resolved_hardware_id = hardware_id

        result["api_hardware_model"] = _find_hardware_model(
                helper=helper,
                hardware_id=resolved_hardware_id,
                name=name,
        )
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
