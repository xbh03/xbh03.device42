from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_cables:
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

	def d42_get_cables(self, cable_id: str = None) -> dict:
		"""
		GET /api/1.0/cables/
		Retrieve information about all cables.
		"""
		params = {}

		if cable_id is not None:
			params["cable_id"] = cable_id

		endpoint = "/api/1.0/cables/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def _build_cable_payload(
		self,
		id: int = None,
		cable_id: str = None,
		vendor: str = None,
		notes: str = None,
		groups: str = None,
		room_id: int = None,
		room: str = None,
		origin_clear: str = None,
		origin_type: str = None,
		origin_id: int = None,
		origin_connector_type: str = None,
		origin_cable_type: str = None,
		origin_cable_color: str = None,
		origin_optic_type: str = None,
		origin_back_patch_panel: str = None,
		end_clear: str = None,
		end_point_type: str = None,
		end_point_id: int = None,
		end_connector_type: str = None,
		end_cable_type: str = None,
		end_cable_color: str = None,
		end_optic_type: str = None,
		end_point_back_patch_panel: str = None,
		end_point_multiple: str = None,
		cable_length: str = None,
		cable_length_units: str = None,
	) -> dict:
		data = {}

		if id is not None:
			data["id"] = int(id)
		if cable_id is not None:
			data["cable_id"] = cable_id
		if vendor is not None:
			data["vendor"] = vendor
		if notes is not None:
			data["notes"] = notes
		if groups is not None:
			data["groups"] = groups
		if room_id is not None:
			data["room_id"] = int(room_id)
		if room is not None:
			data["room"] = room
		if origin_clear is not None:
			data["origin_clear"] = origin_clear
		if origin_type is not None:
			data["origin_type"] = origin_type
		if origin_id is not None:
			data["origin_id"] = int(origin_id)
		if origin_connector_type is not None:
			data["origin_connector_type"] = origin_connector_type
		if origin_cable_type is not None:
			data["origin_cable_type"] = origin_cable_type
		if origin_cable_color is not None:
			data["origin_cable_color"] = origin_cable_color
		if origin_optic_type is not None:
			data["origin_optic_type"] = origin_optic_type
		if origin_back_patch_panel is not None:
			data["origin_back_patch_panel"] = origin_back_patch_panel
		if end_clear is not None:
			data["end_clear"] = end_clear
		if end_point_type is not None:
			data["end_point_type"] = end_point_type
		if end_point_id is not None:
			data["end_point_id"] = int(end_point_id)
		if end_connector_type is not None:
			data["end_connector_type"] = end_connector_type
		if end_cable_type is not None:
			data["end_cable_type"] = end_cable_type
		if end_cable_color is not None:
			data["end_cable_color"] = end_cable_color
		if end_optic_type is not None:
			data["end_optic_type"] = end_optic_type
		if end_point_back_patch_panel is not None:
			data["end_point_back_patch_panel"] = end_point_back_patch_panel
		if end_point_multiple is not None:
			data["end_point_multiple"] = end_point_multiple
		if cable_length is not None:
			data["cable_length"] = cable_length
		if cable_length_units is not None:
			data["cable_length_units"] = cable_length_units

		return data

	def d42_post_cables(
		self,
		id: int = None,
		cable_id: str = None,
		vendor: str = None,
		notes: str = None,
		groups: str = None,
		room_id: int = None,
		room: str = None,
		origin_clear: str = None,
		origin_type: str = None,
		origin_id: int = None,
		origin_connector_type: str = None,
		origin_cable_type: str = None,
		origin_cable_color: str = None,
		origin_optic_type: str = None,
		origin_back_patch_panel: str = None,
		end_clear: str = None,
		end_point_type: str = None,
		end_point_id: int = None,
		end_connector_type: str = None,
		end_cable_type: str = None,
		end_cable_color: str = None,
		end_optic_type: str = None,
		end_point_back_patch_panel: str = None,
		end_point_multiple: str = None,
		cable_length: str = None,
		cable_length_units: str = None,
	) -> dict:
		"""
		POST /api/1.0/cables/
		Create or update cable information.
		"""
		data = self._build_cable_payload(
			id=id,
			cable_id=cable_id,
			vendor=vendor,
			notes=notes,
			groups=groups,
			room_id=room_id,
			room=room,
			origin_clear=origin_clear,
			origin_type=origin_type,
			origin_id=origin_id,
			origin_connector_type=origin_connector_type,
			origin_cable_type=origin_cable_type,
			origin_cable_color=origin_cable_color,
			origin_optic_type=origin_optic_type,
			origin_back_patch_panel=origin_back_patch_panel,
			end_clear=end_clear,
			end_point_type=end_point_type,
			end_point_id=end_point_id,
			end_connector_type=end_connector_type,
			end_cable_type=end_cable_type,
			end_cable_color=end_cable_color,
			end_optic_type=end_optic_type,
			end_point_back_patch_panel=end_point_back_patch_panel,
			end_point_multiple=end_point_multiple,
			cable_length=cable_length,
			cable_length_units=cable_length_units,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/cables/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_cable(self, cable_pk: int) -> dict:
		"""
		DELETE /api/1.0/cables/{id}/
		Delete a cable by Device42 numeric ID.
		"""
		resolved_cable_pk = int(cable_pk)
		return self.auth.request(f"/api/1.0/cables/{resolved_cable_pk}/", method="DELETE")
