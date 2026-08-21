#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_ipam_dns_records
short_description: Manage Device42 IPAM DNS records
description:
    - Create, update, or delete Device42 DNS records.
    - Supports C(POST /api/1.0/dns/records/) and C(DELETE /api/1.0/dns/records/{id}/).
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
            - Desired state of the DNS record.
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
            - DNS record ID.
            - Required when C(state=absent).
        required: false
        type: int
        aliases: [dns_record_id]
    domain:
        description:
            - Domain name.
            - Required when C(state=present).
        required: false
        type: str
    type:
        description:
            - DNS record type.
            - Required when C(state=present).
        required: false
        type: str
    nameserver:
        description:
            - Name server used to disambiguate overlapping domains.
        required: false
        type: str
    name:
        description:
            - Record name (use C(@) for blank).
        required: false
        type: str
    content:
        description:
            - Record content.
        required: false
        type: str
    content_raw:
        description:
            - Raw content preserving leading/trailing whitespace.
        required: false
        type: str
    new_content:
        description:
            - New content to overwrite existing content.
        required: false
        type: str
    new_content_raw:
        description:
            - Raw new content preserving leading/trailing whitespace.
        required: false
        type: str
    prio:
        description:
            - Priority (for MX records).
        required: false
        type: str
    ttl:
        description:
            - TTL value.
        required: false
        type: str
    tags:
        description:
            - Tags for the DNS record.
        required: false
        type: str
    tags_remove:
        description:
            - Tags to remove from the DNS record.
        required: false
        type: str
    change_date:
        description:
            - Days it takes for DNS change to occur.
        required: false
        type: int
"""

EXAMPLES = r"""
- name: Create DNS record
    xbh03.device42.ipam.dns.d42_api_ipam_dns_records:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        domain: example.local
        type: A
        name: www
        content: 10.10.10.20

- name: Update DNS record
    xbh03.device42.ipam.dns.d42_api_ipam_dns_records:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        domain: example.local
        type: TXT
        name: @
        content: old value
        new_content: new value

- name: Delete DNS record
    xbh03.device42.ipam.dns.d42_api_ipam_dns_records:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        id: 114
"""

RETURN = r"""
api_dns_record:
    description: Current or resulting DNS record data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 create/update/delete operations.
    type: dict
    returned: when changed
"""

import re

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.ipam.dns.d42_ipam_dns import (
    d42_ipam_dns,
)


def _extract_dns_record_id_from_response(response):
    if not isinstance(response, dict):
        return None

    msg = response.get("msg")
    if isinstance(msg, list):
        for item in msg:
            try:
                return int(item)
            except (TypeError, ValueError):
                if isinstance(item, str):
                    match = re.search(r"'?(\\d+)'?", item)
                    if match is not None:
                        return int(match.group(1))

    if response.get("id") is not None:
        try:
            return int(response.get("id"))
        except (TypeError, ValueError):
            return None

    return None


def _find_dns_record(helper, record_id=None, domain=None, record_type=None, name=None, nameserver=None, content=None):
    if record_id is not None:
        offset = 0
        limit = 1000
        while True:
            payload = helper.d42_get_dns_records(limit=limit, offset=offset)
            records = payload.get("records", []) if isinstance(payload, dict) else []
            if not isinstance(records, list) or len(records) == 0:
                return None

            for record in records:
                if str(record.get("id")) == str(record_id):
                    return record

            offset += len(records)
            total_count = payload.get("total_count") if isinstance(payload, dict) else None
            if total_count is not None:
                try:
                    if offset >= int(total_count):
                        return None
                except (TypeError, ValueError):
                    pass

    if domain is None or record_type is None:
        return None

    payload = helper.d42_get_dns_records(
        domain=domain,
        record_type=record_type,
        name=name,
        nameserver=nameserver,
        content=content,
        limit=100,
        offset=0,
    )

    for record in payload.get("records", []) if isinstance(payload, dict) else []:
        if str(record.get("domain")) != str(domain):
            continue
        if str(record.get("type")) != str(record_type):
            continue
        if name is not None and str(record.get("name")) != str(name):
            continue
        if nameserver is not None and str(record.get("nameserver")) != str(nameserver):
            continue
        return record

    return None


def _build_payload(params):
    return {
        "domain": params.get("domain"),
        "record_type": params.get("type"),
        "nameserver": params.get("nameserver"),
        "name": params.get("name"),
        "content": params.get("content"),
        "content_raw": params.get("content_raw"),
        "new_content": params.get("new_content"),
        "new_content_raw": params.get("new_content_raw"),
        "prio": params.get("prio"),
        "ttl": params.get("ttl"),
        "tags": params.get("tags"),
        "tags_remove": params.get("tags_remove"),
        "change_date": params.get("change_date"),
    }


def _needs_update(existing, payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    for desired_key, existing_key in (
        ("domain", "domain"),
        ("record_type", "type"),
        ("name", "name"),
        ("nameserver", "nameserver"),
        ("content", "content"),
        ("prio", "prio"),
        ("ttl", "ttl"),
        ("change_date", "change_date"),
    ):
        desired = payload.get(desired_key)
        if desired is None:
            continue

        current = existing.get(existing_key)
        if str(current) != str(desired):
            return True

    for operation_key in ("content_raw", "new_content", "new_content_raw", "tags", "tags_remove"):
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
        id=dict(type="int", required=False, aliases=["dns_record_id"]),
        domain=dict(type="str", required=False),
        type=dict(type="str", required=False),
        nameserver=dict(type="str", required=False),
        name=dict(type="str", required=False),
        content=dict(type="str", required=False),
        content_raw=dict(type="str", required=False),
        new_content=dict(type="str", required=False),
        new_content_raw=dict(type="str", required=False),
        prio=dict(type="str", required=False),
        ttl=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        tags_remove=dict(type="str", required=False),
        change_date=dict(type="int", required=False),
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
    record_id = module.params["id"]

    if state == "absent":
        if record_id is None:
            module.fail_json(msg="id (or dns_record_id) is required when state=absent.")

        existing = _find_dns_record(helper=helper, record_id=record_id)
        if existing is None:
            result["msg"] = "DNS record already absent"
            module.exit_json(**result)

        result["changed"] = True
        result["api_dns_record"] = existing

        if module.check_mode:
            result["msg"] = "DNS record would be deleted"
            module.exit_json(**result)

        result["response"] = helper.d42_delete_dns_record(id=record_id)
        module.exit_json(**result)

    if module.params["domain"] is None or module.params["type"] is None:
        module.fail_json(msg="domain and type are required when state=present.")

    payload = _build_payload(module.params)
    existing = _find_dns_record(
        helper=helper,
        record_id=record_id,
        domain=module.params["domain"],
        record_type=module.params["type"],
        name=module.params["name"],
        nameserver=module.params["nameserver"],
        content=module.params["content"],
    )

    if not _needs_update(existing=existing, payload=payload, force_update=module.params["force_update"]):
        result["api_dns_record"] = existing
        result["msg"] = "DNS record already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "DNS record would be created/updated"
        if existing is not None:
            result["api_dns_record"] = existing
        module.exit_json(**result)

    result["response"] = helper.d42_post_dns_records(**payload)

    resolved_id = _extract_dns_record_id_from_response(result["response"])
    if resolved_id is None and existing is not None:
        resolved_id = existing.get("id")

    result["api_dns_record"] = _find_dns_record(
        helper=helper,
        record_id=resolved_id,
        domain=module.params["domain"],
        record_type=module.params["type"],
        name=module.params["name"],
        nameserver=module.params["nameserver"],
        content=module.params["content"],
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
