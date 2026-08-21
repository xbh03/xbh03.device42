#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_admingroups
short_description: Manage Device42 admin groups
description:
    - Create, update, or delete Device42 admin groups.
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
            - Use together with C(client_secret_key) as an alternative to C(userid) and C(password).
        required: false
        type: str
    client_secret_key:
        description:
            - Device42 API client secret key used to authenticate.
            - Use together with C(client_key) as an alternative to C(userid) and C(password).
        required: false
        type: str
    userid:
        description:
            - Device42 username used to authenticate.
            - Use together with C(password) as an alternative to C(client_key) and C(client_secret_key).
        required: false
        type: str
    password:
        description:
            - Device42 password used to authenticate.
            - Use together with C(userid) as an alternative to C(client_key) and C(client_secret_key).
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
            - Desired state of the admin group.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    group_id:
        description:
            - Admin group ID.
            - Used to target an existing group directly.
        required: false
        type: int
    name:
        description:
            - Admin group name.
            - Required to create a new group when C(group_id) is not provided.
        required: false
        type: str
    members:
        description:
            - Members to add to the admin group.
            - Accepts a comma-separated string or a list of usernames.
        required: false
        type: raw
    members_remove:
        description:
            - Members to remove from an existing group.
            - Ignored when C(members) is provided.
            - Accepts a comma-separated string or a list of usernames.
        required: false
        type: raw
    permissions:
        description:
            - Permissions to add to the admin group.
            - Accepts a comma-separated string or a list of permission names.
        required: false
        type: raw
    permissions_remove:
        description:
            - Permissions to remove from an existing group.
            - Ignored when C(permissions) is provided.
            - Accepts a comma-separated string or a list of permission names.
        required: false
        type: raw
"""

EXAMPLES = r"""
- name: Create admin group
    xbh03.device42.d42_api_admingroups:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: API Admin Group
        members:
            - user1
            - user2
        permissions:
            - View objects
            - Add objects

- name: Update admin group members by ID
    xbh03.device42.d42_api_admingroups:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        group_id: 6
        name: API Admin Group
        members: user1,user3

- name: Remove one permission from an admin group
    xbh03.device42.d42_api_admingroups:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: API Admin Group
        permissions_remove:
            - Delete objects

- name: Delete admin group by name
    xbh03.device42.d42_api_admingroups:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        name: API Admin Group

- name: Delete admin group by name with username and password auth
    xbh03.device42.d42_api_admingroups:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: absent
        name: API Admin Group
"""

RETURN = r"""
api_admingroup:
    description: Current or resulting admin group data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create, update, or delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.admin_users_groups.d42_admingroups import (
        d42_admingroups,
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


def _find_admin_group(helper, group_id=None, name=None):
    payload = helper.d42_get_admingroups(include_cols="permissions")
    groups = payload.get("admingroups", [])

    resolved_group_id = None
    if group_id is not None:
        resolved_group_id = int(group_id)

    for group in groups:
        current_id = group.get("id")
        try:
            current_id = int(current_id)
        except (TypeError, ValueError):
            current_id = None

        if resolved_group_id is not None and current_id == resolved_group_id:
            return group
        if resolved_group_id is None and name is not None and group.get("name") == name:
            return group

    return None


def _needs_update(existing, desired_name=None, members=None, members_remove=None, permissions=None, permissions_remove=None):
    if existing is None:
        return True

    if desired_name is not None and existing.get("name") != desired_name:
        return True

    current_members = set(_normalize_multi_value(existing.get("members")))
    current_permissions = set(_normalize_multi_value(existing.get("permissions")))

    if members is not None:
        desired_members = set(_normalize_multi_value(members))
        if not desired_members.issubset(current_members):
            return True
    elif members_remove is not None:
        if current_members.intersection(_normalize_multi_value(members_remove)):
            return True

    if permissions is not None:
        desired_permissions = set(_normalize_multi_value(permissions))
        if not desired_permissions.issubset(current_permissions):
            return True
    elif permissions_remove is not None:
        if current_permissions.intersection(_normalize_multi_value(permissions_remove)):
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
            group_id=dict(type="int", required=False),
            name=dict(type="str", required=False),
            members=dict(type="raw", required=False),
            members_remove=dict(type="raw", required=False),
            permissions=dict(type="raw", required=False),
            permissions_remove=dict(type="raw", required=False),
    )

    module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True,
            required_one_of=[("client_key", "userid"), ("group_id", "name")],
    )

    result = dict(changed=False)

    if module.params["state"] == "present" and module.params["name"] is None and module.params["group_id"] is None:
        module.fail_json(msg="Either name or group_id is required when state=present.")

    helper = d42_admingroups(
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
    group_id = module.params["group_id"]
    name = module.params["name"]
    members = module.params["members"]
    members_remove = module.params["members_remove"] if members is None else None
    permissions = module.params["permissions"]
    permissions_remove = module.params["permissions_remove"] if permissions is None else None

    existing = _find_admin_group(helper=helper, group_id=group_id, name=name)

    if state == "present" and existing is None and name is None:
        module.fail_json(msg="name is required to create a new admin group when group_id does not match an existing group.")

    if state == "absent":
        if not existing:
            result["msg"] = "Admin group already absent"
            module.exit_json(**result)

        result["api_admingroup"] = existing
        result["changed"] = True

        if module.check_mode:
            result["msg"] = "Admin group would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_admingroup(group_id=existing.get("id"))
        result["response"] = response
        module.exit_json(**result)

    needs_change = _needs_update(
            existing=existing,
            desired_name=name,
            members=members,
            members_remove=members_remove,
            permissions=permissions,
            permissions_remove=permissions_remove,
    )

    if not needs_change:
        result["api_admingroup"] = existing
        result["msg"] = "Admin group already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Admin group would be created/updated"
        if existing:
            result["api_admingroup"] = existing
        module.exit_json(**result)

    response = helper.d42_post_admingroups(
            group_id=group_id if group_id is not None else (existing.get("id") if existing else None),
            name=name,
            members=_as_api_value(members),
            members_remove=_as_api_value(members_remove),
            permissions=_as_api_value(permissions),
            permissions_remove=_as_api_value(permissions_remove),
    )

    result["response"] = response
    result["api_admingroup"] = _find_admin_group(
            helper=helper,
            group_id=group_id if group_id is not None else response.get("id"),
            name=name,
    )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
