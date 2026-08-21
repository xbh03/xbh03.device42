from urllib.parse import urlencode

from ...admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_ipam_switchports:
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

	def d42_get_switchports(
		self,
		switch_id: int = None,
		include_cols: str = None,
		switch2_id: int = None,
		last_updated_lt: str = None,
		last_updated_gt: str = None,
		first_added_lt: str = None,
		first_added_gt: str = None,
		tags: str = None,
		tags_and: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/1.0/switchports/
		Get all switch ports.
		"""
		params = {}

		if switch_id is not None:
			params["switch_id"] = int(switch_id)
		if include_cols is not None:
			params["include_cols"] = include_cols
		if switch2_id is not None:
			params["switch2_id"] = int(switch2_id)
		if last_updated_lt is not None:
			params["last_updated_lt"] = last_updated_lt
		if last_updated_gt is not None:
			params["last_updated_gt"] = last_updated_gt
		if first_added_lt is not None:
			params["first_added_lt"] = first_added_lt
		if first_added_gt is not None:
			params["first_added_gt"] = first_added_gt
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/1.0/switchports/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def _build_switchport_payload(
		self,
		port: str = None,
		port_id: int = None,
		hwaddress: str = None,
		new_port: str = None,
		switch: str = None,
		description: str = None,
		type: str = None,
		vlan_id: str = None,
		vlan: str = None,
		vlan_ids: str = None,
		vlans: str = None,
		clear_vlan_ids: str = None,
		clear_vlans: str = None,
		up: str = None,
		up_admin: str = None,
		count: str = None,
		remote_port_id: str = None,
		remote_device: str = None,
		remote_port: str = None,
		module: str = None,
		device2: str = None,
		device: str = None,
		label: str = None,
		tags: str = None,
		tags_remove: str = None,
		mtu: str = None,
		name: str = None,
		speed: str = None,
		remote_port_clear: str = None,
		parent_port: str = None,
		parent_port_device: str = None,
		slave_ports: str = None,
	) -> dict:
		data = {}

		if port is not None:
			data["port"] = port
		if port_id is not None:
			data["port_id"] = int(port_id)
		if hwaddress is not None:
			data["hwaddress"] = hwaddress
		if new_port is not None:
			data["new_port"] = new_port
		if switch is not None:
			data["switch"] = switch
		if description is not None:
			data["description"] = description
		if type is not None:
			data["type"] = type
		if vlan_id is not None:
			data["vlan_id"] = vlan_id
		if vlan is not None:
			data["vlan"] = vlan
		if vlan_ids is not None:
			data["vlan_ids"] = vlan_ids
		if vlans is not None:
			data["vlans"] = vlans
		if clear_vlan_ids is not None:
			data["clear_vlan_ids"] = clear_vlan_ids
		if clear_vlans is not None:
			data["clear_vlans"] = clear_vlans
		if up is not None:
			data["up"] = up
		if up_admin is not None:
			data["up_admin"] = up_admin
		if count is not None:
			data["count"] = count
		if remote_port_id is not None:
			data["remote_port_id"] = remote_port_id
		if remote_device is not None:
			data["remote_device"] = remote_device
		if remote_port is not None:
			data["remote_port"] = remote_port
		if module is not None:
			data["module"] = module
		if device2 is not None:
			data["device2"] = device2
		if device is not None:
			data["device"] = device
		if label is not None:
			data["label"] = label
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if mtu is not None:
			data["mtu"] = mtu
		if name is not None:
			data["name"] = name
		if speed is not None:
			data["speed"] = speed
		if remote_port_clear is not None:
			data["remote_port_clear"] = remote_port_clear
		if parent_port is not None:
			data["parent_port"] = parent_port
		if parent_port_device is not None:
			data["parent_port_device"] = parent_port_device
		if slave_ports is not None:
			data["slave_ports"] = slave_ports

		return data

	def d42_post_switchports(
		self,
		port: str = None,
		port_id: int = None,
		hwaddress: str = None,
		new_port: str = None,
		switch: str = None,
		description: str = None,
		type: str = None,
		vlan_id: str = None,
		vlan: str = None,
		vlan_ids: str = None,
		vlans: str = None,
		clear_vlan_ids: str = None,
		clear_vlans: str = None,
		up: str = None,
		up_admin: str = None,
		count: str = None,
		remote_port_id: str = None,
		remote_device: str = None,
		remote_port: str = None,
		module: str = None,
		device2: str = None,
		device: str = None,
		label: str = None,
		tags: str = None,
		tags_remove: str = None,
		mtu: str = None,
		name: str = None,
		speed: str = None,
		remote_port_clear: str = None,
		parent_port: str = None,
		parent_port_device: str = None,
		slave_ports: str = None,
	) -> dict:
		"""
		POST /api/1.0/switchports/
		Create or update switch port.
		"""
		if port is None and hwaddress is None:
			self.module.fail_json(msg="Either port or hwaddress is required.")

		data = self._build_switchport_payload(
			port=port,
			port_id=port_id,
			hwaddress=hwaddress,
			new_port=new_port,
			switch=switch,
			description=description,
			type=type,
			vlan_id=vlan_id,
			vlan=vlan,
			vlan_ids=vlan_ids,
			vlans=vlans,
			clear_vlan_ids=clear_vlan_ids,
			clear_vlans=clear_vlans,
			up=up,
			up_admin=up_admin,
			count=count,
			remote_port_id=remote_port_id,
			remote_device=remote_device,
			remote_port=remote_port,
			module=module,
			device2=device2,
			device=device,
			label=label,
			tags=tags,
			tags_remove=tags_remove,
			mtu=mtu,
			name=name,
			speed=speed,
			remote_port_clear=remote_port_clear,
			parent_port=parent_port,
			parent_port_device=parent_port_device,
			slave_ports=slave_ports,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/switchports/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_switchport(self, id: int) -> dict:
		"""
		DELETE /api/1.0/switchports/{id}/
		Delete switch port by ID.
		"""
		resolved_id = int(id)
		return self.auth.request(f"/api/1.0/switchports/{resolved_id}/", method="DELETE")
