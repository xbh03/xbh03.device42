from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_services:
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

	def d42_get_services(
		self,
		service_id: int = None,
		displayname: str = None,
		category: str = None,
		vendor: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/2.0/services/
		Get all services.
		"""
		params = {}

		if service_id is not None:
			params["id"] = int(service_id)
		if displayname is not None:
			params["displayname"] = displayname
		if category is not None:
			params["category"] = category
		if vendor is not None:
			params["vendor"] = vendor
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/2.0/services/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")
