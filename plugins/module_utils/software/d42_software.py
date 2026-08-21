from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_software:
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

	def d42_get_software(
		self,
		name: str = None,
		category: str = None,
		vendor: str = None,
		licensing_model: str = None,
		software_type: str = None,
		deployment_type: str = None,
		tags: str = None,
		tags_and: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/1.0/software/
		Get software component details.
		"""
		params = {}

		if name is not None:
			params["name"] = name
		if category is not None:
			params["category"] = category
		if vendor is not None:
			params["vendor"] = vendor
		if licensing_model is not None:
			params["licensing_model"] = licensing_model
		if software_type is not None:
			params["software_type"] = software_type
		if deployment_type is not None:
			params["deployment_type"] = deployment_type
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/1.0/software/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")
