from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_telco_circuits:
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

	def d42_get_circuits(
		self,
		id: int = None,
		circuit_id: str = None,
		circuit_type: str = None,
		origin_type: str = None,
		origin_id: int = None,
		end_point_type: str = None,
		end_point_id: int = None,
	) -> dict:
		"""
		GET /api/1.0/circuits/
		Get all circuits or filter by supported query parameters.
		"""
		params = {}

		if id is not None:
			params["id"] = int(id)
		if circuit_id is not None:
			params["circuit_id"] = circuit_id
		if circuit_type is not None:
			params["type"] = circuit_type
		if origin_type is not None:
			params["origin_type"] = origin_type
		if origin_id is not None:
			params["origin_id"] = int(origin_id)
		if end_point_type is not None:
			params["end_point_type"] = end_point_type
		if end_point_id is not None:
			params["end_point_id"] = int(end_point_id)

		endpoint = "/api/1.0/circuits/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")
