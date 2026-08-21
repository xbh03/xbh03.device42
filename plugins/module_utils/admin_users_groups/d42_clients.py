from urllib.parse import urlencode

from .d42_token_authentication import d42_token_authentication


class d42_clients:
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

	def d42_get_api_clients(self, limit: int = 1000, offset: int = 0) -> dict:
		"""
		GET /api/2.0/api_clients/
		Get all API Clients.

		Returns a payload like:
		{
		  "api_client": [...],
		  "total_count": 1,
		  "limit": 1000,
		  "offset": 0
		}
		"""
		params = {}
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/2.0/api_clients/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_post_api_client(
		self,
		client_key: str,
		client_secret_key: str,
		resource_owner: str,
		token_ttl: int = None,
		active: bool = None,
	) -> dict:
		"""
		POST /api/2.0/api_clients/
		Create/update API Client.
		"""
		data = {
			"client_key": client_key,
			"client_secret_key": client_secret_key,
			"resource_owner": resource_owner,
		}

		if token_ttl is not None:
			data["token_ttl"] = int(token_ttl)

		if active is not None:
			if isinstance(active, str):
				active_val = active.strip().lower() in {"1", "true", "yes", "on"}
			else:
				active_val = bool(active)
			data["active"] = "true" if active_val else "false"

		payload = urlencode(data)
		return self.auth.request(
			"/api/2.0/api_clients/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_api_client(self, client_id: int) -> dict:
		"""
		DELETE /api/2.0/api_clients/{client_id}
		Delete an API Client by ID.
		"""
		resolved_client_id = int(client_id)
		return self.auth.request(f"/api/2.0/api_clients/{resolved_client_id}", method="DELETE")

	def d42_get_api_client(self, client_id: int) -> dict:
		"""
		GET /api/2.0/api_clients/{client_id}
		Get an API Client by ID.
		"""
		resolved_client_id = int(client_id)
		return self.auth.request(f"/api/2.0/api_clients/{resolved_client_id}", method="GET")
