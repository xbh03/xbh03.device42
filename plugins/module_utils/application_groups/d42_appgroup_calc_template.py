from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_appgroup_calc_template:
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

	def d42_get_appgroup_calc_templates(self, name: str = None) -> dict:
		"""
		GET /api/2.0/app_group_calc_template/
		Get all Application Group Calculation Templates.
		"""
		params = {}

		if name is not None:
			params["name"] = name

		endpoint = "/api/2.0/app_group_calc_template/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_appgroup_calc_template_by_id(self, template_id: int) -> dict:
		"""
		GET /api/2.0/app_group_calc_template/{id}/
		Get a single Application Group Calculation Template by ID.
		"""
		resolved_template_id = int(template_id)
		return self.auth.request(f"/api/2.0/app_group_calc_template/{resolved_template_id}/", method="GET")

	def d42_post_appgroup_calc_template(self, payload: dict) -> dict:
		"""
		POST /api/2.0/app_group_calc_template/
		Create or update an Application Group Calculation Template.
		"""
		if not isinstance(payload, dict) or not payload:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="payload must be a non-empty dictionary for app group calc template create/update.")
			raise ValueError("payload must be a non-empty dictionary for app group calc template create/update.")

		return self.auth.request(
			"/api/2.0/app_group_calc_template/",
			method="POST",
			json=payload,
			headers={"Content-Type": "application/json"},
		)

	def d42_delete_appgroup_calc_template(self, template_id: int) -> dict:
		"""
		DELETE /api/2.0/app_group_calc_template/{id}/
		Delete an Application Group Calculation Template by ID.
		"""
		resolved_template_id = int(template_id)
		return self.auth.request(f"/api/2.0/app_group_calc_template/{resolved_template_id}/", method="DELETE")
