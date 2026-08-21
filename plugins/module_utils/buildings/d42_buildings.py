from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_buildings:
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

	def d42_get_buildings(self, name: str = None, include_cols: str = None) -> dict:
		"""
		GET /api/1.0/buildings/
		Retrieve information about all buildings.
		"""
		params = {}

		if name is not None:
			params["name"] = name
		if include_cols is not None:
			params["include_cols"] = include_cols

		endpoint = "/api/1.0/buildings/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_building_by_id(self, building_id: int, include_cols: str = None) -> dict:
		"""
		GET /api/1.0/buildings/{id}/
		Retrieve detailed information about a specific building.
		"""
		resolved_building_id = int(building_id)
		endpoint = f"/api/1.0/buildings/{resolved_building_id}/"

		if include_cols is not None:
			endpoint = f"{endpoint}?{urlencode({'include_cols': include_cols})}"

		return self.auth.request(endpoint, method="GET")

	def _build_building_payload(
		self,
		name: str = None,
		latitude: str = None,
		longitude: str = None,
		address: str = None,
		contact_name: str = None,
		contact_phone: str = None,
		notes: str = None,
		groups: str = None,
		tags: str = None,
		tags_remove: str = None,
		new_name: str = None,
	) -> dict:
		data = {}

		if name is not None:
			data["name"] = name
		if latitude is not None:
			data["latitude"] = latitude
		if longitude is not None:
			data["longitude"] = longitude
		if address is not None:
			data["address"] = address
		if contact_name is not None:
			data["contact_name"] = contact_name
		if contact_phone is not None:
			data["contact_phone"] = contact_phone
		if notes is not None:
			data["notes"] = notes
		if groups is not None:
			data["groups"] = groups
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if new_name is not None:
			data["new_name"] = new_name

		return data

	def d42_post_buildings(
		self,
		name: str,
		latitude: str = None,
		longitude: str = None,
		address: str = None,
		contact_name: str = None,
		contact_phone: str = None,
		notes: str = None,
		groups: str = None,
		tags: str = None,
		tags_remove: str = None,
		new_name: str = None,
	) -> dict:
		"""
		POST /api/1.0/buildings/
		Create or update a building.
		"""
		data = self._build_building_payload(
			name=name,
			latitude=latitude,
			longitude=longitude,
			address=address,
			contact_name=contact_name,
			contact_phone=contact_phone,
			notes=notes,
			groups=groups,
			tags=tags,
			tags_remove=tags_remove,
			new_name=new_name,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/buildings/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_building(self, building_id: int) -> dict:
		"""
		DELETE /api/1.0/buildings/{id}/
		Delete a building by ID.
		"""
		resolved_building_id = int(building_id)
		return self.auth.request(f"/api/1.0/buildings/{resolved_building_id}/", method="DELETE")

	def d42_put_custom_field_building(
		self,
		key: str,
		building_id: int = None,
		name: str = None,
		type: str = None,
		mandatory: str = None,
		filterable: str = None,
		log_for_api: str = None,
		related_field_name: str = None,
		add_to_picklist: str = None,
		remove_from_picklist: str = None,
		delete_in_use: str = None,
		related_field_value_by_id: str = None,
		value: str = None,
		clear_value: str = None,
		notes: str = None,
		clear_notes: str = None,
		groups: str = None,
		bulk_fields: str = None,
		multi_select: str = None,
	) -> dict:
		"""
		PUT /api/1.0/custom_fields/building/
		Set custom fields for buildings.
		Requires key and one of building_id/name.
		"""
		if building_id is None and name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either building_id or name is required for building custom field update.")
			raise ValueError("Either building_id or name is required for building custom field update.")

		data = {"key": key}

		if building_id is not None:
			data["id"] = int(building_id)
		if name is not None:
			data["name"] = name
		if type is not None:
			data["type"] = type
		if mandatory is not None:
			data["mandatory"] = mandatory
		if filterable is not None:
			data["filterable"] = filterable
		if log_for_api is not None:
			data["log_for_api"] = log_for_api
		if related_field_name is not None:
			data["related_field_name"] = related_field_name
		if add_to_picklist is not None:
			data["add_to_picklist"] = add_to_picklist
		if remove_from_picklist is not None:
			data["remove_from_picklist"] = remove_from_picklist
		if delete_in_use is not None:
			data["delete_in_use"] = delete_in_use
		if related_field_value_by_id is not None:
			data["related_field_value_by_id"] = related_field_value_by_id
		if value is not None:
			data["value"] = value
		if clear_value is not None:
			data["clear_value"] = clear_value
		if notes is not None:
			data["notes"] = notes
		if clear_notes is not None:
			data["clear_notes"] = clear_notes
		if groups is not None:
			data["groups"] = groups
		if bulk_fields is not None:
			data["bulk_fields"] = bulk_fields
		if multi_select is not None:
			data["multi_select"] = multi_select

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/custom_fields/building/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)
