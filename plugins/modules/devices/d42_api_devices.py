#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: d42_api_devices
short_description: Manage Device42 devices
description:
    - Create, update, or delete Device42 devices.
    - Uses C(POST /api/2.0/devices/) for create/update, C(PUT /api/2.0/devices/{id}/) for update by ID,
      and C(DELETE /api/2.0/devices/{id}/) for deletion.
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
            - Desired state of the device.
        required: false
        type: str
        default: present
        choices:
            - present
            - absent
    present_endpoint:
        description:
            - Endpoint used when C(state=present).
            - C(post) uses C(/api/2.0/devices/) to create or update.
            - C(put) uses C(/api/2.0/devices/{id}/) to update by ID.
            - C(custom_fields) uses C(/api/1.0/custom_fields/device/).
        required: false
        type: str
        default: post
        choices:
            - post
            - put
            - custom_fields
    force_update:
        description:
            - Force update call when C(state=present) even if no drift is detected.
        required: false
        type: bool
        default: false
    delete_vms:
        description:
            - If deleting a host, also delete VMs on the host, C(yes) or C(no).
        required: false
        type: str
        choices:
            - yes
            - no
    device_id:
        description:
            - Device ID.
            - Required for C(state=absent) unless a resolvable identifier is provided.
        required: false
        type: int
    serial_no:
        description:
            - Device serial number.
            - Used as identifier for C(present_endpoint=post).
        required: false
        type: str
    name:
        description:
            - Device name.
            - Required to create a new device with C(present_endpoint=post) when no other identifier matches.
        required: false
        type: str
    asset_no:
        description:
            - Device asset number.
        required: false
        type: str
    uuid:
        description:
            - Device UUID.
        required: false
        type: str
    virtual_host:
        description:
            - Whether the device is a virtual host.
        required: false
        type: str
        choices:
            - yes
            - no
    in_service:
        description:
            - In service status.
        required: false
        type: str
        choices:
            - yes
            - no
    device_type_id:
        description:
            - Device type ID.
        required: false
        type: int
    device_type:
        description:
            - Device type name.
        required: false
        type: str
        choices:
            - unknown
            - physical
            - virtual
            - cluster
    physicalsubtype_id:
        description:
            - Physical subtype ID.
        required: false
        type: int
    physicalsubtype:
        description:
            - Physical subtype name.
        required: false
        type: str
    network_device:
        description:
            - Whether the device is a network device.
        required: false
        type: str
        choices:
            - yes
            - no
    blade_chassis:
        description:
            - Whether the device is a blade chassis.
        required: false
        type: str
        choices:
            - yes
            - no
    manufacturer:
        description:
            - Hardware manufacturer.
        required: false
        type: str
    hardware_id:
        description:
            - Hardware model ID.
        required: false
        type: int
    hardware:
        description:
            - Hardware model name.
        required: false
        type: str
    new_hardware:
        description:
            - Existing hardware model name to switch to.
        required: false
        type: str
    virtual_host_device_id:
        description:
            - Host ID of virtual device.
        required: false
        type: int
    virtual_host_device:
        description:
            - Host name of virtual device.
        required: false
        type: str
    host_chassis_device_id:
        description:
            - Host chassis device ID.
        required: false
        type: int
    host_chassis_device:
        description:
            - Host chassis device name.
        required: false
        type: str
    bladeno:
        description:
            - Blade slot number.
        required: false
        type: int
    chassisslot_id:
        description:
            - Chassis slot ID.
        required: false
        type: int
    service_level_id:
        description:
            - Service level ID.
        required: false
        type: int
    service_level:
        description:
            - Service level name.
        required: false
        type: str
    customer_id:
        description:
            - Legacy customer ID field.
        required: false
        type: int
    customer:
        description:
            - Legacy customer name field.
        required: false
        type: str
    customers:
        description:
            - CSV customer names to associate.
        required: false
        type: str
    customers_remove:
        description:
            - CSV customer names to disassociate.
        required: false
        type: str
    additional_location:
        description:
            - Additional location information.
        required: false
        type: str
    building_id:
        description:
            - Building ID.
        required: false
        type: int
    building:
        description:
            - Building name.
        required: false
        type: str
    storage_room:
        description:
            - Storage room name.
        required: false
        type: str
    storage_room_id:
        description:
            - Storage room ID.
        required: false
        type: int
    notes:
        description:
            - Device notes.
        required: false
        type: str
    objectcategory_id:
        description:
            - Object category ID.
        required: false
        type: int
    objectcategory:
        description:
            - Object category name.
        required: false
        type: str
    dont_inherit:
        description:
            - Do not inherit host multi-tenancy permissions.
        required: false
        type: str
        choices:
            - yes
            - no
    virtualsubtype_id:
        description:
            - Virtual subtype ID.
        required: false
        type: int
    virtualsubtype:
        description:
            - Virtual subtype name.
        required: false
        type: str
    datacenter:
        description:
            - Data center name.
        required: false
        type: str
    ram_size:
        description:
            - RAM size.
        required: false
        type: str
    ram_size_type_id:
        description:
            - RAM unit ID.
        required: false
        type: int
    ram_size_type:
        description:
            - RAM unit name.
        required: false
        type: str
    total_cpus:
        description:
            - Total CPUs.
        required: false
        type: int
    core_per_cpu:
        description:
            - Cores per CPU.
        required: false
        type: int
    threads_per_core:
        description:
            - Threads per core.
        required: false
        type: int
    cpu_speed:
        description:
            - CPU speed value.
        required: false
        type: str
    hz_id:
        description:
            - CPU speed unit ID.
        required: false
        type: int
    hz:
        description:
            - CPU speed unit name.
        required: false
        type: str
    hard_disk_count:
        description:
            - Total number of hard disks.
        required: false
        type: int
    hard_disk_size:
        description:
            - Hard disk size.
        required: false
        type: str
    hard_disk_size_type_id:
        description:
            - Hard disk size unit ID.
        required: false
        type: int
    hard_disk_size_type:
        description:
            - Hard disk size unit name.
        required: false
        type: str
    hw_sw_raid_id:
        description:
            - RAID implementation ID.
        required: false
        type: int
    hw_sw_raid:
        description:
            - RAID implementation name.
        required: false
        type: str
    raid_type_id:
        description:
            - RAID type ID.
        required: false
        type: int
    raid_type:
        description:
            - RAID type name.
        required: false
        type: str
    devices_in_clusters_ids:
        description:
            - CSV list of device IDs in the cluster.
        required: false
        type: str
    nonauthoritativealiases:
        description:
            - CSV non-authoritative aliases to add.
        required: false
        type: str
    nonauthoritativealiases_remove:
        description:
            - CSV non-authoritative aliases to remove.
        required: false
        type: str
    aliases:
        description:
            - CSV aliases to add.
        required: false
        type: str
    aliases_remove:
        description:
            - CSV aliases to remove.
        required: false
        type: str
    tags:
        description:
            - CSV tags to add or replace depending on Device42 semantics.
        required: false
        type: str
    tags_remove:
        description:
            - CSV tags to remove.
        required: false
        type: str
    bios_version:
        description:
            - BIOS version (POST endpoint).
        required: false
        type: str
    bios_release_date:
        description:
            - BIOS release date (POST endpoint).
        required: false
        type: str
    bios_revision:
        description:
            - BIOS revision (POST endpoint).
        required: false
        type: str
    bios_fw_revision:
        description:
            - BIOS firmware revision (POST endpoint).
        required: false
        type: str
    bios_vendor:
        description:
            - BIOS vendor (POST endpoint).
        required: false
        type: str
    custom_field_key:
        description:
            - Custom field key for C(present_endpoint=custom_fields).
        required: false
        type: str
    custom_field_type:
        description:
            - Custom field type.
        required: false
        type: str
    custom_field_value:
        description:
            - Custom field value.
        required: false
        type: str
"""

EXAMPLES = r"""
- name: Create a device with POST endpoint
    xbh03.device42.d42_api_devices:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: post
        name: db-080-westport
        device_type: physical
        in_service: yes

- name: Update a device by ID with PUT endpoint
    xbh03.device42.d42_api_devices:
        host: device42.example.internal
        userid: admin
        password: secret123
        state: present
        present_endpoint: put
        device_id: 46
        notes: Managed by Ansible

- name: Delete a device by ID
    xbh03.device42.d42_api_devices:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: absent
        device_id: 46
        delete_vms: no

- name: Set a device custom field
    xbh03.device42.d42_api_devices:
        host: device42.example.internal
        client_key: abc123
        client_secret_key: secret123
        state: present
        present_endpoint: custom_fields
        name: db-080-westport
        custom_field_key: ephimeral
        custom_field_value: "true"
"""

RETURN = r"""
api_device:
    description: Current or resulting device data when available.
    type: dict
    returned: success
response:
    description: Raw response from Device42 for create, update, or delete operations.
    type: dict
    returned: when changed
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.xbh03.device42.plugins.module_utils.devices.d42_devices import (
    d42_devices,
)


POST_ONLY_PARAMS = {
    "serial_no",
    "building",
    "bios_version",
    "bios_release_date",
    "bios_revision",
    "bios_fw_revision",
    "bios_vendor",
}


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


def _find_device(helper, device_id=None, name=None, serial_no=None, uuid=None):
    if device_id is not None:
        payload = helper.d42_get_devices(device_id=device_id, limit=1, offset=0)
        for device in _extract_devices_list(payload):
            current_id = device.get("device_id")
            try:
                current_id = int(current_id)
            except (TypeError, ValueError):
                current_id = None
            if current_id == int(device_id):
                return helper.d42_get_device_by_id(device_id=current_id)
        return None

    if name is not None:
        payload = helper.d42_get_devices(name=name, limit=100, offset=0)
        for device in _extract_devices_list(payload):
            if device.get("name") == name:
                current_id = device.get("device_id")
                if current_id is not None:
                    return helper.d42_get_device_by_id(device_id=current_id)

    if serial_no is not None:
        payload = helper.d42_get_devices(serial_no=serial_no, limit=100, offset=0)
        for device in _extract_devices_list(payload):
            if device.get("serial_no") == serial_no:
                current_id = device.get("device_id")
                if current_id is not None:
                    return helper.d42_get_device_by_id(device_id=current_id)

    if uuid is not None:
        payload = helper.d42_get_devices(uuid=uuid, limit=100, offset=0)
        for device in _extract_devices_list(payload):
            if device.get("uuid") == uuid:
                current_id = device.get("device_id")
                if current_id is not None:
                    return helper.d42_get_device_by_id(device_id=current_id)

    return None


def _resolve_device_id(candidate, fallback=None):
    if isinstance(candidate, dict):
        for key in ("device_id", "id"):
            if candidate.get(key) is not None:
                try:
                    return int(candidate.get(key))
                except (TypeError, ValueError):
                    pass

    if fallback is not None:
        try:
            return int(fallback)
        except (TypeError, ValueError):
            return None

    return None


def _extract_device_id_from_response(response):
    if not isinstance(response, dict):
        return None

    msg = response.get("msg")
    if isinstance(msg, list) and len(msg) > 1:
        try:
            return int(msg[1])
        except (TypeError, ValueError):
            return None

    for key in ("device_id", "id"):
        if response.get(key) is not None:
            try:
                return int(response.get(key))
            except (TypeError, ValueError):
                return None

    return None


def _build_post_payload(params):
    keys = [
        "device_id",
        "serial_no",
        "name",
        "asset_no",
        "uuid",
        "virtual_host",
        "in_service",
        "device_type_id",
        "device_type",
        "physicalsubtype_id",
        "physicalsubtype",
        "network_device",
        "blade_chassis",
        "manufacturer",
        "hardware_id",
        "hardware",
        "new_hardware",
        "virtual_host_device_id",
        "virtual_host_device",
        "host_chassis_device_id",
        "host_chassis_device",
        "bladeno",
        "chassisslot_id",
        "service_level_id",
        "service_level",
        "customer_id",
        "customer",
        "customers",
        "customers_remove",
        "additional_location",
        "building_id",
        "building",
        "storage_room",
        "storage_room_id",
        "notes",
        "objectcategory_id",
        "objectcategory",
        "dont_inherit",
        "virtualsubtype_id",
        "virtualsubtype",
        "datacenter",
        "ram_size",
        "ram_size_type_id",
        "ram_size_type",
        "total_cpus",
        "core_per_cpu",
        "threads_per_core",
        "cpu_speed",
        "hz_id",
        "hz",
        "hard_disk_count",
        "hard_disk_size",
        "hard_disk_size_type_id",
        "hard_disk_size_type",
        "hw_sw_raid_id",
        "hw_sw_raid",
        "raid_type_id",
        "raid_type",
        "devices_in_clusters_ids",
        "nonauthoritativealiases",
        "nonauthoritativealiases_remove",
        "aliases",
        "aliases_remove",
        "tags",
        "tags_remove",
        "bios_version",
        "bios_release_date",
        "bios_revision",
        "bios_fw_revision",
        "bios_vendor",
    ]

    payload = {}
    for key in keys:
        value = params.get(key)
        if value is not None:
            payload[key] = value
    return payload


def _build_put_payload(params):
    keys = [
        "name",
        "asset_no",
        "uuid",
        "virtual_host",
        "in_service",
        "device_type_id",
        "device_type",
        "physicalsubtype_id",
        "physicalsubtype",
        "network_device",
        "blade_chassis",
        "manufacturer",
        "hardware_id",
        "hardware",
        "new_hardware",
        "virtual_host_device_id",
        "virtual_host_device",
        "host_chassis_device_id",
        "host_chassis_device",
        "bladeno",
        "chassisslot_id",
        "service_level_id",
        "service_level",
        "customer_id",
        "customer",
        "customers",
        "customers_remove",
        "additional_location",
        "building_id",
        "storage_room",
        "storage_room_id",
        "notes",
        "objectcategory_id",
        "objectcategory",
        "dont_inherit",
        "virtualsubtype_id",
        "virtualsubtype",
        "datacenter",
        "ram_size",
        "ram_size_type_id",
        "ram_size_type",
        "total_cpus",
        "core_per_cpu",
        "threads_per_core",
        "cpu_speed",
        "hz_id",
        "hz",
        "hard_disk_count",
        "hard_disk_size",
        "hard_disk_size_type_id",
        "hard_disk_size_type",
        "hw_sw_raid_id",
        "hw_sw_raid",
        "raid_type_id",
        "raid_type",
        "devices_in_clusters_ids",
        "nonauthoritativealiases",
        "nonauthoritativealiases_remove",
        "aliases",
        "aliases_remove",
        "tags",
        "tags_remove",
    ]

    payload = {}
    for key in keys:
        value = params.get(key)
        if value is not None:
            payload[key] = value
    return payload


def _existing_value(existing, payload_key):
    alias_map = {
        "type_id": ["type_id", "device_type_id"],
        "type": ["type", "device_type"],
        "chassisslot_id": ["chassisslot_id", "chassis_slot_id"],
        "host_chassis_device_id": ["host_chassis_device_id", "device_host_chassis_id"],
        "virtual_host_device_id": ["virtual_host_device_id", "device_virtual_host_id"],
        "additional_location": ["additional_location", "additional_location_info"],
        "datacenter": ["datacenter", "data_center"],
        "ram_size": ["ram_size", "ram"],
    }

    for key in alias_map.get(payload_key, [payload_key]):
        if key in existing:
            return existing.get(key)
    return None


def _equal_value(desired, current, key):
    if desired is None:
        return True

    if isinstance(desired, str) and desired.lower() == "d42null":
        return current in (None, "", "null")

    list_like_keys = {
        "customers",
        "customers_remove",
        "devices_in_clusters_ids",
        "nonauthoritativealiases",
        "nonauthoritativealiases_remove",
        "aliases",
        "aliases_remove",
        "tags",
        "tags_remove",
    }
    if key in list_like_keys:
        desired_set = set(_normalize_multi_value(desired))
        current_set = set(_normalize_multi_value(current))
        return desired_set == current_set

    int_like_keys = {
        "device_id",
        "type_id",
        "physicalsubtype_id",
        "hardware_id",
        "virtual_host_device_id",
        "host_chassis_device_id",
        "bladeno",
        "chassisslot_id",
        "service_level_id",
        "customer_id",
        "building_id",
        "storage_room_id",
        "objectcategory_id",
        "virtualsubtype_id",
        "ram_size_type_id",
        "total_cpus",
        "core_per_cpu",
        "threads_per_core",
        "hz_id",
        "hard_disk_count",
        "hard_disk_size_type_id",
        "hw_sw_raid_id",
        "raid_type_id",
    }
    if key in int_like_keys:
        try:
            return int(current) == int(desired)
        except (TypeError, ValueError):
            return False

    return str(current) == str(desired)


def _needs_update(existing, payload, force_update=False):
    if force_update:
        return True

    if existing is None:
        return True

    remove_or_replace_keys = {
        "customers_remove",
        "nonauthoritativealiases_remove",
        "aliases_remove",
        "tags_remove",
        "new_hardware",
    }

    for key, desired in payload.items():
        if key in remove_or_replace_keys:
            return True

        current = _existing_value(existing, key)
        if not _equal_value(desired=desired, current=current, key=key):
            return True

    return False

def _build_custom_field_payload(params):
    payload = {
        "key": params.get("custom_field_key"),
        "device_id": params.get("device_id"),
        "name": params.get("name"),
        "type": params.get("custom_field_type"),
        "mandatory": params.get("custom_field_mandatory"),
        "filterable": params.get("custom_field_filterable"),
        "log_for_api": params.get("custom_field_log_for_api"),
        "related_field_name": params.get("custom_field_related_field_name"),
        "add_to_picklist": params.get("custom_field_add_to_picklist"),
        "remove_from_picklist": params.get("custom_field_remove_from_picklist"),
        "delete_in_use": params.get("custom_field_delete_in_use"),
        "related_field_value_by_id": params.get("custom_field_related_field_value_by_id"),
        "value": params.get("custom_field_value"),
        "clear_value": params.get("custom_field_clear_value"),
        "notes": params.get("custom_field_notes"),
        "clear_notes": params.get("custom_field_clear_notes"),
        "bulk_fields": params.get("custom_field_bulk_fields"),
        "multi_select": params.get("custom_field_multi_select"),
    }

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
        present_endpoint=dict(type="str", required=False, default="post", choices=["post", "put", "custom_fields"]),
        force_update=dict(type="bool", required=False, default=False),
        delete_vms=dict(type="str", required=False, choices=["yes", "no"]),
        device_id=dict(type="int", required=False),
        serial_no=dict(type="str", required=False),
        name=dict(type="str", required=False),
        asset_no=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        virtual_host=dict(type="str", required=False, choices=["yes", "no"]),
        in_service=dict(type="str", required=False, choices=["yes", "no"]),
        device_type_id=dict(type="int", required=False),
        device_type=dict(type="str", required=False, choices=["unknown", "physical", "virtual", "cluster"]),
        physicalsubtype_id=dict(type="int", required=False),
        physicalsubtype=dict(type="str", required=False),
        network_device=dict(type="str", required=False, choices=["yes", "no"]),
        blade_chassis=dict(type="str", required=False, choices=["yes", "no"]),
        manufacturer=dict(type="str", required=False),
        hardware_id=dict(type="int", required=False),
        hardware=dict(type="str", required=False),
        new_hardware=dict(type="str", required=False),
        virtual_host_device_id=dict(type="int", required=False),
        virtual_host_device=dict(type="str", required=False),
        host_chassis_device_id=dict(type="int", required=False),
        host_chassis_device=dict(type="str", required=False),
        bladeno=dict(type="int", required=False),
        chassisslot_id=dict(type="int", required=False),
        service_level_id=dict(type="int", required=False),
        service_level=dict(type="str", required=False),
        customer_id=dict(type="int", required=False),
        customer=dict(type="str", required=False),
        customers=dict(type="str", required=False),
        customers_remove=dict(type="str", required=False),
        additional_location=dict(type="str", required=False),
        building_id=dict(type="int", required=False),
        building=dict(type="str", required=False),
        storage_room=dict(type="str", required=False),
        storage_room_id=dict(type="int", required=False),
        notes=dict(type="str", required=False),
        objectcategory_id=dict(type="int", required=False),
        objectcategory=dict(type="str", required=False),
        dont_inherit=dict(type="str", required=False, choices=["yes", "no"]),
        virtualsubtype_id=dict(type="int", required=False),
        virtualsubtype=dict(type="str", required=False),
        datacenter=dict(type="str", required=False),
        ram_size=dict(type="str", required=False),
        ram_size_type_id=dict(type="int", required=False),
        ram_size_type=dict(type="str", required=False),
        total_cpus=dict(type="int", required=False),
        core_per_cpu=dict(type="int", required=False),
        threads_per_core=dict(type="int", required=False),
        cpu_speed=dict(type="str", required=False),
        hz_id=dict(type="int", required=False),
        hz=dict(type="str", required=False),
        hard_disk_count=dict(type="int", required=False),
        hard_disk_size=dict(type="str", required=False),
        hard_disk_size_type_id=dict(type="int", required=False),
        hard_disk_size_type=dict(type="str", required=False),
        hw_sw_raid_id=dict(type="int", required=False),
        hw_sw_raid=dict(type="str", required=False),
        raid_type_id=dict(type="int", required=False),
        raid_type=dict(type="str", required=False),
        devices_in_clusters_ids=dict(type="str", required=False),
        nonauthoritativealiases=dict(type="str", required=False),
        nonauthoritativealiases_remove=dict(type="str", required=False),
        aliases=dict(type="str", required=False),
        aliases_remove=dict(type="str", required=False),
        tags=dict(type="str", required=False),
        tags_remove=dict(type="str", required=False),
        bios_version=dict(type="str", required=False),
        bios_release_date=dict(type="str", required=False),
        bios_revision=dict(type="str", required=False),
        bios_fw_revision=dict(type="str", required=False),
        bios_vendor=dict(type="str", required=False),
        custom_field_key=dict(type="str", required=False),
        custom_field_type=dict(type="str", required=False),
        custom_field_mandatory=dict(type="str", required=False, choices=["yes", "no"]),
        custom_field_filterable=dict(type="str", required=False, choices=["yes", "no"]),
        custom_field_log_for_api=dict(type="str", required=False, choices=["yes", "no"]),
        custom_field_related_field_name=dict(type="str", required=False),
        custom_field_add_to_picklist=dict(type="str", required=False),
        custom_field_remove_from_picklist=dict(type="str", required=False),
        custom_field_delete_in_use=dict(type="str", required=False, choices=["yes", "no"]),
        custom_field_related_field_value_by_id=dict(type="str", required=False, choices=["yes", "no"]),
        custom_field_value=dict(type="str", required=False),
        custom_field_clear_value=dict(type="str", required=False, choices=["yes", "no"]),
        custom_field_notes=dict(type="str", required=False),
        custom_field_clear_notes=dict(type="str", required=False, choices=["yes", "no"]),
        custom_field_bulk_fields=dict(type="str", required=False),
        custom_field_multi_select=dict(type="str", required=False, choices=["yes", "no"]),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(changed=False)

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

    state = module.params["state"]
    present_endpoint = module.params["present_endpoint"]
    device_id = module.params["device_id"]
    name = module.params["name"]
    serial_no = module.params["serial_no"]
    uuid = module.params["uuid"]

    existing = _find_device(
        helper=helper,
        device_id=device_id,
        name=name,
        serial_no=serial_no,
        uuid=uuid,
    )

    if state == "absent":
        if device_id is None and name is None and serial_no is None and uuid is None:
            module.fail_json(msg="At least one identifier (device_id, name, serial_no, uuid) is required when state=absent.")

        if not existing and device_id is None:
            result["msg"] = "Device already absent"
            module.exit_json(**result)

        resolved_device_id = _resolve_device_id(existing, fallback=device_id)
        if resolved_device_id is None:
            result["msg"] = "Device already absent"
            module.exit_json(**result)

        result["api_device"] = existing
        result["changed"] = True

        if module.check_mode:
            result["msg"] = "Device would be deleted"
            module.exit_json(**result)

        response = helper.d42_delete_device(
            device_id=resolved_device_id,
            delete_vms=module.params["delete_vms"],
        )
        result["response"] = response
        module.exit_json(**result)

    if present_endpoint == "put":
        used_post_only = [param for param in POST_ONLY_PARAMS if module.params.get(param) is not None]
        if used_post_only:
            module.fail_json(
                msg=(
                    "present_endpoint=put does not support these parameters: "
                    + ", ".join(sorted(used_post_only))
                )
            )
    
    if present_endpoint == "custom_fields":
        cf_payload = _build_custom_field_payload(module.params)
        if not cf_payload.get("key"):
            module.fail_json(msg="custom_field_key is required when present_endpoint=custom_fields.")
        if cf_payload.get("device_id") is None and cf_payload.get("name") is None:
            module.fail_json(msg="device_id or name is required when present_endpoint=custom_fields.")

        result["changed"] = True
        if module.check_mode:
            result["msg"] = "Device custom fields would be updated"
            if existing is not None:
                result["api_device"] = existing
            module.exit_json(**result)

        response = helper.d42_put_custom_field_device(**cf_payload)
        result["response"] = response

        resolved_device_id = _resolve_device_id(existing, fallback=module.params["device_id"])
        if resolved_device_id is None:
            resolved_device_id = _extract_device_id_from_response(response)
        if resolved_device_id is not None:
            result["api_device"] = helper.d42_get_device_by_id(device_id=resolved_device_id, include_cols="custom_fields")
        else:
            result["api_device"] = existing
        module.exit_json(**result)

    post_payload = _build_post_payload(module.params)
    put_payload = _build_put_payload(module.params)

    if present_endpoint == "post" and not post_payload:
        module.fail_json(msg="At least one POST parameter is required when state=present and present_endpoint=post.")
    if present_endpoint == "put" and not put_payload:
        module.fail_json(msg="At least one PUT parameter is required when state=present and present_endpoint=put.")

    if present_endpoint == "post" and existing is None and name is None:
        module.fail_json(
            msg=(
                "name is required to create a new device with present_endpoint=post "
                "when no existing device is found by device_id, serial_no, or uuid."
            )
        )

    resolved_device_id = _resolve_device_id(existing, fallback=device_id)
    if present_endpoint == "put" and resolved_device_id is None:
        module.fail_json(msg="device_id (or a resolvable identifier) is required when present_endpoint=put.")

    needs_change = _needs_update(
        existing=existing,
        payload=post_payload if present_endpoint == "post" else put_payload,
        force_update=module.params["force_update"],
    )

    if not needs_change:
        result["api_device"] = existing
        result["msg"] = "Device already in desired state"
        module.exit_json(**result)

    result["changed"] = True
    if module.check_mode:
        result["msg"] = "Device would be created/updated"
        if existing is not None:
            result["api_device"] = existing
        module.exit_json(**result)

    if present_endpoint == "post":
        response = helper.d42_post_devices(**post_payload)
    else:
        response = helper.d42_put_device_by_id(device_id=resolved_device_id, **put_payload)

    result["response"] = response

    refetched_id = _extract_device_id_from_response(response)
    if refetched_id is None:
        refetched_id = resolved_device_id
    if refetched_id is None and existing is not None:
        refetched_id = _resolve_device_id(existing)

    if refetched_id is not None:
        result["api_device"] = helper.d42_get_device_by_id(device_id=refetched_id)
    else:
        result["api_device"] = _find_device(
            helper=helper,
            device_id=module.params["device_id"],
            name=module.params["name"],
            serial_no=module.params["serial_no"],
            uuid=module.params["uuid"],
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
