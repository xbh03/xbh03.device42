# Changelog

## 0.2.4

- Published the collection under the `xbh03.device42` namespace.

## 0.2.3

- Implemented custom field value updates for existing devices.
- Removed the device bulk-extraction plugin because of Ansible performance limitations. Use Python directly in ETL solutions instead.

## 0.2.2

- Fixed general issues in the bulk device-extraction plugin used to generate Ansible inventory.

## 0.2.1

- Implemented a bulk device-extraction plugin for generating Ansible inventory.

## 0.2.0

Implemented new APIs.

### Admin Users-Groups

- API Admin Users-Groups - get /api/1.0/admingroups/
- API Admin Users-Groups - post /api/1.0/admingroups/
- API Admin Users-Groups - delete /api/1.0/admingroups/{id}/
- API Admin Users-Groups - get /api/1.0/adminusers/
- API Admin Users-Groups - post /api/1.0/adminusers/
- API Admin Users-Groups - delete /api/1.0/adminusers/{id}/
- API Admin Users-Groups - get /api/1.0/adminusers/{id}/

### Application Components

- Application Components - get /api/1.0/appcomps/
- Application Components - post /api/1.0/appcomps/
- Application Components - delete /api/1.0/appcomps/{appcomp_id}/
- Application Components - get /api/1.0/appcomps/{appcomp_id}/
- Application Components - put /api/1.0/custom_fields/appcomp/

- Application Component Template - get /api/2.0/appcomp_templates/
- Application Component Template - get /api/2.0/appcomp_templates/
- Application Component Template - delete /api/2.0/appcomp_templates/{id}/

### Asset-Device Life Cycle

- Asset-Device Life Cycle - get /api/1.0/lifecycle_event/
- Asset-Device Life Cycle - put /api/1.0/lifecycle_event/
- Asset-Device Life Cycle - delete /api/1.0/lifecycle_event/{id}/
- Asset-Device Life Cycle - get /api/1.0/lifecycle_event/{id}/

### Devices

- Devices - get /api/2.0/device/mountpoints/
- Devices - post /api/2.0/devices/
- Devices - delete /api/2.0/devices/{id}/
- Devices - get /api/2.0/devices/{id}/
- Devices - put /api/2.0/devices/{id}/

### Assets

- Assets - post /api/1.0/assets/
- Assets - put /api/1.0/assets/
- Assets - delete /api/1.0/assets/{id}/
- Assets - get /api/1.0/assets/{id}/
- Assets - put /api/1.0/assets/{id}/
- Assets - put /api/1.0/custom_fields/asset/

### Backup Schedules

- Backup Schedules - get :4343/api/1.0/backup_schedules/
- Backup Schedules - post :4343/api/1.0/backup_schedules/
- Backup Schedules - delete :4343/api/1.0/backup_schedules/{id}/ 

### Buildings

- Buildings - get /api/1.0/buildings/
- Buildings - post /api/1.0/buildings/
- Buildings - delete /api/1.0/buildings/{id}/
- Buildings - get /api/1.0/buildings/{id}/
- Buildings - put /api/1.0/custom_fields/building/

### Cables

- Cables - get /api/1.0/cables/
- Cables - post /api/1.0/cables/
- Cables - delete /api/1.0/cables/{id}/

### Certificates

- Certificates - get /api/1.0/certificates/
- Certificates - post /api/1.0/certificates/
- Certificates - delete /api/1.0/certificates/{id}/
- Certificates - put /api/1.0/custom_fields/certificate/

### Custom Fields

- Custom Fields - delete /api/2.0/custom_fields/
- Custom Fields - get /api/2.0/custom_fields/
- Custom Fields - put /api/2.0/custom_fields/

### Operating Systems

- Operating Systems - post /api/1.0/operatingsystems/
- Operating Systems - delete /api/1.0/operatingsystems/{id}/
- Operating Systems - get /api/1.0/operatingsystems/{id}/
- EOLEOS - get /api/1.0/os_eoleos/
- EOLEOS - post /api/1.0/os_eoleos/
- EOLEOS - delete /api/1.0/os_eoleos/{id}/

### Rooms

- Rooms - delete /api/1.0/rooms/{id}/
- Rooms - post /api/1.0/rooms/
- Rooms - get /api/1.0/rooms/
- Rooms - get /api/1.0/rooms/{id}/
- Rooms - put /api/1.0/rooms/{id}/

### Service Levels

- Service Levels - get /api/1.0/service_level/
- Service Levels - post /api/1.0/service_level/

### Hardware Models

- Hardware Models - get /api/2.0/hardwares/
- Hardware Models - post /api/2.0/hardwares/
- Hardware Models - delete /api/2.0/hardwares/{id}/
- Hardware Models - get /api/2.0/hardwares/{id}/

### IPAM

- IPs - delete /api/1.0/ips/{id}/
- IPs - post /api/2.0/ips/
- Subnets - post /api/1.0/subnets/
- Subnets - put /api/1.0/subnets/
- Subnets - delete /api/1.0/subnets/{subnet_id}/
- Subnets - get /api/1.0/subnets/{subnet_id}/
- Switches - post /api/1.0/switches/
- Switch Templates - get /api/1.0/switch_templates/
- Switch Ports - delete /api/1.0/switchports/{id}/
- Switch Ports - post /api/1.0/switchports/
- Switch Ports - get /api/1.0/switchports/
- VLANs - post /api/1.0/vlans/
- VLANs - put /api/1.0/vlans/
- VLANs - delete /api/1.0/vlans/{id}/
- VLANs - get /api/1.0/vlans/{id}/
- VLANs - put /api/1.0/vlans/{id}/
- DNS - delete /api/1.0/dns/records/{id}/
- DNS - post /api/1.0/dns/records/
- DNS - post /api/1.0/dns/zones/
- DNS - delete /api/1.0/dns/zones/{id}/

### Tags

- Tags - get /api/1.0/tags/

### Telco Circuits

- Telco Circuits - get /api/1.0/circuits/

## 0.1.2

Removed the Audit Logs implementation because of security and other specific requirements.

## 0.1.1

Fixed Audit Logs parameters:

- Removed timeout and offset
- Added action_time_gt, action_time_lt

## 0.1.0

Initial development phase.

This collection supports the following APIs:

### API Clients and Token

- API Client Keys - get /api/2.0/api_client_keys/
- API Clients - get /api/2.0/api_clients/
- API Clients - post /api/2.0/api_clients/
- API Clients - delete /api/2.0/api_clients/{client_id}
- API Clients - get /api/2.0/api_clients/{client_id}
- API Token Authentication - post /tauth/1.0/token/
- API Token Authentication - delete /tauth/1.0/token/{token_id}/

### Health Status

- Health Status - get :4343/healthstats/

### Audit Log

- Audit Log - get /api/1.0/auditlogs/
- Audit Log - delete /api/1.0/auditlogs/

### Devices

- Devices - get /api/2.0/devices/

### Assets

- Assets - get /api/1.0/assets/

### Operating Systems

- Operating Systems - get /api/1.0/operatingsystems/

### Vendors

- Vendors - get /api/1.0/vendors/

### Racks

- Racks - get /api/1.0/racks/

### IPAM

- IPs - get /api/2.0/ips/
- Subnets - get /api/1.0/subnets/
- VLANs - get /api/1.0/vlans/
- DNS Zones - get /api/1.0/dns/zones/
- DNS Records - get /api/1.0/dns/records/

### Services

- Services - get /api/2.0/services/

### Software

- Software - get /api/1.0/software/