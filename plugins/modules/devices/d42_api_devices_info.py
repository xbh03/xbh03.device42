#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_devices_info
short_description: Get Device42 devices
description:
    - Retrieve information about Device42 devices from the v2 endpoint.
    - Supports list endpoint C(/api/2.0/devices/), specific device endpoint C(/api/2.0/devices/{id}/), and mountpoints endpoint C(/api/2.0/device/mountpoints/).
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
            - Select which devices endpoint to query.
            - Use C(list) for C(/api/2.0/devices/).
            - Use C(specific) for C(/api/2.0/devices/{id}/).
            - Use C(mountpoints) for C(/api/2.0/device/mountpoints/).
        required: false
        type: str
        default: list
        choices:
            - list
            - specific
            - mountpoints
    include_cols:
        description:
            - Return only specified columns.
        required: false
        type: str
    device_id:
        description:
            - Device42 device ID.
        required: false
        type: int
    name:
        description:
            - Filter by device name.
        required: false
        type: str
    serial_no:
        description:
            - Filter by serial number.
        required: false
        type: str
    serial_no_contains:
        description:
            - Filter by partial serial number match.
        required: false
        type: str
    asset_no:
        description:
            - Filter by asset number.
        required: false
        type: str
    asset_no_contains:
        description:
            - Filter by partial asset number match.
        required: false
        type: str
    uuid:
        description:
            - Filter by exact UUID.
        required: false
        type: str
    in_service:
        description:
            - Filter by in-service status.
            - Use C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    service_level:
        description:
            - Filter by service level name.
        required: false
        type: str
    service_level_id:
        description:
            - Filter by service level ID.
        required: false
        type: int
    device_type:
        description:
            - Filter by device type.
        required: false
        type: str
        choices:
            - unknown
            - physical
            - virtual
            - cluster
    type_id:
        description:
            - Filter by type ID.
            - 1 unknown, 2 physical, 3 virtual, 4 cluster.
        required: false
        type: int
    last_edited_lt:
        description:
            - Filter by last edited date less than value (YYYY-MM-DD).
        required: false
        type: str
    last_edited_gt:
        description:
            - Filter by last edited date greater than value (YYYY-MM-DD).
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
    objectcategory_id:
        description:
            - Filter by object category ID.
        required: false
        type: int
    objectcategory:
        description:
            - Filter by object category name.
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
    cluster_device_id:
        description:
            - Filter by cluster device ID.
        required: false
        type: int
    customer_id:
        description:
            - Filter by customer ID.
        required: false
        type: int
    customer:
        description:
            - Filter by customer name.
        required: false
        type: str
    hardware_id:
        description:
            - Filter by hardware ID.
        required: false
        type: int
    hardware:
        description:
            - Filter by hardware name.
        required: false
        type: str
    device_host_chassis_id:
        description:
            - Filter by host chassis device ID.
        required: false
        type: int
    device_virtual_host_id:
        description:
            - Filter by virtual host device ID.
        required: false
        type: int
    rack_id:
        description:
            - Filter by rack ID.
        required: false
        type: int
    virtualsubtype:
        description:
            - Filter by virtual subtype name.
        required: false
        type: str
    virtualsubtype_id:
        description:
            - Filter by virtual subtype ID.
        required: false
        type: int
    os_id:
        description:
            - Filter by OS ID.
        required: false
        type: int
    os_name:
        description:
            - Filter by OS name.
        required: false
        type: str
    custom_fields_and:
        description:
            - AND filter by custom fields in format key1:value1,key2:value2.
        required: false
        type: str
    custom_fields_or:
        description:
            - OR filter by custom fields in format key1:value1,key2:value2.
        required: false
        type: str
    virtual_host:
        description:
            - Filter by virtual host status.
            - Use C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    blade_chassis:
        description:
            - Filter by blade chassis status.
            - Use C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    physicalsubtype:
        description:
            - Filter by physical subtype name.
        required: false
        type: str
    physicalsubtype_id:
        description:
            - Filter by physical subtype ID.
        required: false
        type: int
    filesystem:
        description:
            - Filter mountpoints by filesystem name.
            - Used only when C(query_type=mountpoints).
        required: false
        type: str
    fstype:
        description:
            - Filter mountpoints by filesystem type.
            - Used only when C(query_type=mountpoints).
        required: false
        type: str
    limit:
        description:
            - Number of devices to return.
        required: false
        type: int
        default: 1000
    offset:
        description:
            - Start position for pagination.
        required: false
        type: int
        default: 0
    fetch_all:
        description:
            - Retrieve all devices using automatic pagination.
            - When true, C(limit) and C(offset) are ignored.
        required: false
        type: bool
        default: false
"""

EXAMPLES = r"""
- name: Get Device42 devices
    xbh03.device42.d42_api_devices_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123

- name: Get Device42 device by ID
    xbh03.device42.d42_api_devices_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: specific
        device_id: 64

- name: Get Device42 device mountpoints for specific device
    xbh03.device42.d42_api_devices_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        query_type: mountpoints
        device_id: 64
        fstype: NTFS

- name: Get Device42 devices filtered by type and service level
    xbh03.device42.d42_api_devices_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        device_type: physical
        service_level: In Service

- name: Get all Device42 devices with automatic pagination
    xbh03.device42.d42_api_devices_info:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        fetch_all: true
"""

RETURN = r"""
api_devices:
    description: Raw response from Device42 devices endpoint.
    type: dict
    returned: success
    sample: |
        Devices:
            total_count: "709"
            limit: "1"
            devices:
                - name: Device_Name
                    type_id: 2
                    serial_no: FOC1252W6EW
                    asset_no: "123456"
                    device_url: /api/2.0/devices/64/
                    device_id: "64"
                    type: physical
                    uuid: ""
            offset: "0"
api_device:
    description: Raw response from Device42 specific device endpoint.
    type: dict
    returned: when query_type=specific
api_device_mountpoints:
    description: Raw response from Device42 device mountpoints endpoint.
    type: dict
    returned: when query_type=mountpoints
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.devices.d42_devices import (
        d42_devices,
)


def _extract_devices_container(payload):
        devices_container = payload.get("Devices")
        if isinstance(devices_container, dict):
                return devices_container
        return payload


def _extract_devices_list(payload):
        container = _extract_devices_container(payload)
        devices = container.get("devices")
        if isinstance(devices, list):
                return devices
        return []


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
                query_type=dict(type="str", required=False, default="list", choices=["list", "specific", "mountpoints"]),
                include_cols=dict(type="str", required=False),
                device_id=dict(type="int", required=False),
                name=dict(type="str", required=False),
                serial_no=dict(type="str", required=False),
                serial_no_contains=dict(type="str", required=False),
                asset_no=dict(type="str", required=False),
                asset_no_contains=dict(type="str", required=False),
                uuid=dict(type="str", required=False),
                in_service=dict(type="str", required=False, choices=["yes", "no"]),
                service_level=dict(type="str", required=False),
                service_level_id=dict(type="int", required=False),
                device_type=dict(
                        type="str",
                        required=False,
                        choices=["unknown", "physical", "virtual", "cluster"],
                ),
                type_id=dict(type="int", required=False),
                last_edited_lt=dict(type="str", required=False),
                last_edited_gt=dict(type="str", required=False),
                first_added_lt=dict(type="str", required=False),
                first_added_gt=dict(type="str", required=False),
                objectcategory_id=dict(type="int", required=False),
                objectcategory=dict(type="str", required=False),
                tags=dict(type="str", required=False),
                tags_and=dict(type="str", required=False),
                cluster_device_id=dict(type="int", required=False),
                customer_id=dict(type="int", required=False),
                customer=dict(type="str", required=False),
                hardware_id=dict(type="int", required=False),
                hardware=dict(type="str", required=False),
                device_host_chassis_id=dict(type="int", required=False),
                device_virtual_host_id=dict(type="int", required=False),
                rack_id=dict(type="int", required=False),
                virtualsubtype=dict(type="str", required=False),
                virtualsubtype_id=dict(type="int", required=False),
                os_id=dict(type="int", required=False),
                os_name=dict(type="str", required=False),
                custom_fields_and=dict(type="str", required=False),
                custom_fields_or=dict(type="str", required=False),
                virtual_host=dict(type="str", required=False, choices=["yes", "no"]),
                blade_chassis=dict(type="str", required=False, choices=["yes", "no"]),
                physicalsubtype=dict(type="str", required=False),
                physicalsubtype_id=dict(type="int", required=False),
                filesystem=dict(type="str", required=False),
                fstype=dict(type="str", required=False),
                limit=dict(type="int", required=False, default=1000),
                offset=dict(type="int", required=False, default=0),
                fetch_all=dict(type="bool", required=False, default=False),
        )

        result = dict(changed=False)
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

        helper = d42_devices(
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

        base_filters = dict(
                include_cols=module.params["include_cols"],
                device_id=module.params["device_id"],
                name=module.params["name"],
                serial_no=module.params["serial_no"],
                serial_no_contains=module.params["serial_no_contains"],
                asset_no=module.params["asset_no"],
                asset_no_contains=module.params["asset_no_contains"],
                uuid=module.params["uuid"],
                in_service=module.params["in_service"],
                service_level=module.params["service_level"],
                service_level_id=module.params["service_level_id"],
                device_type=module.params["device_type"],
                type_id=module.params["type_id"],
                last_edited_lt=module.params["last_edited_lt"],
                last_edited_gt=module.params["last_edited_gt"],
                first_added_lt=module.params["first_added_lt"],
                first_added_gt=module.params["first_added_gt"],
                objectcategory_id=module.params["objectcategory_id"],
                objectcategory=module.params["objectcategory"],
                tags=module.params["tags"],
                tags_and=module.params["tags_and"],
                cluster_device_id=module.params["cluster_device_id"],
                customer_id=module.params["customer_id"],
                customer=module.params["customer"],
                hardware_id=module.params["hardware_id"],
                hardware=module.params["hardware"],
                device_host_chassis_id=module.params["device_host_chassis_id"],
                device_virtual_host_id=module.params["device_virtual_host_id"],
                rack_id=module.params["rack_id"],
                virtualsubtype=module.params["virtualsubtype"],
                virtualsubtype_id=module.params["virtualsubtype_id"],
                os_id=module.params["os_id"],
                os_name=module.params["os_name"],
                custom_fields_and=module.params["custom_fields_and"],
                custom_fields_or=module.params["custom_fields_or"],
                virtual_host=module.params["virtual_host"],
                blade_chassis=module.params["blade_chassis"],
                physicalsubtype=module.params["physicalsubtype"],
                physicalsubtype_id=module.params["physicalsubtype_id"],
        )

        query_type = module.params["query_type"]

        if query_type == "specific":
            if module.params["device_id"] is None:
                module.fail_json(msg="device_id is required when query_type=specific.")
            if module.params["fetch_all"]:
                module.fail_json(msg="fetch_all is not supported when query_type=specific.")

            result["api_device"] = helper.d42_get_device_by_id(
                device_id=module.params["device_id"],
                include_cols=module.params["include_cols"],
            )
            module.exit_json(**result)

        if query_type == "mountpoints":
            if module.params["fetch_all"]:
                module.fail_json(msg="fetch_all is not supported when query_type=mountpoints.")

            result["api_device_mountpoints"] = helper.d42_get_device_mountpoints(
                device_id=module.params["device_id"],
                filesystem=module.params["filesystem"],
                fstype=module.params["fstype"],
            )
            module.exit_json(**result)

        if module.params["fetch_all"]:
                page_size = 1000
                offset = 0
                merged = []
                total_count = None

                while True:
                        page = helper.d42_get_devices(limit=page_size, offset=offset, **base_filters)
                        container = _extract_devices_container(page)
                        page_devices = _extract_devices_list(page)
                        merged.extend(page_devices)

                        page_total = container.get("total_count")
                        try:
                                page_total = int(page_total)
                        except (TypeError, ValueError):
                                page_total = None

                        if page_total is not None:
                                total_count = page_total

                        if not page_devices:
                                break

                        offset += len(page_devices)
                        if total_count is not None and offset >= total_count:
                                break

                api_devices = {
                        "Devices": {
                                "devices": merged,
                                "total_count": str(total_count if total_count is not None else len(merged)),
                                "limit": str(len(merged)),
                                "offset": "0",
                        }
                }
        else:
                api_devices = helper.d42_get_devices(
                        limit=module.params["limit"],
                        offset=module.params["offset"],
                        **base_filters
                )

        result["api_devices"] = api_devices
        module.exit_json(**result)


def main():
        run_module()


if __name__ == "__main__":
        main()
