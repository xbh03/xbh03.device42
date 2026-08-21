from urllib.parse import urlencode

from ...admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_ipam_ips:
	def __init__(
		self,
		host: str,
		module: object,
		result: object,
		sslverify,
		client_key: str = None,
		client_secret_key: str = None,
		userid: str = None,
		password: str = None,
		proto: str = "https",
		port: int = 443,
		debug: bool = False,
		auth_client: d42_token_authentication = None,
	):
		self.debug = debug
		self.module = module
		self.result = result

		# Reuse an already configured auth helper when provided.
		self.auth = auth_client or d42_token_authentication(
			host=host,
			module=module,
			result=result,
			sslverify=sslverify,
			client_key=client_key,
			client_secret_key=client_secret_key,
			userid=userid,
			password=password,
			proto=proto,
			port=port,
			debug=debug,
		)

	def d42_get_ips(
		self,
		offset: str = None,
		limit: str = None,
		subnet_id: str = None,
		subnet: str = None,
		device: str = None,
		mac: str = None,
		available: str = None,
		ip_type: str = None,
		last_updated_lt: str = None,
		last_updated_gt: str = None,
		ip: str = None,
		first_added_lt: str = None,
		first_added_gt: str = None,
		ip_id: str = None,
		label: str = None,
		tags: str = None,
		tags_and: str = None,
		custom_fields_and: str = None,
		custom_fields_or: str = None,
		total_count: str = None,
		is_shared: str = None,
	) -> dict:
		"""
		GET /api/2.0/ips/
		Retrieve all IPs (API 2.0).
		"""
		params = {}

		if offset is not None:
			params["offset"] = offset
		if limit is not None:
			params["limit"] = limit
		if subnet_id is not None:
			params["subnet_id"] = subnet_id
		if subnet is not None:
			params["subnet"] = subnet
		if device is not None:
			params["device"] = device
		if mac is not None:
			params["mac"] = mac
		if available is not None:
			params["available"] = available
		if ip_type is not None:
			params["type"] = ip_type
		if last_updated_lt is not None:
			params["last_updated_lt"] = last_updated_lt
		if last_updated_gt is not None:
			params["last_updated_gt"] = last_updated_gt
		if ip is not None:
			params["ip"] = ip
		if first_added_lt is not None:
			params["first_added_lt"] = first_added_lt
		if first_added_gt is not None:
			params["first_added_gt"] = first_added_gt
		if ip_id is not None:
			params["ip_id"] = ip_id
		if label is not None:
			params["label"] = label
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if custom_fields_and is not None:
			params["custom_fields_and"] = custom_fields_and
		if custom_fields_or is not None:
			params["custom_fields_or"] = custom_fields_or
		if total_count is not None:
			params["total_count"] = total_count
		if is_shared is not None:
			params["is_shared"] = is_shared

		endpoint = "/api/2.0/ips/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def _build_ip_payload(
		self,
		ipaddress: str,
		label: str = None,
		subnet: str = None,
		macaddress: str = None,
		ip_type: str = None,
		notes: str = None,
		vrf_group_id: int = None,
		vrf_group: str = None,
		available: str = None,
		clear_all: str = None,
		tags: str = None,
		devices: str = None,
		device_ids: str = None,
		remove_devices: str = None,
		remove_device_ids: str = None,
		locked: str = None,
	) -> dict:
		data = {"ipaddress": ipaddress}

		if label is not None:
			data["label"] = label
		if subnet is not None:
			data["subnet"] = subnet
		if macaddress is not None:
			data["macaddress"] = macaddress
		if ip_type is not None:
			data["type"] = ip_type
		if notes is not None:
			data["notes"] = notes
		if vrf_group_id is not None:
			data["vrf_group_id"] = int(vrf_group_id)
		if vrf_group is not None:
			data["vrf_group"] = vrf_group
		if available is not None:
			data["available"] = available
		if clear_all is not None:
			data["clear_all"] = clear_all
		if tags is not None:
			data["tags"] = tags
		if devices is not None:
			data["devices"] = devices
		if device_ids is not None:
			data["device_ids"] = device_ids
		if remove_devices is not None:
			data["remove_devices"] = remove_devices
		if remove_device_ids is not None:
			data["remove_device_ids"] = remove_device_ids
		if locked is not None:
			data["locked"] = locked

		return data

	def d42_post_ips(
		self,
		ipaddress: str,
		label: str = None,
		subnet: str = None,
		macaddress: str = None,
		ip_type: str = None,
		notes: str = None,
		vrf_group_id: int = None,
		vrf_group: str = None,
		available: str = None,
		clear_all: str = None,
		tags: str = None,
		devices: str = None,
		device_ids: str = None,
		remove_devices: str = None,
		remove_device_ids: str = None,
		locked: str = None,
	) -> dict:
		"""
		POST /api/2.0/ips/
		Create or update IP address (API 2.0).
		"""
		data = self._build_ip_payload(
			ipaddress=ipaddress,
			label=label,
			subnet=subnet,
			macaddress=macaddress,
			ip_type=ip_type,
			notes=notes,
			vrf_group_id=vrf_group_id,
			vrf_group=vrf_group,
			available=available,
			clear_all=clear_all,
			tags=tags,
			devices=devices,
			device_ids=device_ids,
			remove_devices=remove_devices,
			remove_device_ids=remove_device_ids,
			locked=locked,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/2.0/ips/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_ip_by_id(self, id: int) -> dict:
		"""
		DELETE /api/1.0/ips/{id}/
		Delete IP address by ID.
		"""
		resolved_id = int(id)
		return self.auth.request(f"/api/1.0/ips/{resolved_id}/", method="DELETE")
