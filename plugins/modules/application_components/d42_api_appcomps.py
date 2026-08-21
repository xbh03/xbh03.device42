#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_appcomps
short_description: Manage Device42 application components
description:
  - Create, update, or delete Device42 application components.
  - Optionally manage custom fields for the target application component.
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
      - Desired state of the application component.
    required: false
    type: str
    default: present
    choices:
      - present
      - absent
  appcomp_id:
    description:
      - Application component ID.
      - Used to target an existing application component.
    required: false
    type: int
  name:
    description:
      - Unique application component name.
      - Required to create an application component.
    required: false
    type: str
  device:
    description:
      - Device name that this component is dependent on.
    required: false
    type: str
  group_owner:
    description:
      - Group responsible for this component.
    required: false
    type: str
  what:
    description:
      - Business impact description.
    required: false
    type: str
  depends_on:
    description:
      - Names of app components this component depends on.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  dependents:
    description:
      - Names of app components depending on this component.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  groups_affected:
    description:
      - Names of affected groups.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  device_reason:
    description:
      - Device reason string for the application component.
    required: false
    type: str
  depends_on_reasons:
    description:
      - Dependency reason pairs.
    required: false
    type: str
  category:
    description:
      - Application component category name.
    required: false
    type: str
  category_id:
    description:
      - Application component category ID.
    required: false
    type: int
  tags_remove:
    description:
      - Tags to remove from the application component.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  customer:
    description:
      - Customer name.
    required: false
    type: str
  notes:
    description:
      - Additional notes.
    required: false
    type: str
  service_detail_ids:
    description:
      - Service instance IDs.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  software_detail_ids:
    description:
      - Software in use IDs.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  tags:
    description:
      - Tags to assign to the application component.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  custom_field_key:
    description:
      - Custom field key to create or update for the target application component.
    required: false
    type: str
  custom_field_type:
    description:
      - Custom field type.
    required: false
    type: str
  custom_field_mandatory:
    description:
      - Whether the custom field is mandatory, C(yes) or C(no).
    required: false
    type: str
  custom_field_filterable:
    description:
      - Whether the custom field is filterable, C(yes) or C(no).
    required: false
    type: str
  custom_field_log_for_api:
    description:
      - Whether to log the custom field for API, C(yes) or C(no).
    required: false
    type: str
  custom_field_related_field_name:
    description:
      - Related field name when C(custom_field_type=related_field).
    required: false
    type: str
  custom_field_add_to_picklist:
    description:
      - Picklist values to add.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  custom_field_remove_from_picklist:
    description:
      - Picklist values to remove.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  custom_field_delete_in_use:
    description:
      - Whether to delete picklist values that are in use, C(yes) or C(no).
    required: false
    type: str
  custom_field_related_field_value_by_id:
    description:
      - Whether to set related field value by ID, C(yes) or C(no).
    required: false
    type: str
  custom_field_value:
    description:
      - Custom field value.
    required: false
    type: str
  custom_field_clear_value:
    description:
      - Whether to clear the existing custom field value, C(yes) or C(no).
    required: false
    type: str
  custom_field_show_on_chart:
    description:
      - Whether to show the custom field on charts.
    required: false
    type: str
  custom_field_notes:
    description:
      - Additional notes for the custom field.
    required: false
    type: str
  custom_field_clear_notes:
    description:
      - Whether to clear custom field notes, C(yes) or C(no).
    required: false
    type: str
  custom_field_bulk_fields:
    description:
      - Bulk custom field key:value pairs.
    required: false
    type: str
  custom_field_multi_select:
    description:
      - Whether the picklist custom field is multi-select, C(yes) or C(no).
    required: false
    type: str
  force_update:
    description:
      - Force POST update when C(state=present) even if no drift is detected.
    required: false
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Create application component
  xbh03.device42.d42_api_appcomps:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: present
    name: Corp Wiki
    device: prodserver-001
    category: Application Layer
    tags:
      - wiki
      - internal

- name: Update application component notes and tags
  xbh03.device42.d42_api_appcomps:
    host: device42.example.internal
    userid: admin
    password: secret123
    state: present
    name: Corp Wiki
    notes: Updated by Ansible
    tags_remove:
      - legacy

- name: Update custom field on an application component
  xbh03.device42.d42_api_appcomps:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: present
    name: Corp Wiki
    custom_field_key: Project
    custom_field_value: Migration

- name: Delete application component by name
  xbh03.device42.d42_api_appcomps:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: absent
    name: Corp Wiki
"""

RETURN = r"""
api_appcomp:
  description: Current or resulting application component data when available.
  type: dict
  returned: success
response:
  description: Raw response from Device42 for create, update, or delete operations.
  type: dict
  returned: when changed
custom_field_response:
  description: Raw response from Device42 for custom field operations.
  type: dict
  returned: when a custom field operation is executed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.application_components.d42_appcomps import (
    d42_appcomps,
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


def _as_api_value(value):
    items = _normalize_multi_value(value)
    if not items:
        return None
    return ",".join(items)


def _find_appcomp_by_name(helper, name):
    if not name:
        return None

    payload = helper.d42_get_appcomps(
        name=name,
        include_cols="custom_fields,depends_on,dependent,device,group_owner,groups_affected,category,category_id,tags,what,notes,customer,service_detail_ids,software_detail_ids,device_reason,depends_on_reasons",
    )
    for appcomp in payload.get("appcomps", []):
        if appcomp.get("name") == name:
            return appcomp
    return None


def _find_appcomp_by_id(helper, appcomp_id):
    if appcomp_id is None:
        return None

    payload = helper.d42_get_appcomps(include_cols="custom_fields")
    for appcomp in payload.get("appcomps", []):
        try:
            current_id = int(appcomp.get("appcomp_id", -1))
        except (TypeError, ValueError):
            current_id = -1
        if current_id == int(appcomp_id):
            return helper.d42_get_appcomp_by_id(appcomp_id=current_id)
    return None


def _find_appcomp(helper, appcomp_id=None, name=None):
    if name is not None:
        return _find_appcomp_by_name(helper=helper, name=name)
    return _find_appcomp_by_id(helper=helper, appcomp_id=appcomp_id)


def _needs_update(existing, params):
    if existing is None:
        return True

    scalar_fields = [
        "device",
        "group_owner",
        "what",
        "device_reason",
        "depends_on_reasons",
        "category",
        "customer",
        "notes",
    ]

    for field_name in scalar_fields:
        if params[field_name] is not None and existing.get(field_name) != params[field_name]:
            return True

    list_fields = [
        ("depends_on", "depends_on"),
        ("dependents", "dependent"),
        ("groups_affected", "groups_affected"),
        ("tags", "tags"),
        ("service_detail_ids", "service_detail_ids"),
        ("software_detail_ids", "software_detail_ids"),
    ]

    for param_name, existing_name in list_fields:
        if params[param_name] is not None:
            desired = set(_normalize_multi_value(params[param_name]))
            current = set(_normalize_multi_value(existing.get(existing_name)))
            if desired != current:
                return True

    if params["tags_remove"] is not None:
        current_tags = set(_normalize_multi_value(existing.get("tags")))
        if current_tags.intersection(_normalize_multi_value(params["tags_remove"])):
            return True

    if params["category_id"] is not None:
        current_category_id = existing.get("category_id")
        try:
            current_category_id = int(current_category_id)
        except (TypeError, ValueError):
            current_category_id = None
        if current_category_id != int(params["category_id"]):
            return True

    if params["force_update"]:
        return True

    return False


def _custom_field_needs_update(existing, params):
    if params["custom_field_key"] is None:
        return False

    forcing_fields = [
        "custom_field_type",
        "custom_field_mandatory",
        "custom_field_filterable",
        "custom_field_log_for_api",
        "custom_field_related_field_name",
        "custom_field_add_to_picklist",
        "custom_field_remove_from_picklist",
        "custom_field_delete_in_use",
        "custom_field_related_field_value_by_id",
        "custom_field_clear_value",
        "custom_field_show_on_chart",
        "custom_field_clear_notes",
        "custom_field_bulk_fields",
        "custom_field_multi_select",
    ]
    for field_name in forcing_fields:
        if params[field_name] is not None:
            return True

    if existing is None:
        return True

    for custom_field in existing.get("custom_fields", []):
        if custom_field.get("key") != params["custom_field_key"]:
            continue

        if params["custom_field_value"] is not None and custom_field.get("value") != params["custom_field_value"]:
            return True
        if params["custom_field_notes"] is not None and custom_field.get("notes") != params["custom_field_notes"]:
            return True
        return False

    return True


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
        appcomp_id=dict(type="int", required=False),
        name=dict(type="str", required=False),
        device=dict(type="str", required=False),
        group_owner=dict(type="str", required=False),
        what=dict(type="str", required=False),
        depends_on=dict(type="raw", required=False),
        dependents=dict(type="raw", required=False),
        groups_affected=dict(type="raw", required=False),
        device_reason=dict(type="str", required=False),
        depends_on_reasons=dict(type="str", required=False),
        category=dict(type="str", required=False),
        category_id=dict(type="int", required=False),
        tags_remove=dict(type="raw", required=False),
        customer=dict(type="str", required=False),
        notes=dict(type="str", required=False),
        service_detail_ids=dict(type="raw", required=False),
        software_detail_ids=dict(type="raw", required=False),
        tags=dict(type="raw", required=False),
        custom_field_key=dict(type="str", required=False),
        custom_field_type=dict(type="str", required=False),
        custom_field_mandatory=dict(type="str", required=False),
        custom_field_filterable=dict(type="str", required=False),
        custom_field_log_for_api=dict(type="str", required=False),
        custom_field_related_field_name=dict(type="str", required=False),
        custom_field_add_to_picklist=dict(type="raw", required=False),
        custom_field_remove_from_picklist=dict(type="raw", required=False),
        custom_field_delete_in_use=dict(type="str", required=False),
        custom_field_related_field_value_by_id=dict(type="str", required=False),
        custom_field_value=dict(type="str", required=False),
        custom_field_clear_value=dict(type="str", required=False),
        custom_field_show_on_chart=dict(type="str", required=False),
        custom_field_notes=dict(type="str", required=False),
        custom_field_clear_notes=dict(type="str", required=False),
        custom_field_bulk_fields=dict(type="str", required=False),
        custom_field_multi_select=dict(type="str", required=False),
        force_update=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    state = module.params["state"]
    name = module.params["name"]
    appcomp_id = module.params["appcomp_id"]

    if state == "present" and name is None and appcomp_id is None:
        module.fail_json(msg="Either name or appcomp_id is required when state=present for application components.")

    if state == "absent" and name is None and appcomp_id is None:
        module.fail_json(msg="Either appcomp_id or name is required when state=absent for application components.")

    helper = d42_appcomps(
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

    existing = _find_appcomp(helper=helper, appcomp_id=appcomp_id, name=name)

    if state == "absent":
        if not existing:
            result["msg"] = "Application component already absent"
            module.exit_json(**result)

        result["api_appcomp"] = existing
        result["changed"] = True

        if module.check_mode:
            result["msg"] = "Application component would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_appcomp(appcomp_id=existing.get("appcomp_id"))
        result["response"] = response
        module.exit_json(**result)

    if existing is None and name is None:
        module.fail_json(msg="name is required to create a new application component when appcomp_id does not resolve an existing object.")

    appcomp_needs_update = _needs_update(existing=existing, params=module.params)
    custom_field_needs_update = _custom_field_needs_update(existing=existing, params=module.params)

    if not appcomp_needs_update and not custom_field_needs_update:
        result["api_appcomp"] = existing
        result["msg"] = "Application component already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Application component would be created/updated"
        if existing:
            result["api_appcomp"] = existing
        module.exit_json(**result)

    if appcomp_needs_update:
        response = helper.d42_post_appcomps(
            name=name if name is not None else existing.get("name"),
            device=module.params["device"],
            group_owner=module.params["group_owner"],
            what=module.params["what"],
            depends_on=_as_api_value(module.params["depends_on"]),
            dependents=_as_api_value(module.params["dependents"]),
            groups_affected=_as_api_value(module.params["groups_affected"]),
            device_reason=module.params["device_reason"],
            depends_on_reasons=module.params["depends_on_reasons"],
            category=module.params["category"],
            category_id=module.params["category_id"],
            tags_remove=_as_api_value(module.params["tags_remove"]),
            customer=module.params["customer"],
            notes=module.params["notes"],
            service_detail_ids=_as_api_value(module.params["service_detail_ids"]),
            software_detail_ids=_as_api_value(module.params["software_detail_ids"]),
            tags=_as_api_value(module.params["tags"]),
        )
        result["response"] = response

    refreshed = _find_appcomp(
        helper=helper,
        appcomp_id=appcomp_id,
        name=name if name is not None else (existing.get("name") if existing else None),
    )

    if custom_field_needs_update:
        if refreshed is None and appcomp_id is None:
            module.fail_json(msg="Unable to resolve application component for custom field update.")

        custom_field_response = helper.d42_put_custom_field_appcomp(
            key=module.params["custom_field_key"],
            appcomp_id=refreshed.get("appcomp_id") if refreshed else appcomp_id,
            name=None if refreshed else name,
            type=module.params["custom_field_type"],
            mandatory=module.params["custom_field_mandatory"],
            filterable=module.params["custom_field_filterable"],
            log_for_api=module.params["custom_field_log_for_api"],
            related_field_name=module.params["custom_field_related_field_name"],
            add_to_picklist=_as_api_value(module.params["custom_field_add_to_picklist"]),
            remove_from_picklist=_as_api_value(module.params["custom_field_remove_from_picklist"]),
            delete_in_use=module.params["custom_field_delete_in_use"],
            related_field_value_by_id=module.params["custom_field_related_field_value_by_id"],
            value=module.params["custom_field_value"],
            clear_value=module.params["custom_field_clear_value"],
            show_on_chart=module.params["custom_field_show_on_chart"],
            notes=module.params["custom_field_notes"],
            clear_notes=module.params["custom_field_clear_notes"],
            bulk_fields=module.params["custom_field_bulk_fields"],
            multi_select=module.params["custom_field_multi_select"],
        )
        result["custom_field_response"] = custom_field_response

    result["api_appcomp"] = _find_appcomp(
        helper=helper,
        appcomp_id=refreshed.get("appcomp_id") if refreshed else appcomp_id,
        name=name if name is not None else (refreshed.get("name") if refreshed else None),
    )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
