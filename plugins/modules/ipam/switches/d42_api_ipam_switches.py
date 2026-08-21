#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_switches
short_description: Manage Device42 switches using switch templates
description:
    - Create or update switches and switch ports via switch templates.
    - Supports C(POST /api/1.0/switches/).
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
            - Desired state of switch template assignment.
        required: false
        type: str
        default: present
        choices:
            - present
    switch_template_id:
        description:
            - Switch template ID.
            - Required for C(state=present).
        required: false
        type: str
    device:
        description:
            - Device name (new or existing).
        required: false
        type: str
    device_id:
        description:
            - Existing Device42 device ID.
        required: false
        type: str
    devices:
        description:
            - Comma-separated names of new devices.
        required: false
        type: str
    device_ids:
        description:
            - Comma-separated IDs of existing devices.
        required: false
        type: str
    assets:
        description:
            - Comma-separated names of new assets.
        required: false
        type: str
    asset_ids:
        description:
            - Comma-separated IDs of existing assets.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Add switch ports to a device using a template
    xbh03.device42.ipam.switches.d42_api_ipam_switches:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        device: oxctrouter
        switch_template_id: "12"

- name: Add switch ports by device ID
    xbh03.device42.ipam.switches.d42_api_ipam_switches:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        device_id: "337"
        switch_template_id: "12"

- name: Bulk apply with multiple devices/assets
    xbh03.device42.ipam.switches.d42_api_ipam_switches:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        device: core-switch-01
        switch_template_id: "12"
        devices: edge-01,edge-02
        assets: asset-edge-03,asset-edge-04
"""

RETURN = r"""
response:
    description: Raw response from Device42 switch template operation.
    type: dict
    returned: success
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.switches.d42_ipam_switches import (
    d42_ipam_switches,
)


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
        state=dict(type="str", required=False, default="present", choices=["present"]),
        switch_template_id=dict(type="str", required=False),
        device=dict(type="str", required=False),
        device_id=dict(type="str", required=False),
        devices=dict(type="str", required=False),
        device_ids=dict(type="str", required=False),
        assets=dict(type="str", required=False),
        asset_ids=dict(type="str", required=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    helper = d42_ipam_switches(
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

    if module.params["switch_template_id"] is None:
        module.fail_json(msg="switch_template_id is required when state=present.")

    if module.params["device"] is None and module.params["device_id"] is None:
        module.fail_json(msg="Either device or device_id is required when state=present.")

    result["changed"] = True

    if module.check_mode:
        result["msg"] = "Switch ports would be created/updated via template"
        module.exit_json(**result)

    result["response"] = helper.d42_post_switches(
        switch_template_id=module.params["switch_template_id"],
        device=module.params["device"],
        device_id=module.params["device_id"],
        devices=module.params["devices"],
        device_ids=module.params["device_ids"],
        assets=module.params["assets"],
        asset_ids=module.params["asset_ids"],
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
