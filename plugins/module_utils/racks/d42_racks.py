from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_racks:
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

	def d42_get_racks(
		self,
		name: str = None,
		building_id: int = None,
		building: str = None,
		room_id: int = None,
		room: str = None,
		size: int = None,
		row: str = None,
		asset_no: str = None,
		manufacturer: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/1.0/racks/
		Retrieve basic information about all racks.
		"""
		params = {}

		if name is not None:
			params["name"] = name
		if building_id is not None:
			params["building_id"] = int(building_id)
		if building is not None:
			params["building"] = building
		if room_id is not None:
			params["room_id"] = int(room_id)
		if room is not None:
			params["room"] = room
		if size is not None:
			params["size"] = int(size)
		if row is not None:
			params["row"] = row
		if asset_no is not None:
			params["asset_no"] = asset_no
		if manufacturer is not None:
			params["manufacturer"] = manufacturer
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/1.0/racks/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")
