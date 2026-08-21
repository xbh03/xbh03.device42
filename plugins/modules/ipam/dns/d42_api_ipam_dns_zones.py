#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_dns_zones
short_description: Manage Device42 IPAM DNS zones
description:
    - Create, update, or delete Device42 DNS zones.
    - Supports C(POST /api/1.0/dns/zones/) and C(DELETE /api/1.0/dns/zones/{id}/).
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
            - Desired state of the DNS zone.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    force_update:
        description:
            - Force POST call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    id:
        description:
            - DNS zone ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [dns_zone_id]
    name:
        description:
            - DNS zone name.
            - Required when C(state=present).
        required: false
        type: str
    nameserver:
        description:
            - Name server hostname or IP.
            - Required when C(state=present).
        required: false
        type: str
    notes:
        description:
            - Additional notes.
        required: false
        type: str
    vrf_group:
        description:
            - VRF group name.
        required: false
        type: str
    vrf_group_id:
        description:
            - VRF group ID.
        required: false
        type: int
    tags:
        description:
            - Tags for grouping zone entries.
        required: false
        type: str
    tags_remove:
        description:
            - Tags to remove from grouping zone entries.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create DNS zone
    xbh03.device42.ipam.dns.d42_api_ipam_dns_zones:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        name: DNS_host
        nameserver: 10.10.10.10

- name: Update DNS zone
    xbh03.device42.ipam.dns.d42_api_ipam_dns_zones:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        name: DNS_host
        nameserver: ns1.example.local
        notes: Updated by Ansible

- name: Delete DNS zone
    xbh03.device42.ipam.dns.d42_api_ipam_dns_zones:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        id: 114
"""

RETURN = r"""
api_dns_zone:
    description: Current or resulting DNS zone data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 create/update/delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.dns.d42_ipam_dns import (
    d42_ipam_dns,
)


def _extract_dns_zone_id_from_response(response):
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


def _find_dns_zone(helper, zone_id=None, name=None, nameserver=None):
    if zone_id is not None:
        payload = helper.d42_get_dns_zones(dns_zone_id=zone_id, limit=1, offset=0)
        zones = payload.get("dns_zones", []) if isinstance(payload, dict) else []
        if isinstance(zones, list) and len(zones) > 0:
            return zones[0]
        return None

    if name is None:
        return None

    payload = helper.d42_get_dns_zones(domain=name, nameserver=nameserver, limit=100, offset=0)
    for zone in payload.get("dns_zones", []) if isinstance(payload, dict) else []:
        zone_name = zone.get("domain") or zone.get("name")
        if str(zone_name) != str(name):
            continue
        if nameserver is not None and str(zone.get("nameserver")) != str(nameserver):
            continue
        return zone

    return None


def _build_payload(params):
    return {
        "name": params.get("name"),
        "nameserver": params.get("nameserver"),
        "notes": params.get("notes"),
        "vrf_group": params.get("vrf_group"),
        "vrf_group_id": params.get("vrf_group_id"),
        "tags": params.get("tags"),
        "tags_remove": params.get("tags_remove"),
    }


def _needs_update(existing, payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    for desired_key, existing_key in (
        ("name", "domain"),
        ("nameserver", "nameserver"),
        ("notes", "notes"),
        ("vrf_group", "vrf_group"),
        ("vrf_group_id", "vrf_group_id"),
    ):
        desired = payload.get(desired_key)
        if desired is None:
            continue

        current = existing.get(existing_key)
        if str(current) != str(desired):
            return True

    for operation_key in ("tags", "tags_remove"):
        if payload.get(operation_key) is not None:
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
        force_update=dict(type="bool", required=False, default=False),
        id=dict(type="int", required=False, aliases=["dns_zone_id"]),
        name=dict(type="str", required=False),
        nameserver=dict(type="str", required=False),
        notes=dict(type="str", required=False),
        vrf_group=dict(type="str", required=False),
        vrf_group_id=dict(type="int", required=False),
        tags=dict(type="str", required=False),
        tags_remove=dict(type="str", required=False),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

    helper = d42_ipam_dns(
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
    zone_id = module.params["id"]

    if state == "absent":
        if zone_id is None:
            module.fail_json(msg="id (or dns_zone_id) is required when state=absent.")

        existing = _find_dns_zone(helper=helper, zone_id=zone_id)
        if existing is None:
            result["msg"] = "DNS zone already absent"
            module.exit_json(**result)

        result["changed"] = True
        result["api_dns_zone"] = existing

        if module.check_mode:
            result["msg"] = "DNS zone would be deleted"
            module.exit_json(**result)

        result["response"] = helper.d42_delete_dns_zone(id=zone_id)
        module.exit_json(**result)

    if module.params["name"] is None or module.params["nameserver"] is None:
        module.fail_json(msg="name and nameserver are required when state=present.")

    payload = _build_payload(module.params)
    existing = _find_dns_zone(
        helper=helper,
        zone_id=zone_id,
        name=module.params["name"],
        nameserver=module.params["nameserver"],
    )

    if not _needs_update(existing=existing, payload=payload, force_update=module.params["force_update"]):
        result["api_dns_zone"] = existing
        result["msg"] = "DNS zone already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "DNS zone would be created/updated"
        if existing is not None:
            result["api_dns_zone"] = existing
        module.exit_json(**result)

    result["response"] = helper.d42_post_dns_zones(**payload)

    resolved_id = _extract_dns_zone_id_from_response(result["response"])
    if resolved_id is None and existing is not None:
        resolved_id = existing.get("id") or existing.get("dns_zone_id")

    result["api_dns_zone"] = _find_dns_zone(
        helper=helper,
        zone_id=resolved_id,
        name=module.params["name"],
        nameserver=module.params["nameserver"],
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
