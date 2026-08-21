from urllib.parse import urlencode

from .d42_token_authentication import d42_token_authentication


class d42_adminusers:
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

	def d42_get_adminusers(
		self,
		username: str = None,
		email: str = None,
		include_cols: str = None,
	) -> dict:
		"""
		GET /api/1.0/adminusers/
		Get all admin users.

		Supported filters:
		- username
		- email
		- include_cols
		"""
		params = {}

		if username is not None:
			params["username"] = username
		if email is not None:
			params["email"] = email
		if include_cols is not None:
			params["include_cols"] = include_cols

		endpoint = "/api/1.0/adminusers/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_post_adminusers(
		self,
		user_id: int = None,
		username: str = None,
		password: str = None,
		first_name: str = None,
		last_name: str = None,
		email: str = None,
		is_superuser = None,
		is_staff = None,
		is_active = None,
		password_doesnt_expire = None,
		groups: str = None,
		new_username: str = None,
	) -> dict:
		"""
		POST /api/1.0/adminusers/
		Create/update admin users.
		"""
		if user_id is None and username is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either user_id or username is required for admin user create/update.")
			raise ValueError("Either user_id or username is required for admin user create/update.")

		def _bool_to_api(value):
			if isinstance(value, str):
				parsed = value.strip().lower() in {"1", "true", "yes", "on"}
			else:
				parsed = bool(value)
			return "true" if parsed else "false"

		data = {}

		if user_id is not None:
			data["id"] = int(user_id)
		if username is not None:
			data["username"] = username
		if password is not None:
			data["password"] = password
		if first_name is not None:
			data["first_name"] = first_name
		if last_name is not None:
			data["last_name"] = last_name
		if email is not None:
			data["email"] = email
		if is_superuser is not None:
			data["is_superuser"] = _bool_to_api(is_superuser)
		if is_staff is not None:
			data["is_staff"] = _bool_to_api(is_staff)
		if is_active is not None:
			data["is_active"] = _bool_to_api(is_active)
		if password_doesnt_expire is not None:
			data["password_doesnt_expire"] = _bool_to_api(password_doesnt_expire)
		if groups is not None:
			data["groups"] = groups
		if new_username is not None:
			data["new_username"] = new_username

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/adminusers/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_adminuser(self, user_id: int) -> dict:
		"""
		DELETE /api/1.0/adminusers/{id}/
		Delete an admin user by ID.
		"""
		resolved_user_id = int(user_id)
		return self.auth.request(f"/api/1.0/adminusers/{resolved_user_id}/", method="DELETE")

	def d42_get_adminuser_by_id(self, user_id: int) -> dict:
		"""
		GET /api/1.0/adminusers/{id}/
		Get a specific admin user by ID.
		"""
		resolved_user_id = int(user_id)
		return self.auth.request(f"/api/1.0/adminusers/{resolved_user_id}/", method="GET")

	# Backward-compatible alias.
	def d42_get_adminuser(self, user_id: int) -> dict:
		return self.d42_get_adminuser_by_id(user_id=user_id)
