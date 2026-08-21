#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_appgroup_calc_rule
short_description: Manage Device42 application group calculation rules
description:
    - Create, update, or delete Device42 application group calculation rules.
    - Uses JSON payload for create/update as documented by Device42.
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
            - Desired state of the application group calculation rule.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    rule_id:
        description:
            - Application group calculation rule ID.
            - Used as primary target when provided.
        required: false
        type: int
    name:
        description:
            - Application group calculation rule name.
            - Used to target existing rules when C(rule_id) is not provided.
        required: false
        type: str
    payload:
        description:
            - JSON payload for create/update requests to C(/api/2.0/app_group_calc_rule/).
            - Accepts all fields supported by the Device42 endpoint body.
        required: false
        type: dict
    force_update:
        description:
            - Force POST update when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Create application group calculation rule
    xbh03.device42.d42_api_appgroup_calc_rule:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        payload:
            name: AG Rule
            enabled: yes
            outcome: Auto-Create
            starting_point_type: Criteria
            starting_point_criteria:
                - criteria: type="virtual"
                  ci_type: device
                  required: yes

- name: Update application group calculation rule by ID
    xbh03.device42.d42_api_appgroup_calc_rule:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        rule_id: 11
        payload:
            levels_of_depth: 20
            store_connection_metadata: yes

- name: Delete application group calculation rule by name
    xbh03.device42.d42_api_appgroup_calc_rule:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        name: AG Rule
"""

RETURN = r"""
api_appgroup_calc_rule:
    description: Current or resulting application group calculation rule data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create, update, or delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.application_groups.d42_appgroup_calc_rule import (
    d42_appgroup_calc_rule,
)


def _find_rule(helper, rule_id=None, name=None):
    if rule_id is not None:
        return helper.d42_get_appgroup_calc_rule_by_id(rule_id=rule_id)

    if name is None:
        return None

    payload = helper.d42_get_appgroup_calc_rules(name=name)
    for rule in payload.get("rules", []):
        if rule.get("name") == name:
            return rule
    return None


def _needs_update(existing, desired_payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    for key, desired_value in desired_payload.items():
        if key not in existing:
            return True
        if existing.get(key) != desired_value:
            return True

    return False


def _build_payload(module):
    payload = dict(module.params.get("payload") or {})

    rule_id = module.params.get("rule_id")
    name = module.params.get("name")

    if rule_id is not None:
        if payload.get("id") is not None and int(payload.get("id")) != int(rule_id):
            module.fail_json(msg="rule_id and payload.id reference different application group calculation rules.")
        payload["id"] = int(rule_id)

    if name is not None:
        if payload.get("name") is not None and payload.get("name") != name:
            module.fail_json(msg="name and payload.name reference different application group calculation rules.")
        payload["name"] = name

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
        rule_id=dict(type="int", required=False),
        name=dict(type="str", required=False),
        payload=dict(type="dict", required=False),
        force_update=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    state = module.params["state"]
    rule_id = module.params["rule_id"]
    name = module.params["name"]

    helper = d42_appgroup_calc_rule(
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

    if state == "absent" and rule_id is None and name is None:
        module.fail_json(msg="Either rule_id or name is required when state=absent.")

    existing = _find_rule(helper=helper, rule_id=rule_id, name=name)

    if state == "absent":
        if not existing:
            result["msg"] = "Application group calculation rule already absent"
            module.exit_json(**result)

        resolved_rule_id = existing.get("id")
        if resolved_rule_id is None and rule_id is not None:
            resolved_rule_id = rule_id

        result["api_appgroup_calc_rule"] = existing
        result["changed"] = True

        if module.check_mode:
            result["msg"] = "Application group calculation rule would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_appgroup_calc_rule(rule_id=resolved_rule_id)
        result["response"] = response
        module.exit_json(**result)

    merged_payload = _build_payload(module)
    if not merged_payload:
        module.fail_json(msg="payload is required when state=present.")

    if existing is None and merged_payload.get("name") is None:
        module.fail_json(msg="name (or payload.name) is required to create a new calculation rule.")

    needs_change = _needs_update(
        existing=existing,
        desired_payload=merged_payload,
        force_update=module.params["force_update"],
    )

    if not needs_change:
        result["api_appgroup_calc_rule"] = existing
        result["msg"] = "Application group calculation rule already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Application group calculation rule would be created/updated"
        if existing:
            result["api_appgroup_calc_rule"] = existing
        module.exit_json(**result)

    response = helper.d42_post_appgroup_calc_rule(payload=merged_payload)
    result["response"] = response

    refresh_id = merged_payload.get("id")
    refresh_name = merged_payload.get("name")
    if refresh_id is None and isinstance(existing, dict):
        refresh_id = existing.get("id")
    if refresh_name is None and isinstance(existing, dict):
        refresh_name = existing.get("name")

    result["api_appgroup_calc_rule"] = _find_rule(helper=helper, rule_id=refresh_id, name=refresh_name)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
