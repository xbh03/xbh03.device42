from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_operating_systems:
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

	def d42_get_operating_systems(
		self,
		name: str = None,
		manufacturer: str = None,
		category: str = None,
	) -> dict:
		"""
		GET /api/1.0/operatingsystems/
		Get information about operating systems.
		"""
		params = {}

		if name is not None:
			params["name"] = name
		if manufacturer is not None:
			params["manufacturer"] = manufacturer
		if category is not None:
			params["category"] = category

		endpoint = "/api/1.0/operatingsystems/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_operating_system_by_id(self, operating_system_id: int) -> dict:
		"""
		GET /api/1.0/operatingsystems/{id}/
		Retrieve detailed information about a specific operating system by ID.
		"""
		resolved_os_id = int(operating_system_id)
		return self.auth.request(f"/api/1.0/operatingsystems/{resolved_os_id}/", method="GET")

	def _build_operating_system_payload(
		self,
		name: str = None,
		manufacturer: str = None,
		notes: str = None,
		category: str = None,
		licensed_count: str = None,
		licensing_model: str = None,
	) -> dict:
		data = {}

		if name is not None:
			data["name"] = name
		if manufacturer is not None:
			data["manufacturer"] = manufacturer
		if notes is not None:
			data["notes"] = notes
		if category is not None:
			data["category"] = category
		if licensed_count is not None:
			data["licensed_count"] = licensed_count
		if licensing_model is not None:
			data["licensing_model"] = licensing_model

		return data

	def d42_post_operating_systems(
		self,
		name: str,
		manufacturer: str = None,
		notes: str = None,
		category: str = None,
		licensed_count: str = None,
		licensing_model: str = None,
	) -> dict:
		"""
		POST /api/1.0/operatingsystems/
		Create or update information about operating systems.
		"""
		data = self._build_operating_system_payload(
			name=name,
			manufacturer=manufacturer,
			notes=notes,
			category=category,
			licensed_count=licensed_count,
			licensing_model=licensing_model,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/operatingsystems/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_operating_system(self, operating_system_id: int) -> dict:
		"""
		DELETE /api/1.0/operatingsystems/{id}/
		Delete an operating system by ID.
		"""
		resolved_os_id = int(operating_system_id)
		return self.auth.request(f"/api/1.0/operatingsystems/{resolved_os_id}/", method="DELETE")
