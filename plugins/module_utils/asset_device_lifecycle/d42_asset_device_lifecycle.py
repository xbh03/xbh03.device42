from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_asset_device_lifecycle:
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

	def d42_get_lifecycle_events(
		self,
		event_type: str = None,
		device: str = None,
		asset: str = None,
		asset_id: int = None,
		enduser: str = None,
		date_gt: str = None,
		date_lt: str = None,
	) -> dict:
		"""
		GET /api/1.0/lifecycle_event/
		Retrieve life cycle events with optional filters.
		"""
		params = {}

		if event_type is not None:
			params["type"] = event_type
		if device is not None:
			params["device"] = device
		if asset is not None:
			params["asset"] = asset
		if asset_id is not None:
			params["asset_id"] = int(asset_id)
		if enduser is not None:
			params["enduser"] = enduser
		if date_gt is not None:
			params["date_gt"] = date_gt
		if date_lt is not None:
			params["date_lt"] = date_lt

		endpoint = "/api/1.0/lifecycle_event/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_lifecycle_event_by_id(self, event_id: int) -> dict:
		"""
		GET /api/1.0/lifecycle_event/{id}/
		Retrieve a specific lifecycle event by ID.
		"""
		resolved_event_id = int(event_id)
		return self.auth.request(f"/api/1.0/lifecycle_event/{resolved_event_id}/", method="GET")

	def d42_put_lifecycle_event(
		self,
		event_id: int = None,
		date: str = None,
		new_date: str = None,
		event_type: str = None,
		device: str = None,
		device_id: int = None,
		asset_no: str = None,
		serial_no: str = None,
		asset_id: int = None,
		fully_qualified_username: str = None,
		tags: str = None,
		tags_remove: str = None,
		enduser_id: int = None,
		user: str = None,
		notes: str = None,
	) -> dict:
		"""
		PUT /api/1.0/lifecycle_event/
		Create or update lifecycle events for devices/assets.
		"""
		if date is None and new_date is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="date or new_date is required for lifecycle event create/update.")
			raise ValueError("date or new_date is required for lifecycle event create/update.")

		if event_type is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="event_type is required for lifecycle event create/update.")
			raise ValueError("event_type is required for lifecycle event create/update.")

		targets = [event_id, device, device_id, asset_no, serial_no, asset_id]
		if all(target is None for target in targets):
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(
					msg=(
						"One target identifier is required: event_id, device, device_id, "
						"asset_no, serial_no, or asset_id."
					)
				)
			raise ValueError(
				"One target identifier is required: event_id, device, device_id, asset_no, serial_no, or asset_id."
			)

		data = {}

		if event_id is not None:
			data["id"] = int(event_id)
		if date is not None:
			data["date"] = date
		if new_date is not None:
			data["new_date"] = new_date
		if event_type is not None:
			data["type"] = event_type
		if device is not None:
			data["device"] = device
		if device_id is not None:
			data["device_id"] = int(device_id)
		if asset_no is not None:
			data["asset_no"] = asset_no
		if serial_no is not None:
			data["serial_no"] = serial_no
		if asset_id is not None:
			data["asset_id"] = int(asset_id)
		if fully_qualified_username is not None:
			data["fully_qualified_username"] = fully_qualified_username
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if enduser_id is not None:
			data["enduser_id"] = int(enduser_id)
		if user is not None:
			data["user"] = user
		if notes is not None:
			data["notes"] = notes

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/lifecycle_event/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_lifecycle_event(self, event_id: int) -> dict:
		"""
		DELETE /api/1.0/lifecycle_event/{id}/
		Delete a lifecycle event by ID.
		"""
		resolved_event_id = int(event_id)
		return self.auth.request(f"/api/1.0/lifecycle_event/{resolved_event_id}/", method="DELETE")
