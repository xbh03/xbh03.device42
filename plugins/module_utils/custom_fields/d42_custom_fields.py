from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_custom_fields:
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

	def d42_get_custom_fields(
		self,
		object_name: str,
		id: int = None,
		type: str = None,
		key: str = None,
	) -> dict:
		"""
		GET /api/2.0/custom_fields/
		Get custom fields for a given object model.
		"""
		if object_name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="object_name is required for custom field lookup.")
			raise ValueError("object_name is required for custom field lookup.")

		params = {"object_name": object_name}

		if id is not None:
			params["id"] = int(id)
		if type is not None:
			params["type"] = type
		if key is not None:
			params["key"] = key

		endpoint = f"/api/2.0/custom_fields/?{urlencode(params)}"
		return self.auth.request(endpoint, method="GET")

	def d42_put_custom_field(
		self,
		object_name: str,
		key: str,
		type: str = None,
		mandatory: str = None,
		filterable: str = None,
		log_for_api: str = None,
		add_to_picklist: str = None,
		remove_from_picklist: str = None,
		delete_in_use: str = None,
		multi_select: str = None,
		include_in_context_popups: str = None,
		related_field_name: str = None,
	) -> dict:
		"""
		PUT /api/2.0/custom_fields/
		Create or update custom field.
		"""
		if object_name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="object_name is required for custom field update.")
			raise ValueError("object_name is required for custom field update.")

		if key is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="key is required for custom field update.")
			raise ValueError("key is required for custom field update.")

		data = {
			"object_name": object_name,
			"key": key,
		}

		if type is not None:
			data["type"] = type
		if mandatory is not None:
			data["mandatory"] = mandatory
		if filterable is not None:
			data["filterable"] = filterable
		if log_for_api is not None:
			data["log_for_api"] = log_for_api
		if add_to_picklist is not None:
			data["add_to_picklist"] = add_to_picklist
		if remove_from_picklist is not None:
			data["remove_from_picklist"] = remove_from_picklist
		if delete_in_use is not None:
			data["delete_in_use"] = delete_in_use
		if multi_select is not None:
			data["multi_select"] = multi_select
		if include_in_context_popups is not None:
			data["include_in_context_popups"] = include_in_context_popups
		if related_field_name is not None:
			data["related_field_name"] = related_field_name

		payload = urlencode(data)
		return self.auth.request(
			"/api/2.0/custom_fields/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_custom_field(
		self,
		object_name: str,
		id: int = None,
		key: str = None,
		delete_in_use: bool = None,
	) -> dict:
		"""
		DELETE /api/2.0/custom_fields/
		Delete custom field by object_name and id or key.
		"""
		if object_name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="object_name is required for custom field deletion.")
			raise ValueError("object_name is required for custom field deletion.")

		if id is None and key is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="id or key is required for custom field deletion.")
			raise ValueError("id or key is required for custom field deletion.")

		params = {"object_name": object_name}

		if id is not None:
			params["id"] = int(id)
		if key is not None:
			params["key"] = key
		if delete_in_use is not None:
			params["delete_in_use"] = "true" if bool(delete_in_use) else "false"

		endpoint = f"/api/2.0/custom_fields/?{urlencode(params)}"
		return self.auth.request(endpoint, method="DELETE")
