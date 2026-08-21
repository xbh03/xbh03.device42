#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_appcomptemplate
short_description: Manage Device42 application component templates
description:
    - Create, update, or delete Device42 application component templates.
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
            - Desired state of the application component template.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    template_id:
        description:
            - Application component template ID.
            - If provided, used as primary lookup key.
        required: false
        type: int
    name:
        description:
            - Application component template name.
            - Required to create a new template when C(template_id) is not provided.
        required: false
        type: str
    enabled:
        description:
            - Enable or disable template, C(yes) or C(no).
        required: false
        type: str
    rule_type:
        description:
            - Target environment.
            - C(Windows) or C(*Nix).
        required: false
        type: str
    rule_type_id:
        description:
            - Rule type ID.
            - C(0) for Windows, C(1) for *Nix.
        required: false
        type: int
    service_id:
        description:
            - Associated service ID.
        required: false
        type: int
    associated_software_id:
        description:
            - Associated software ID.
        required: false
        type: int
    service:
        description:
            - Associated service name.
        required: false
        type: str
    service_listening_port:
        description:
            - Filter service instances listening on this port.
        required: false
        type: int
    app_name_pattern:
        description:
            - Application name pattern.
        required: false
        type: str
    related_services_listening_port:
        description:
            - Related services listening port.
        required: false
        type: int
    config_file_location:
        description:
            - Starting location for config file discovery.
        required: false
        type: str
    traverse_subdirectories:
        description:
            - Traverse subdirectories while discovering config files, C(yes) or C(no).
        required: false
        type: str
    filename_filter:
        description:
            - Config file name pattern.
        required: false
        type: str
    application_category:
        description:
            - Application category name.
        required: false
        type: str
    application_category_id:
        description:
            - Application category ID.
        required: false
        type: int
    customer_id:
        description:
            - Customer ID.
        required: false
        type: int
    customer:
        description:
            - Customer name.
        required: false
        type: str
    what:
        description:
            - Business impact description.
        required: false
        type: str
    tags:
        description:
            - Comma-separated tags to set.
        required: false
        type: str
    tags_remove:
        description:
            - Comma-separated tags to remove.
        required: false
        type: str
    related_services_ids:
        description:
            - Comma-separated related service IDs.
        required: false
        type: str
    related_services_ids_remove:
        description:
            - Comma-separated related service IDs to remove.
        required: false
        type: str
    related_software_ids:
        description:
            - Comma-separated related software IDs.
        required: false
        type: str
    related_software_ids_remove:
        description:
            - Comma-separated related software IDs to remove.
        required: false
        type: str
    service_cmd_arg_match:
        description:
            - Path argument matching value used by template discovery logic.
        required: false
        type: str
    match_type:
        description:
            - Match mode C(Text) or C(Regular Expression).
        required: false
        type: str
    match_type_id:
        description:
            - Match mode ID.
            - C(0) for Text, C(1) for Regular Expression.
        required: false
        type: int
    force_update:
        description:
            - Force POST update when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Create application component template
    xbh03.device42.d42_api_appcomptemplate:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: App-Comp-Template-T2
        enabled: yes
        rule_type: Windows
        application_category: Application Layer

- name: Update existing application component template by ID
    xbh03.device42.d42_api_appcomptemplate:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        template_id: 13
        tags: app,managed
        service_cmd_arg_match: service
        match_type: Text

- name: Delete application component template by ID
    xbh03.device42.d42_api_appcomptemplate:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        template_id: 13

- name: Delete application component template by name
    xbh03.device42.d42_api_appcomptemplate:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        name: App-Comp-Template-T2
"""

RETURN = r"""
api_appcomp_template:
    description: Current or resulting application component template data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create, update, or delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.application_components.d42_appcomptemplate import (
        d42_appcomptemplate,
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


def _find_template(helper, template_id=None, name=None):
    if template_id is not None:
        payload = helper.d42_get_appcomp_templates(template_id=template_id)
    else:
        payload = helper.d42_get_appcomp_templates(name=name)
    templates = payload.get("app_component_templates", [])

    resolved_template_id = None
    if template_id is not None:
        resolved_template_id = int(template_id)

    for template in templates:
        current_id = template.get("id")
        try:
            current_id = int(current_id)
        except (TypeError, ValueError):
            current_id = None

        if resolved_template_id is not None and current_id == resolved_template_id:
            return template
        if resolved_template_id is None and name is not None and template.get("name") == name:
            return template

    return None


def _resolve_template(helper, module, template_id=None, name=None):
    if template_id is not None:
        existing = _find_template(helper=helper, template_id=template_id)
        if existing is not None and name is not None and existing.get("name") != name:
            module.fail_json(
                msg=(
                    "template_id and name reference different application component templates. "
                    "Provide only one identifier or matching values."
                )
            )
        return existing

    return _find_template(helper=helper, name=name)


def _needs_update(existing, params):
    if existing is None:
        return True

    field_map = {
        "name": "name",
        "enabled": "enabled",
        "rule_type": "rule_type",
        "rule_type_id": "rule_type_id",
        "service_id": "service_id",
        "service_listening_port": "service_listening_port",
        "app_name_pattern": "app_name_pattern",
        "related_services_listening_port": "related_services_listening_port",
        "config_file_location": "config_file_location",
        "traverse_subdirectories": "traverse_subdirectories",
        "filename_filter": "filename_filter",
        "application_category_id": "application_category_id",
        "application_category": "application_category_name",
        "customer_id": "customer_id",
        "customer": "customer",
        "what": "what",
        "service_cmd_arg_match": "service_cmd_arg_match",
        "match_type": "match_type",
        "match_type_id": "match_type_id",
    }

    for param_name, existing_name in field_map.items():
        desired = params[param_name]
        if desired is None:
            continue

        current = existing.get(existing_name)
        if param_name in (
            "rule_type_id",
            "service_id",
            "service_listening_port",
            "related_services_listening_port",
            "application_category_id",
            "customer_id",
            "match_type_id",
        ):
            try:
                current = int(current)
            except (TypeError, ValueError):
                current = None
            if current != int(desired):
                return True
        else:
            if str(current) != str(desired):
                return True

    if params["tags"] is not None:
        desired_tags = set(_normalize_multi_value(params["tags"]))
        current_tags = set(_normalize_multi_value(existing.get("tags")))
        if desired_tags != current_tags:
            return True

    if params["related_services_ids"] is not None:
        desired_related_services = set(_normalize_multi_value(params["related_services_ids"]))
        current_related_services = set(_normalize_multi_value(existing.get("related_services_ids")))
        if desired_related_services != current_related_services:
            return True

    if params["related_software_ids"] is not None:
        desired_related_software = set(_normalize_multi_value(params["related_software_ids"]))
        current_related_software = set(_normalize_multi_value(existing.get("related_software_ids")))
        if desired_related_software != current_related_software:
            return True

    if params["tags_remove"] is not None:
        remove_tags = set(_normalize_multi_value(params["tags_remove"]))
        current_tags = set(_normalize_multi_value(existing.get("tags")))
        if current_tags.intersection(remove_tags):
            return True

    if params["related_services_ids_remove"] is not None:
        remove_services = set(_normalize_multi_value(params["related_services_ids_remove"]))
        current_related_services = set(_normalize_multi_value(existing.get("related_services_ids")))
        if current_related_services.intersection(remove_services):
            return True

    if params["related_software_ids_remove"] is not None:
        remove_software = set(_normalize_multi_value(params["related_software_ids_remove"]))
        current_related_software = set(_normalize_multi_value(existing.get("related_software_ids")))
        if current_related_software.intersection(remove_software):
            return True

    if params["force_update"]:
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
        template_id=dict(type="int", required=False),
        name=dict(type="str", required=False),
        enabled=dict(type="str", required=False),
        rule_type=dict(type="str", required=False),
        rule_type_id=dict(type="int", required=False),
        service_id=dict(type="int", required=False),
        associated_software_id=dict(type="int", required=False),
        service=dict(type="str", required=False),
        service_listening_port=dict(type="int", required=False),
        app_name_pattern=dict(type="str", required=False),
        related_services_listening_port=dict(type="int", required=False),
        config_file_location=dict(type="str", required=False),
        traverse_subdirectories=dict(type="str", required=False),
        filename_filter=dict(type="str", required=False),
        application_category=dict(type="str", required=False),
        application_category_id=dict(type="int", required=False),
        customer_id=dict(type="int", required=False),
        customer=dict(type="str", required=False),
        what=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        tags_remove=dict(type="str", required=False),
        related_services_ids=dict(type="str", required=False),
        related_services_ids_remove=dict(type="str", required=False),
        related_software_ids=dict(type="str", required=False),
        related_software_ids_remove=dict(type="str", required=False),
        service_cmd_arg_match=dict(type="str", required=False),
        match_type=dict(type="str", required=False),
        match_type_id=dict(type="int", required=False),
        force_update=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    state = module.params["state"]
    template_id = module.params["template_id"]
    name = module.params["name"]

    if state == "present" and template_id is None and name is None:
        module.fail_json(msg="Either template_id or name is required when state=present for application component templates.")

    if state == "absent" and template_id is None and name is None:
        module.fail_json(msg="Either template_id or name is required when state=absent for application component templates.")

    helper = d42_appcomptemplate(
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

    existing = _resolve_template(helper=helper, module=module, template_id=template_id, name=name)

    if state == "absent":
        if not existing:
            result["msg"] = "Application component template already absent"
            module.exit_json(**result)

        result["api_appcomp_template"] = existing
        result["changed"] = True

        if module.check_mode:
            result["msg"] = "Application component template would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_appcomp_template(template_id=existing.get("id"))
        result["response"] = response
        module.exit_json(**result)

    if existing is None and name is None:
        module.fail_json(msg="name is required to create a new application component template when template_id does not resolve an existing object.")

    needs_update = _needs_update(existing=existing, params=module.params)

    if not needs_update:
        result["api_appcomp_template"] = existing
        result["msg"] = "Application component template already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Application component template would be created/updated"
        if existing:
            result["api_appcomp_template"] = existing
        module.exit_json(**result)

    response = helper.d42_post_appcomp_template(
        template_id=template_id if template_id is not None else (existing.get("id") if existing else None),
        name=name if name is not None else (existing.get("name") if existing else None),
        enabled=module.params["enabled"],
        rule_type=module.params["rule_type"],
        rule_type_id=module.params["rule_type_id"],
        service_id=module.params["service_id"],
        associated_software_id=module.params["associated_software_id"],
        service=module.params["service"],
        service_listening_port=module.params["service_listening_port"],
        app_name_pattern=module.params["app_name_pattern"],
        related_services_listening_port=module.params["related_services_listening_port"],
        config_file_location=module.params["config_file_location"],
        traverse_subdirectories=module.params["traverse_subdirectories"],
        filename_filter=module.params["filename_filter"],
        application_category=module.params["application_category"],
        application_category_id=module.params["application_category_id"],
        customer_id=module.params["customer_id"],
        customer=module.params["customer"],
        what=module.params["what"],
        tags=module.params["tags"],
        tags_remove=module.params["tags_remove"],
        related_services_ids=module.params["related_services_ids"],
        related_services_ids_remove=module.params["related_services_ids_remove"],
        related_software_ids=module.params["related_software_ids"],
        related_software_ids_remove=module.params["related_software_ids_remove"],
        service_cmd_arg_match=module.params["service_cmd_arg_match"],
        match_type=module.params["match_type"],
        match_type_id=module.params["match_type_id"],
    )
    result["response"] = response

    refreshed_template_id = template_id if template_id is not None else (existing.get("id") if existing else None)
    refreshed_name = name if refreshed_template_id is None else None
    if refreshed_name is None and existing is not None:
        refreshed_name = existing.get("name") if refreshed_template_id is None else None

    refreshed = _find_template(
        helper=helper,
        template_id=refreshed_template_id,
        name=refreshed_name,
    )
    if refreshed is not None:
        result["api_appcomp_template"] = refreshed

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
