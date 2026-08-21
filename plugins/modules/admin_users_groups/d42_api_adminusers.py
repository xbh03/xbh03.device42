#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_adminusers
short_description: Manage Device42 admin users
description:
  - Create, update, or delete Device42 admin users.
  - Device42 exposes create and update through POST on the same endpoint.
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
      - Desired state of the admin user.
    required: false
    type: str
    default: present
    choices:
      - present
      - absent
  user_id:
    description:
      - Device42 admin user ID.
      - Used to target a specific admin user.
    required: false
    type: int
  username:
    description:
      - Admin username.
      - Required when creating a user if C(user_id) is not provided.
    required: false
    type: str
  new_password:
    description:
      - Password to set on the managed admin user.
      - Required when creating a new user.
      - Separate from C(password), which is used for authentication.
    required: false
    type: str
  first_name:
    description:
      - First name of admin user.
    required: false
    type: str
  last_name:
    description:
      - Last name of admin user.
    required: false
    type: str
  email:
    description:
      - Email address of admin user.
    required: false
    type: str
  is_superuser:
    description:
      - Whether the admin user is superuser.
    required: false
    type: bool
  is_staff:
    description:
      - Whether the admin user is staff.
    required: false
    type: bool
  is_active:
    description:
      - Whether the admin user is active.
    required: false
    type: bool
  password_doesnt_expire:
    description:
      - Whether the managed admin user's password does not expire.
    required: false
    type: bool
  groups:
    description:
      - Admin groups to assign to the user.
      - Accepts a comma-separated string or a list.
    required: false
    type: raw
  new_username:
    description:
      - New username for an existing admin user.
    required: false
    type: str
  force_update:
    description:
      - Force update call for existing user when C(state=present).
      - Useful when rotating C(new_password).
    required: false
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Create admin user
  xbh03.device42.d42_api_adminusers:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: present
    username: JohnDoe
    new_password: Secret123!
    first_name: John
    last_name: Doe
    email: john.doe@example.internal
    is_superuser: false
    is_staff: true
    is_active: true
    password_doesnt_expire: false
    groups:
      - System Generated Read Only

- name: Update admin user and change username
  xbh03.device42.d42_api_adminusers:
    host: device42.example.internal
    userid: admin
    password: admin-secret
    state: present
    user_id: 125
    username: JohnDoe
    new_username: John.Doe
    is_active: true

- name: Delete admin user by username
  xbh03.device42.d42_api_adminusers:
    host: device42.example.internal
    client_key: abc123
    client_secret_key: secret123
    state: absent
    username: JohnDoe
"""

RETURN = r"""
api_adminuser:
  description: Current or resulting admin user data when available.
  type: dict
  returned: success
response:
  description: Raw response from Device42 for create/update/delete operations.
  type: dict
  returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.admin_users_groups.d42_adminusers import (
    d42_adminusers,
)


def _normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


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


def _as_api_groups(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value

    serialized = []
    for group_name in _normalize_multi_value(value):
        if "," in group_name and not (group_name.startswith('"') and group_name.endswith('"')):
            serialized.append(f'"{group_name}"')
        else:
            serialized.append(group_name)
    return ",".join(serialized)


def _find_adminuser_by_id(helper, user_id):
    if user_id is None:
        return None

    payload = helper.d42_get_adminusers()
    users = payload.get("adminusers", [])
    for user in users:
        try:
            current_id = int(user.get("id", -1))
        except (TypeError, ValueError):
            current_id = -1
        if current_id == int(user_id):
            return user
    return None


def _find_adminuser_by_username(helper, username):
    if not username:
        return None

    payload = helper.d42_get_adminusers(username=username)
    users = payload.get("adminusers", [])
    for user in users:
        if user.get("username") == username:
            return user
    return None


def _find_adminuser(helper, user_id=None, username=None):
    if user_id is not None:
        return _find_adminuser_by_id(helper=helper, user_id=user_id)
    return _find_adminuser_by_username(helper=helper, username=username)


def _needs_update(existing, params):
    if existing is None:
        return True

    if params["username"] is not None and existing.get("username") != params["username"]:
        return True

    if params["new_username"] is not None and params["new_username"] != existing.get("username"):
        return True

    if params["first_name"] is not None and existing.get("first_name") != params["first_name"]:
        return True

    if params["last_name"] is not None and existing.get("last_name") != params["last_name"]:
        return True

    if params["email"] is not None and existing.get("email") != params["email"]:
        return True

    if params["is_superuser"] is not None and _normalize_bool(existing.get("is_superuser")) != bool(params["is_superuser"]):
        return True

    if params["is_staff"] is not None and _normalize_bool(existing.get("is_staff")) != bool(params["is_staff"]):
        return True

    if params["is_active"] is not None and _normalize_bool(existing.get("is_active")) != bool(params["is_active"]):
        return True

    if params["password_doesnt_expire"] is not None and _normalize_bool(existing.get("password_doesnt_expire")) != bool(params["password_doesnt_expire"]):
        return True

    if params["groups"] is not None:
        desired_groups = set(_normalize_multi_value(params["groups"]))
        current_groups = set(_normalize_multi_value(existing.get("groups")))
        if desired_groups != current_groups:
            return True

    if params["new_password"] is not None:
        # Password value is not returned by GET, so we cannot compare.
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
        user_id=dict(type="int", required=False),
        username=dict(type="str", required=False),
        new_password=dict(type="str", required=False, no_log=True),
        first_name=dict(type="str", required=False),
        last_name=dict(type="str", required=False),
        email=dict(type="str", required=False),
        is_superuser=dict(type="bool", required=False),
        is_staff=dict(type="bool", required=False),
        is_active=dict(type="bool", required=False),
        password_doesnt_expire=dict(type="bool", required=False),
        groups=dict(type="raw", required=False),
        new_username=dict(type="str", required=False),
        force_update=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[("user_id", "username")],
    )

    result = dict(changed=False)

    helper = d42_adminusers(
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
    user_id = module.params["user_id"]
    username = module.params["username"]

    existing = _find_adminuser(helper=helper, user_id=user_id, username=username)

    if state == "absent":
        if not existing:
            result["msg"] = "Admin user already absent"
            module.exit_json(**result)

        result["api_adminuser"] = existing
        result["changed"] = True

        if module.check_mode:
            result["msg"] = "Admin user would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_adminuser(user_id=existing.get("id"))
        result["response"] = response
        module.exit_json(**result)

    if existing is None and module.params["username"] is None:
        module.fail_json(msg="username is required to create a new admin user when user_id does not match an existing user.")

    if existing is None and module.params["new_password"] is None:
        module.fail_json(msg="new_password is required when creating a new admin user.")

    if not _needs_update(existing=existing, params=module.params):
        result["api_adminuser"] = existing
        result["msg"] = "Admin user already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Admin user would be created/updated"
        if existing:
            result["api_adminuser"] = existing
        module.exit_json(**result)

    response = helper.d42_post_adminusers(
        user_id=user_id if user_id is not None else (existing.get("id") if existing else None),
        username=module.params["username"],
        password=module.params["new_password"],
        first_name=module.params["first_name"],
        last_name=module.params["last_name"],
        email=module.params["email"],
        is_superuser=module.params["is_superuser"],
        is_staff=module.params["is_staff"],
        is_active=module.params["is_active"],
        password_doesnt_expire=module.params["password_doesnt_expire"],
        groups=_as_api_groups(module.params["groups"]),
        new_username=module.params["new_username"],
    )

    result["response"] = response
    result["api_adminuser"] = _find_adminuser(
        helper=helper,
        user_id=user_id if user_id is not None else (existing.get("id") if existing else None),
        username=module.params["new_username"] or module.params["username"],
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
