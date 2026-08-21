#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_eoleos
short_description: Manage Device42 OS EOL/EOS records
description:
    - Create, update, or delete Device42 OS End of Life/End of Support records.
    - Supports C(POST /api/1.0/os_eoleos/) and C(DELETE /api/1.0/os_eoleos/{id}/).
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
            - Desired state of the OS EOL/EOS record.
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
    id:
        description:
            - OS EOL/EOS numeric ID.
            - Required when C(state=absent).
        required: false
        type: int
    os:
        description:
            - Operating system name.
            - Required with C(state=present) if C(os_id) and C(id) are not provided.
        required: false
        type: str
    os_id:
        description:
            - Operating system ID.
            - Required with C(state=present) if C(os) and C(id) are not provided.
        required: false
        type: int
    version:
        description:
            - Operating system version.
        required: false
        type: str
    end_of_life_date:
        description:
            - End of Life date in YYYY-MM-DD format.
        required: false
        type: str
    end_of_support_date:
        description:
            - End of Support date in YYYY-MM-DD format.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create OS EOL/EOS with OS name
    xbh03.device42.operating_systems.d42_api_eoleos:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        os: Ubuntu
        version: 4.4.0-53-generic
        end_of_life_date: "2017-11-15"
        end_of_support_date: "2017-11-30"

- name: Update existing OS EOL/EOS by ID
    xbh03.device42.operating_systems.d42_api_eoleos:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        id: 9
        end_of_life_date: "2018-01-01"

- name: Delete OS EOL/EOS record
    xbh03.device42.operating_systems.d42_api_eoleos:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        id: 9
"""

RETURN = r"""
api_os_eoleos:
    description: Current or resulting OS EOL/EOS data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.operating_systems.d42_eoleos import (
        d42_eoleos,
)


def _extract_id_from_response(response):
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


def _list_os_eoleos(helper):
        payload = helper.d42_get_os_eoleos()
        values = payload.get("values", []) if isinstance(payload, dict) else []
        return values if isinstance(values, list) else []


def _find_os_eoleos(helper, id=None, os=None, os_id=None, version=None):
        for entry in _list_os_eoleos(helper):
                if id is not None:
                        try:
                                if int(entry.get("id")) == int(id):
                                        return entry
                        except (TypeError, ValueError):
                                continue

                if os_id is not None:
                        try:
                                if int(entry.get("os_id")) != int(os_id):
                                        continue
                        except (TypeError, ValueError):
                                continue
                if os is not None and str(entry.get("os")) != str(os):
                        continue
                if version is not None and str(entry.get("version")) != str(version):
                        continue

                if id is None and (os_id is not None or os is not None):
                        return entry

        return None


def _needs_update(existing, params, force_update=False):
        if force_update:
                return True

        if existing is None:
                return True

        for desired_key, current_key in (
                ("version", "version"),
                ("end_of_life_date", "end_of_life"),
                ("end_of_support_date", "end_of_support"),
        ):
            desired = params.get(desired_key)
            if desired is None:
                    continue
            if str(existing.get(current_key)) != str(desired):
                    return True

        return False


def _build_post_payload(params):
        payload = {}
        for key in ("id", "os", "os_id", "version"):
                if params.get(key) is not None:
                        payload[key] = params.get(key)

        if params.get("end_of_life_date") is not None:
                payload["end_of_life"] = params.get("end_of_life_date")
        if params.get("end_of_support_date") is not None:
                payload["end_of_support"] = params.get("end_of_support_date")

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
                id=dict(type="int", required=False),
                os=dict(type="str", required=False),
                os_id=dict(type="int", required=False),
                version=dict(type="str", required=False),
                end_of_life_date=dict(type="str", required=False),
                end_of_support_date=dict(type="str", required=False),
        )

        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
        result = dict(changed=False)

        helper = d42_eoleos(
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
        entry_id = module.params["id"]

        existing = _find_os_eoleos(
                helper=helper,
                id=entry_id,
                os=module.params["os"],
                os_id=module.params["os_id"],
                version=module.params["version"],
        )

        if state == "absent":
                if entry_id is None:
                        module.fail_json(msg="id is required when state=absent.")

                if existing is None:
                        result["msg"] = "OS EOL/EOS record already absent"
                        module.exit_json(**result)

                result["changed"] = True
                result["api_os_eoleos"] = existing

                if module.check_mode:
                        result["msg"] = "OS EOL/EOS record would be deleted"
                        module.exit_json(**result)

                result["response"] = helper.d42_delete_os_eoleos(id=entry_id)
                module.exit_json(**result)

        if entry_id is None and module.params["os"] is None and module.params["os_id"] is None:
                module.fail_json(msg="os or os_id is required when state=present for new records.")

        post_payload = _build_post_payload(module.params)
        needs_change = _needs_update(
                existing=existing,
                params=module.params,
                force_update=module.params["force_update"],
        )

        if not needs_change:
                result["api_os_eoleos"] = existing
                result["msg"] = "OS EOL/EOS record already in desired state"
                module.exit_json(**result)

        result["changed"] = True
        if module.check_mode:
                result["msg"] = "OS EOL/EOS record would be created/updated"
                if existing is not None:
                        result["api_os_eoleos"] = existing
                module.exit_json(**result)

        response = helper.d42_post_os_eoleos(**post_payload)
        result["response"] = response

        resolved_id = _extract_id_from_response(response)
        if resolved_id is None:
                resolved_id = entry_id

        result["api_os_eoleos"] = _find_os_eoleos(
                helper=helper,
                id=resolved_id,
                os=module.params["os"],
                os_id=module.params["os_id"],
                version=module.params["version"],
        )
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
