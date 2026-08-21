#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_vlans_info
short_description: Get Device42 IPAM VLANs
description:
    - Retrieve VLANs from Device42 IPAM.
    - Supports filter parameters documented for C(/api/1.0/vlans/).
    - Supports specific VLAN retrieval for C(/api/1.0/vlans/{id}/).
version_added: "0.1.0"
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
        required: true
        type: str
    client_secret_key:
        description:
            - Device42 API client secret key used to authenticate.
        required: true
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
    query_type:
        description:
            - Query mode.
            - Use C(list) for list endpoint or C(specific) for VLAN-by-id endpoint.
        required: false
        type: str
        default: list
        choices:
            - list
            - specific
    vlan_id:
        description:
            - VLAN ID filter.
            - Required when C(query_type=specific).
        required: false
        type: int
    number:
        description:
            - VLAN number filter.
        required: false
        type: int
    name:
        description:
            - VLAN name filter.
        required: false
        type: str
    tags:
        description:
            - OR filter by tags (comma separated).
        required: false
        type: str
    tags_and:
        description:
            - AND filter by tags (comma separated).
        required: false
        type: str
    description:
        description:
            - VLAN description filter (case-insensitive exact match).
        required: false
        type: str
    switch_ids:
        description:
            - CSV list of switch IDs.
        required: false
        type: str
    switches:
        description:
            - CSV list of switch names.
        required: false
        type: str
    last_updated_lt:
        description:
            - Filter by last updated date less than value (YYYY-MM-DD).
        required: false
        type: str
    last_updated_gt:
        description:
            - Filter by last updated date greater than or equal to value (YYYY-MM-DD).
        required: false
        type: str
    first_added_lt:
        description:
            - Filter by first added date less than value (YYYY-MM-DD).
        required: false
        type: str
    first_added_gt:
        description:
            - Filter by first added date greater than or equal to value (YYYY-MM-DD).
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Get all VLANs
    xbh03.device42.d42_ipam_vlans_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: list

- name: Get VLAN by ID
    xbh03.device42.d42_ipam_vlans_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: specific
        vlan_id: 13

- name: Filter VLANs by number and switches
    xbh03.device42.d42_ipam_vlans_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        number: 20
        switches: nh-lab-switch-01
"""

RETURN = r"""
ipam_vlans:
    description: Raw response from Device42 VLANs endpoint.
    type: dict
    returned: success
    sample: |
        vlans:
            - vlan_id: 13
                name: CRMConsultant
                number: 20
                description: ""
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.vlans.d42_ipam_vlans import (
        d42_ipam_vlans,
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
                query_type=dict(type="str", required=False, default="list", choices=["list", "specific"]),
                vlan_id=dict(type="int", required=False),
                number=dict(type="int", required=False),
                name=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_and=dict(type="str", required=False),
                description=dict(type="str", required=False),
                switch_ids=dict(type="str", required=False),
                switches=dict(type="str", required=False),
                last_updated_lt=dict(type="str", required=False),
                last_updated_gt=dict(type="str", required=False),
                first_added_lt=dict(type="str", required=False),
                first_added_gt=dict(type="str", required=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_ipam_vlans(
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

        query_type = module.params["query_type"]

        if query_type == "specific":
            if module.params["vlan_id"] is None:
                module.fail_json(msg="vlan_id is required when query_type=specific.")

            result["ipam_vlans"] = helper.d42_get_vlan_by_id(id=module.params["vlan_id"])
            module.exit_json(**result)

        ipam_vlans = helper.d42_get_vlans(
                vlan_id=module.params["vlan_id"],
                number=module.params["number"],
                name=module.params["name"],
                tags=module.params["tags"],
                tags_and=module.params["tags_and"],
                description=module.params["description"],
                switch_ids=module.params["switch_ids"],
                switches=module.params["switches"],
                last_updated_lt=module.params["last_updated_lt"],
                last_updated_gt=module.params["last_updated_gt"],
                first_added_lt=module.params["first_added_lt"],
                first_added_gt=module.params["first_added_gt"],
        )

        result["ipam_vlans"] = ipam_vlans
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
