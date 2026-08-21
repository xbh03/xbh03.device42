from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_service_levels:
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

	def d42_get_service_levels(self) -> dict:
		"""
		GET /api/1.0/service_level/
		Get all service levels.
		"""
		return self.auth.request("/api/1.0/service_level/", method="GET")

	def d42_post_service_level(self, name: str) -> dict:
		"""
		POST /api/1.0/service_level/
		Create a service level.
		"""
		payload = urlencode({"name": name})
		return self.auth.request(
			"/api/1.0/service_level/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)
