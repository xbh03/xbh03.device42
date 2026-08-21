from urllib.parse import urlencode

from ...admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_ipam_vlans:
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

	def d42_get_vlans(
		self,
		vlan_id: int = None,
		number: int = None,
		name: str = None,
		tags: str = None,
		tags_and: str = None,
		description: str = None,
		switch_ids: str = None,
		switches: str = None,
		last_updated_lt: str = None,
		last_updated_gt: str = None,
		first_added_lt: str = None,
		first_added_gt: str = None,
	) -> dict:
		"""
		GET /api/1.0/vlans/
		Retrieve all VLANs.
		"""
		params = {}

		if vlan_id is not None:
			params["vlan_id"] = int(vlan_id)
		if number is not None:
			params["number"] = int(number)
		if name is not None:
			params["name"] = name
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if description is not None:
			params["description"] = description
		if switch_ids is not None:
			params["switch_ids"] = switch_ids
		if switches is not None:
			params["switches"] = switches
		if last_updated_lt is not None:
			params["last_updated_lt"] = last_updated_lt
		if last_updated_gt is not None:
			params["last_updated_gt"] = last_updated_gt
		if first_added_lt is not None:
			params["first_added_lt"] = first_added_lt
		if first_added_gt is not None:
			params["first_added_gt"] = first_added_gt

		endpoint = "/api/1.0/vlans/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_vlan_by_id(self, id: int) -> dict:
		"""
		GET /api/1.0/vlans/{id}/
		Retrieve VLAN by Device42 VLAN ID.
		"""
		resolved_id = int(id)
		return self.auth.request(f"/api/1.0/vlans/{resolved_id}/", method="GET")

	def _build_vlan_payload(
		self,
		number: int = None,
		name: str = None,
		description: str = None,
		switch_ids: str = None,
		switches: str = None,
		clear_switches: str = None,
		clear_switch_ids: str = None,
		tags: str = None,
		notes: str = None,
		groups: str = None,
	) -> dict:
		data = {}

		if number is not None:
			data["number"] = int(number)
		if name is not None:
			data["name"] = name
		if description is not None:
			data["description"] = description
		if switch_ids is not None:
			data["switch_ids"] = switch_ids
		if switches is not None:
			data["switches"] = switches
		if clear_switches is not None:
			data["clear_switches"] = clear_switches
		if clear_switch_ids is not None:
			data["clear_switch_ids"] = clear_switch_ids
		if tags is not None:
			data["tags"] = tags
		if notes is not None:
			data["notes"] = notes
		if groups is not None:
			data["groups"] = groups

		return data

	def d42_post_vlans(
		self,
		number: int,
		name: str = None,
		description: str = None,
		switch_ids: str = None,
		switches: str = None,
		tags: str = None,
		notes: str = None,
		groups: str = None,
	) -> dict:
		"""
		POST /api/1.0/vlans/
		Create VLAN.
		"""
		data = self._build_vlan_payload(
			number=number,
			name=name,
			description=description,
			switch_ids=switch_ids,
			switches=switches,
			tags=tags,
			notes=notes,
			groups=groups,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/vlans/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_put_vlans(
		self,
		id: int,
		number: int = None,
		name: str = None,
		switch_ids: str = None,
		switches: str = None,
		clear_switches: str = None,
		clear_switch_ids: str = None,
		tags: str = None,
		description: str = None,
		notes: str = None,
		groups: str = None,
	) -> dict:
		"""
		PUT /api/1.0/vlans/
		Create/update specific VLAN using ID in form data.
		"""
		data = self._build_vlan_payload(
			number=number,
			name=name,
			description=description,
			switch_ids=switch_ids,
			switches=switches,
			clear_switches=clear_switches,
			clear_switch_ids=clear_switch_ids,
			tags=tags,
			notes=notes,
			groups=groups,
		)
		data["id"] = int(id)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/vlans/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_put_vlan_by_id(
		self,
		id: int,
		number: int = None,
		name: str = None,
		switch_ids: str = None,
		switches: str = None,
		tags: str = None,
		description: str = None,
		notes: str = None,
		groups: str = None,
	) -> dict:
		"""
		PUT /api/1.0/vlans/{id}/
		Update VLAN using ID in URL.
		"""
		resolved_id = int(id)
		data = self._build_vlan_payload(
			number=number,
			name=name,
			description=description,
			switch_ids=switch_ids,
			switches=switches,
			tags=tags,
			notes=notes,
			groups=groups,
		)

		payload = urlencode(data)
		return self.auth.request(
			f"/api/1.0/vlans/{resolved_id}/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_vlan(self, id: int) -> dict:
		"""
		DELETE /api/1.0/vlans/{id}/
		Delete VLAN by Device42 VLAN ID.
		"""
		resolved_id = int(id)
		return self.auth.request(f"/api/1.0/vlans/{resolved_id}/", method="DELETE")
