from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_appcomps:
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

	def d42_get_appcomps(
		self,
		device_id: int = None,
		device: str = None,
		name: str = None,
		resource_id: int = None,
		category_id: int = None,
		include_cols: str = None,
		category: str = None,
	) -> dict:
		"""
		GET /api/1.0/appcomps/
		Get application components.
		"""
		params = {}

		if device_id is not None:
			params["device_id"] = int(device_id)
		if device is not None:
			params["device"] = device
		if name is not None:
			params["name"] = name
		if resource_id is not None:
			params["resource_id"] = int(resource_id)
		if category_id is not None:
			params["category_id"] = int(category_id)
		if include_cols is not None:
			params["include_cols"] = include_cols
		if category is not None:
			params["category"] = category

		endpoint = "/api/1.0/appcomps/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_appcomp_by_id(self, appcomp_id: int) -> dict:
		"""
		GET /api/1.0/appcomps/{appcomp_id}/
		Get a specific application component by ID.
		"""
		resolved_appcomp_id = int(appcomp_id)
		return self.auth.request(f"/api/1.0/appcomps/{resolved_appcomp_id}/", method="GET")

	def d42_post_appcomps(
		self,
		name: str,
		device: str = None,
		group_owner: str = None,
		what: str = None,
		depends_on: str = None,
		dependents: str = None,
		groups_affected: str = None,
		device_reason: str = None,
		depends_on_reasons: str = None,
		category: str = None,
		category_id: int = None,
		tags_remove: str = None,
		customer: str = None,
		notes: str = None,
		service_detail_ids: str = None,
		software_detail_ids: str = None,
		tags: str = None,
	) -> dict:
		"""
		POST /api/1.0/appcomps/
		Create/update application components.
		"""
		data = {"name": name}

		if device is not None:
			data["device"] = device
		if group_owner is not None:
			data["group_owner"] = group_owner
		if what is not None:
			data["what"] = what
		if depends_on is not None:
			data["depends_on"] = depends_on
		if dependents is not None:
			data["dependents"] = dependents
		if groups_affected is not None:
			data["groups_affected"] = groups_affected
		if device_reason is not None:
			data["device_reason"] = device_reason
		if depends_on_reasons is not None:
			data["depends_on_reasons"] = depends_on_reasons
		if category is not None:
			data["category"] = category
		if category_id is not None:
			data["category_id"] = int(category_id)
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if customer is not None:
			data["customer"] = customer
		if notes is not None:
			data["notes"] = notes
		if service_detail_ids is not None:
			data["service_detail_ids"] = service_detail_ids
		if software_detail_ids is not None:
			data["software_detail_ids"] = software_detail_ids
		if tags is not None:
			data["tags"] = tags

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/appcomps/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_appcomp(self, appcomp_id: int) -> dict:
		"""
		DELETE /api/1.0/appcomps/{appcomp_id}/
		Delete an application component by ID.
		"""
		resolved_appcomp_id = int(appcomp_id)
		return self.auth.request(f"/api/1.0/appcomps/{resolved_appcomp_id}/", method="DELETE")

	def d42_put_custom_field_appcomp(
		self,
		key: str,
		appcomp_id: int = None,
		name: str = None,
		type: str = None,
		mandatory: str = None,
		filterable: str = None,
		log_for_api: str = None,
		related_field_name: str = None,
		add_to_picklist: str = None,
		remove_from_picklist: str = None,
		delete_in_use: str = None,
		related_field_value_by_id: str = None,
		value: str = None,
		clear_value: str = None,
		show_on_chart: str = None,
		notes: str = None,
		clear_notes: str = None,
		bulk_fields: str = None,
		multi_select: str = None,
	) -> dict:
		"""
		PUT /api/1.0/custom_fields/appcomp/
		Set custom fields for application components.
		Requires key and one of appcomp_id/name.
		"""
		if appcomp_id is None and name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either appcomp_id or name is required for custom field update.")
			raise ValueError("Either appcomp_id or name is required for custom field update.")

		data = {"key": key}

		if appcomp_id is not None:
			data["id"] = int(appcomp_id)
		if name is not None:
			data["name"] = name
		if type is not None:
			data["type"] = type
		if mandatory is not None:
			data["mandatory"] = mandatory
		if filterable is not None:
			data["filterable"] = filterable
		if log_for_api is not None:
			data["log_for_api"] = log_for_api
		if related_field_name is not None:
			data["related_field_name"] = related_field_name
		if add_to_picklist is not None:
			data["add_to_picklist"] = add_to_picklist
		if remove_from_picklist is not None:
			data["remove_from_picklist"] = remove_from_picklist
		if delete_in_use is not None:
			data["delete_in_use"] = delete_in_use
		if related_field_value_by_id is not None:
			data["related_field_value_by_id"] = related_field_value_by_id
		if value is not None:
			data["value"] = value
		if clear_value is not None:
			data["clear_value"] = clear_value
		if show_on_chart is not None:
			data["show_on_chart"] = show_on_chart
		if notes is not None:
			data["notes"] = notes
		if clear_notes is not None:
			data["clear_notes"] = clear_notes
		if bulk_fields is not None:
			data["bulk_fields"] = bulk_fields
		if multi_select is not None:
			data["multi_select"] = multi_select

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/custom_fields/appcomp/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)
