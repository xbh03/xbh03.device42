from .d42_token_authentication import d42_token_authentication


class d42_client_keys:
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

	def d42_get_api_client_keys(self) -> dict:
		"""
		GET /api/2.0/api_client_keys/
		Get API Client Keys.

		Returns a payload like:
		{
		  "apiclient_key": "...",
		  "apiclient_secret_key": "..."
		}
		"""
		return self.auth.request("/api/2.0/api_client_keys/", method="GET")
