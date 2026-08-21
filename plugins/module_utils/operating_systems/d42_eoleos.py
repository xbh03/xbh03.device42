from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_eoleos:
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

	def d42_get_os_eoleos(self) -> dict:
		"""
		GET /api/1.0/os_eoleos/
		Get operating systems End of Life / End of Support information.
		"""
		return self.auth.request("/api/1.0/os_eoleos/", method="GET")

	def _build_os_eoleos_payload(
		self,
		id: int = None,
		os_id: int = None,
		os: str = None,
		version: str = None,
		end_of_life: str = None,
		end_of_support: str = None,
	) -> dict:
		data = {}

		if id is not None:
			data["id"] = int(id)
		if os_id is not None:
			data["os_id"] = int(os_id)
		if os is not None:
			data["os"] = os
		if version is not None:
			data["version"] = version
		if end_of_life is not None:
			data["end_of_life"] = end_of_life
		if end_of_support is not None:
			data["end_of_support"] = end_of_support

		return data

	def d42_post_os_eoleos(
		self,
		id: int = None,
		os_id: int = None,
		os: str = None,
		version: str = None,
		end_of_life: str = None,
		end_of_support: str = None,
	) -> dict:
		"""
		POST /api/1.0/os_eoleos/
		Create or update OS EOL/EOS information.
		"""
		data = self._build_os_eoleos_payload(
			id=id,
			os_id=os_id,
			os=os,
			version=version,
			end_of_life=end_of_life,
			end_of_support=end_of_support,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/os_eoleos/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_os_eoleos(self, id: int) -> dict:
		"""
		DELETE /api/1.0/os_eoleos/{ID}/
		Delete OS EOL/EOS information by ID.
		"""
		resolved_id = int(id)
		return self.auth.request(f"/api/1.0/os_eoleos/{resolved_id}/", method="DELETE")
