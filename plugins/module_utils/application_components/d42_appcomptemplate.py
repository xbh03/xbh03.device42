from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_appcomptemplate:
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

	def d42_get_appcomp_templates(
		self,
		template_id: int = None,
		name: str = None,
		enabled: str = None,
		rule_type: str = None,
		rule_type_id: int = None,
		service_id: int = None,
		service_listening_port: int = None,
		app_name_pattern: str = None,
		related_services_listening_port: int = None,
		config_file_location: str = None,
		traverse_subdirectories: str = None,
		filename_filter: str = None,
		application_category_id: int = None,
		application_category_name: str = None,
		what: str = None,
		customer_id: int = None,
		customer: str = None,
		last_changed_lt: str = None,
		last_changed_gt: str = None,
		service_cmd_arg_match: str = None,
		tags: str = None,
		match_type: str = None,
		match_type_id: int = None,
	) -> dict:
		"""
		GET /api/2.0/appcomp_templates/
		Get all application component templates.
		"""
		params = {}

		if template_id is not None:
			params["id"] = int(template_id)
		if name is not None:
			params["name"] = name
		if enabled is not None:
			params["enabled"] = enabled
		if rule_type is not None:
			params["rule_type"] = rule_type
		if rule_type_id is not None:
			params["rule_type_id"] = int(rule_type_id)
		if service_id is not None:
			params["service_id"] = int(service_id)
		if service_listening_port is not None:
			params["service_listening_port"] = int(service_listening_port)
		if app_name_pattern is not None:
			params["app_name_pattern"] = app_name_pattern
		if related_services_listening_port is not None:
			params["related_services_listening_port"] = int(related_services_listening_port)
		if config_file_location is not None:
			params["config_file_location"] = config_file_location
		if traverse_subdirectories is not None:
			params["traverse_subdirectories"] = traverse_subdirectories
		if filename_filter is not None:
			params["filename_filter"] = filename_filter
		if application_category_id is not None:
			params["application_category_id"] = int(application_category_id)
		if application_category_name is not None:
			params["application_category_name"] = application_category_name
		if what is not None:
			params["what"] = what
		if customer_id is not None:
			params["customer_id"] = int(customer_id)
		if customer is not None:
			params["customer"] = customer
		if last_changed_lt is not None:
			params["last_changed_lt"] = last_changed_lt
		if last_changed_gt is not None:
			params["last_changed_gt"] = last_changed_gt
		if service_cmd_arg_match is not None:
			params["service_cmd_arg_match"] = service_cmd_arg_match
		if tags is not None:
			params["tags"] = tags
		if match_type is not None:
			params["match_type"] = match_type
		if match_type_id is not None:
			params["match_type_id"] = int(match_type_id)

		endpoint = "/api/2.0/appcomp_templates/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_post_appcomp_template(
		self,
		template_id: int = None,
		name: str = None,
		enabled: str = None,
		rule_type: str = None,
		rule_type_id: int = None,
		service_id: int = None,
		associated_software_id: int = None,
		service: str = None,
		service_listening_port: int = None,
		app_name_pattern: str = None,
		related_services_listening_port: int = None,
		config_file_location: str = None,
		traverse_subdirectories: str = None,
		filename_filter: str = None,
		application_category: str = None,
		application_category_id: int = None,
		customer_id: int = None,
		customer: str = None,
		what: str = None,
		tags: str = None,
		tags_remove: str = None,
		related_services_ids: str = None,
		related_services_ids_remove: str = None,
		related_software_ids: str = None,
		related_software_ids_remove: str = None,
		service_cmd_arg_match: str = None,
		match_type: str = None,
		match_type_id: int = None,
	) -> dict:
		"""
		POST /api/2.0/appcomp_templates/
		Create/update an application component template.
		"""
		if template_id is None and name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either template_id or name is required for app component template create/update.")
			raise ValueError("Either template_id or name is required for app component template create/update.")

		data = {}

		if template_id is not None:
			data["id"] = int(template_id)
		if name is not None:
			data["name"] = name
		if enabled is not None:
			data["enabled"] = enabled
		if rule_type is not None:
			data["rule_type"] = rule_type
		if rule_type_id is not None:
			data["rule_type_id"] = int(rule_type_id)
		if service_id is not None:
			data["service_id"] = int(service_id)
		if associated_software_id is not None:
			data["associated_software_id"] = int(associated_software_id)
		if service is not None:
			data["service"] = service
		if service_listening_port is not None:
			data["service_listening_port"] = int(service_listening_port)
		if app_name_pattern is not None:
			data["app_name_pattern"] = app_name_pattern
		if related_services_listening_port is not None:
			data["related_services_listening_port"] = int(related_services_listening_port)
		if config_file_location is not None:
			data["config_file_location"] = config_file_location
		if traverse_subdirectories is not None:
			data["traverse_subdirectories"] = traverse_subdirectories
		if filename_filter is not None:
			data["filename_filter"] = filename_filter
		if application_category is not None:
			data["application_category"] = application_category
		if application_category_id is not None:
			data["application_category_id"] = int(application_category_id)
		if customer_id is not None:
			data["customer_id"] = int(customer_id)
		if customer is not None:
			data["customer"] = customer
		if what is not None:
			data["what"] = what
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if related_services_ids is not None:
			data["related_services_ids"] = related_services_ids
		if related_services_ids_remove is not None:
			data["related_services_ids_remove"] = related_services_ids_remove
		if related_software_ids is not None:
			data["related_software_ids"] = related_software_ids
		if related_software_ids_remove is not None:
			data["related_software_ids_remove"] = related_software_ids_remove
		if service_cmd_arg_match is not None:
			data["service_cmd_arg_match"] = service_cmd_arg_match
		if match_type is not None:
			data["match_type"] = match_type
		if match_type_id is not None:
			data["match_type_id"] = int(match_type_id)

		payload = urlencode(data)
		return self.auth.request(
			"/api/2.0/appcomp_templates/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_appcomp_template(self, template_id: int) -> dict:
		"""
		DELETE /api/2.0/appcomp_templates/{id}/
		Delete an application component template by ID.
		"""
		resolved_template_id = int(template_id)
		return self.auth.request(f"/api/2.0/appcomp_templates/{resolved_template_id}/", method="DELETE")
