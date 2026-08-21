#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_operatingsystems
short_description: Manage Device42 operating systems
description:
    - Create, update, or delete Device42 operating systems.
    - Supports C(POST /api/1.0/operatingsystems/) and C(DELETE /api/1.0/operatingsystems/{id}/).
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
            - Desired state of the operating system.
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
    operating_system_id:
        description:
            - Device42 operating system ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [id]
    name:
        description:
            - Name of the operating system.
            - Required when C(state=present).
        required: false
        type: str
    manufacturer:
        description:
            - Hardware/software manufacturer name.
        required: false
        type: str
    notes:
        description:
            - Additional notes.
        required: false
        type: str
    category:
        description:
            - Multitenancy admin groups access string for initial insert.
        required: false
        type: str
    licensed_count:
        description:
            - Number of purchased licenses.
        required: false
        type: str
    licensing_model:
        description:
            - Licensing model.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create operating system
    xbh03.device42.operating_systems.d42_api_operatingsystems:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: ESX6.0
        manufacturer: VMware
        licensed_count: "100"

- name: Update operating system
    xbh03.device42.operating_systems.d42_api_operatingsystems:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        name: ESX6.0
        notes: Updated by Ansible

- name: Delete operating system
    xbh03.device42.operating_systems.d42_api_operatingsystems:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        operating_system_id: 114
"""

RETURN = r"""
api_operating_system:
    description: Current or resulting operating system data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.operating_systems.d42_operating_systems import (
        d42_operating_systems,
)


def _extract_operating_system_id_from_response(response):
        if not isinstance(response, dict):
                return None

        msg = response.get("msg")
        if isinstance(msg, list) and len(msg) > 1:
                try:
                        return int(msg[1])
                except (TypeError, ValueError):
                        return None

        for key in ("id", "operating_system_id"):
                if response.get(key) is not None:
                        try:
                                return int(response.get(key))
                        except (TypeError, ValueError):
                                return None

        return None


def _list_operating_systems(helper, name=None, manufacturer=None, category=None):
        payload = helper.d42_get_operating_systems(
                name=name,
                manufacturer=manufacturer,
                category=category,
        )
        operating_systems = payload.get("operatingsystems", [])
        return operating_systems if isinstance(operating_systems, list) else []


def _get_operating_system_by_id(helper, operating_system_id):
        payload = helper.d42_get_operating_system_by_id(operating_system_id=operating_system_id)
        entries = payload.get("operatingsystems", []) if isinstance(payload, dict) else []
        if isinstance(entries, list) and len(entries) > 0:
                return entries[0]
        return payload if isinstance(payload, dict) else None


def _find_operating_system(helper, operating_system_id=None, name=None):
        if operating_system_id is not None:
                return _get_operating_system_by_id(helper, operating_system_id=operating_system_id)

        if name is not None:
                for operating_system in _list_operating_systems(helper, name=name):
                        if str(operating_system.get("name")) == str(name):
                                return operating_system

        return None


def _needs_update(existing, payload, force_update=False):
        if force_update:
                return True

        if existing is None:
                return True

        compare_keys = ["manufacturer", "notes", "category", "licensed_count", "licensing_model"]
        for key in compare_keys:
            desired = payload.get(key)
            if desired is None:
                    continue

            current = existing.get(key)
            if str(current) != str(desired):
                    return True

        return False


def _build_post_payload(params):
        payload = {}
        for key in ["name", "manufacturer", "notes", "category", "licensed_count", "licensing_model"]:
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
                operating_system_id=dict(type="int", required=False, aliases=["id"]),
                name=dict(type="str", required=False),
                manufacturer=dict(type="str", required=False),
                notes=dict(type="str", required=False),
                category=dict(type="str", required=False),
                licensed_count=dict(type="str", required=False),
                licensing_model=dict(type="str", required=False),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_operating_systems(
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
        operating_system_id = module.params["operating_system_id"]
        name = module.params["name"]

        existing = _find_operating_system(
                helper=helper,
                operating_system_id=operating_system_id,
                name=name,
        )

        if state == "absent":
                if operating_system_id is None:
                        module.fail_json(msg="operating_system_id (or id) is required when state=absent.")

                if existing is None:
                        result["msg"] = "Operating system already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_operating_system"] = existing

                if module.check_mode:
                        result["msg"] = "Operating system would be deleted"
                        module.exit_json(**result)

                result["response"] = helper.d42_delete_operating_system(operating_system_id=operating_system_id)
                module.exit_json(**result)

        if name is None:
                module.fail_json(msg="name is required when state=present.")

        post_payload = _build_post_payload(module.params)
        needs_change = _needs_update(
                existing=existing,
                payload=post_payload,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_operating_system"] = existing
                result["msg"] = "Operating system already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "Operating system would be created/updated"
                if existing is not None:
                        result["api_operating_system"] = existing
                module.exit_json(**result)

        response = helper.d42_post_operating_systems(**post_payload)
        result["response"] = response

        resolved_os_id = _extract_operating_system_id_from_response(response)
        if resolved_os_id is None:
                resolved_os_id = operating_system_id

        result["api_operating_system"] = _find_operating_system(
                helper=helper,
                operating_system_id=resolved_os_id,
                name=name,
        )

        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
