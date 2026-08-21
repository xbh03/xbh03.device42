# Device42 Ansible Collection

[![Ansible Galaxy](https://img.shields.io/badge/Ansible%20Galaxy-xbh03.device42-EE0000?logo=ansible&logoColor=white)](https://galaxy.ansible.com/ui/repo/published/xbh03/device42/)
[![Ansible](https://img.shields.io/badge/Ansible-%3E%3D2.13-EE0000?logo=ansible&logoColor=white)](https://docs.ansible.com/ansible/latest/)
[![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue)](https://www.gnu.org/licenses/gpl-3.0.html)

An Ansible collection for managing and querying [Device42](https://www.device42.com/) through its REST API.

The collection provides modules for devices, assets, IPAM, racks, rooms, software, services, users and groups, and other Device42 resources.

> This project is community maintained and is not affiliated with or endorsed by Device42.

## Requirements

- Ansible 2.13 or later
- A Device42 instance reachable from the Ansible control node
- Device42 API credentials: an API client key and secret, or a username and password where supported

## Installation

Install the collection from Ansible Galaxy:

```sh
ansible-galaxy collection install xbh03.device42
```

To install it from a local checkout during development:

```sh
ansible-galaxy collection install .
```

## Configuration

Store credentials in Ansible Vault rather than directly in a playbook:

```yaml
# group_vars/all/device42.yml
d42_host: device42.example.com
d42_client_key: !vault |
	$ANSIBLE_VAULT;1.1;AES256
	...
d42_client_secret: !vault |
	$ANSIBLE_VAULT;1.1;AES256
d42_sslverify: true
```

The common connection options are:

| Option | Description | Default |
| --- | --- | --- |
| `host` | Device42 hostname or IP address | Required |
| `client_key` | Device42 API client key | Required by most modules |
| `client_secret_key` | Device42 API client secret | Required by most modules |
| `proto` | Connection protocol (`http` or `https`) | `https` |
| `port` | Device42 API port | `443` |
| `sslverify` | Validate the TLS certificate | `true` |

Use `sslverify: false` only for a development instance with a self-signed certificate.

## Examples

### Query devices

```yaml
---
- name: Query Device42
	hosts: localhost
	gather_facts: false

	vars_files:
		- group_vars/all/device42.yml

	tasks:
		- name: Retrieve physical devices
			xbh03.device42.devices.d42_api_devices_info:
				host: "{{ d42_host }}"
				client_key: "{{ d42_client_key }}"
				client_secret_key: "{{ d42_client_secret }}"
				sslverify: "{{ d42_sslverify }}"
				device_type: physical
			register: devices

		- name: Display retrieved devices
			ansible.builtin.debug:
				var: devices
```

### Create or update a device

```yaml
- name: Ensure a device is present
	xbh03.device42.devices.d42_api_devices:
		host: "{{ d42_host }}"
		client_key: "{{ d42_client_key }}"
		client_secret_key: "{{ d42_client_secret }}"
		sslverify: "{{ d42_sslverify }}"
		state: present
		name: web-01
		serial_no: ABC123456
		device_type: physical
		in_service: 'yes'
```

Use the module documentation for the complete list of supported arguments and resource-specific examples:

```sh
ansible-doc xbh03.device42.devices.d42_api_devices
ansible-doc xbh03.device42.devices.d42_api_devices_info
```

## Available Modules

Modules are grouped by Device42 resource:

- Admin users, groups, API clients, and client keys
- Application components and application groups
- Assets, devices, hardware models, operating systems, and lifecycle data
- Buildings, rooms, racks, cables, certificates, and custom fields
- IPAM: DNS, IP addresses, subnets, switches, switch ports, and VLANs
- Services, service levels, software, tags, vendors, backup schedules, and telco circuits

Run the following command to discover all installed modules:

```sh
ansible-doc -l | grep '^xbh03.device42'
```

## Testing

The smoke playbook queries the available information modules against a Device42 instance. Configure credentials through environment variables, then run it from the repository root:

```sh
export D42_HOST=device42.example.com
export D42_CLIENT_KEY=your-client-key
export D42_CLIENT_SECRET=your-client-secret
ansible-playbook tests/smoke_get_all_info.yml
```

Alternatively, use Basic Authentication for modules that support it:

```sh
export D42_HOST=device42.example.com
export D42_USERID=your-username
export D42_PASSWORD=your-password
ansible-playbook tests/smoke_get_all_info.yml
```

Optional connection variables are `D42_PROTO`, `D42_PORT`, and `D42_SSLVERIFY`.

## Contributing

Open an issue or pull request in the [GitHub repository](https://github.com/xbh03/xbh03.device42). Keep changes focused, add or update module documentation, and validate against a non-production Device42 instance when practical.

## License

This collection is licensed under GPL-3.0-or-later. See the collection metadata in `galaxy.yml`.