from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_hardware_models:
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

	def d42_get_hardware_models(
		self,
		hardware_id: int = None,
		name: str = None,
		physicalsubtype_id: int = None,
		physicalsubtype: str = None,
		size: str = None,
		blade_size_id: int = None,
		blade_size: str = None,
		depth_id: int = None,
		depth: str = None,
		width_ratio_id: int = None,
		width_ratio: str = None,
		part_number: str = None,
		network_device: str = None,
		blade_host: str = None,
		watts: int = None,
		vendor_id: int = None,
		vendor: str = None,
		custom_fields_and: str = None,
		custom_fields_or: str = None,
		device_id: int = None,
		include_cols: str = None,
	) -> dict:
		"""
		GET /api/2.0/hardwares/
		Get information about hardware models.
		"""
		params = {}

		if hardware_id is not None:
			params["hardware_id"] = int(hardware_id)
		if name is not None:
			params["name"] = name
		if physicalsubtype_id is not None:
			params["physicalsubtype_id"] = int(physicalsubtype_id)
		if physicalsubtype is not None:
			params["physicalsubtype"] = physicalsubtype
		if size is not None:
			params["size"] = size
		if blade_size_id is not None:
			params["blade_size_id"] = int(blade_size_id)
		if blade_size is not None:
			params["blade_size"] = blade_size
		if depth_id is not None:
			params["depth_id"] = int(depth_id)
		if depth is not None:
			params["depth"] = depth
		if width_ratio_id is not None:
			params["width_ratio_id"] = int(width_ratio_id)
		if width_ratio is not None:
			params["width_ratio"] = width_ratio
		if part_number is not None:
			params["part_number"] = part_number
		if network_device is not None:
			params["network_device"] = network_device
		if blade_host is not None:
			params["blade_host"] = blade_host
		if watts is not None:
			params["watts"] = int(watts)
		if vendor_id is not None:
			params["vendor_id"] = int(vendor_id)
		if vendor is not None:
			params["vendor"] = vendor
		if custom_fields_and is not None:
			params["custom_fields_and"] = custom_fields_and
		if custom_fields_or is not None:
			params["custom_fields_or"] = custom_fields_or
		if device_id is not None:
			params["device_id"] = int(device_id)
		if include_cols is not None:
			params["include_cols"] = include_cols

		endpoint = "/api/2.0/hardwares/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_hardware_model_by_id(self, hardware_id: int) -> dict:
		"""
		GET /api/2.0/hardwares/{id}/
		Get hardware model information by hardware model ID.
		"""
		resolved_hardware_id = int(hardware_id)
		return self.auth.request(f"/api/2.0/hardwares/{resolved_hardware_id}/", method="GET")

	def _build_hardware_model_payload(
		self,
		name: str = None,
		hardware_id: int = None,
		physicalsubtype_id: int = None,
		physicalsubtype: str = None,
		size: str = None,
		depth_id: int = None,
		depth: str = None,
		width_ratio_id: int = None,
		width_ratio: str = None,
		blade_size_id: int = None,
		blade_size: str = None,
		vendor_id: int = None,
		vendor: str = None,
		front_image_id: str = None,
		front_image: str = None,
		back_image_id: int = None,
		back_image: str = None,
		network_device: str = None,
		blade_host: str = None,
		add_ports_when_creating_device: str = None,
		part_number: str = None,
		watts: int = None,
		specification_url: str = None,
		end_of_life_date: str = None,
		end_of_support_date: str = None,
		notes: str = None,
	) -> dict:
		data = {}

		if name is not None:
			data["name"] = name
		if hardware_id is not None:
			data["hardware_id"] = int(hardware_id)
		if physicalsubtype_id is not None:
			data["physicalsubtype_id"] = int(physicalsubtype_id)
		if physicalsubtype is not None:
			data["physicalsubtype"] = physicalsubtype
		if size is not None:
			data["size"] = size
		if depth_id is not None:
			data["depth_id"] = int(depth_id)
		if depth is not None:
			data["depth"] = depth
		if width_ratio_id is not None:
			data["width_ratio_id"] = int(width_ratio_id)
		if width_ratio is not None:
			data["width_ratio"] = width_ratio
		if blade_size_id is not None:
			data["blade_size_id"] = int(blade_size_id)
		if blade_size is not None:
			data["blade_size"] = blade_size
		if vendor_id is not None:
			data["vendor_id"] = int(vendor_id)
		if vendor is not None:
			data["vendor"] = vendor
		if front_image_id is not None:
			data["front_image_id"] = front_image_id
		if front_image is not None:
			data["front_image"] = front_image
		if back_image_id is not None:
			data["back_image_id"] = int(back_image_id)
		if back_image is not None:
			data["back_image"] = back_image
		if network_device is not None:
			data["network_device"] = network_device
		if blade_host is not None:
			data["blade_host"] = blade_host
		if add_ports_when_creating_device is not None:
			data["add_ports_when_creating_device"] = add_ports_when_creating_device
		if part_number is not None:
			data["part_number"] = part_number
		if watts is not None:
			data["watts"] = int(watts)
		if specification_url is not None:
			data["specification_url"] = specification_url
		if end_of_life_date is not None:
			data["end_of_life_date"] = end_of_life_date
		if end_of_support_date is not None:
			data["end_of_support_date"] = end_of_support_date
		if notes is not None:
			data["notes"] = notes

		return data

	def d42_post_hardware_models(
		self,
		name: str = None,
		hardware_id: int = None,
		physicalsubtype_id: int = None,
		physicalsubtype: str = None,
		size: str = None,
		depth_id: int = None,
		depth: str = None,
		width_ratio_id: int = None,
		width_ratio: str = None,
		blade_size_id: int = None,
		blade_size: str = None,
		vendor_id: int = None,
		vendor: str = None,
		front_image_id: str = None,
		front_image: str = None,
		back_image_id: int = None,
		back_image: str = None,
		network_device: str = None,
		blade_host: str = None,
		add_ports_when_creating_device: str = None,
		part_number: str = None,
		watts: int = None,
		specification_url: str = None,
		end_of_life_date: str = None,
		end_of_support_date: str = None,
		notes: str = None,
	) -> dict:
		"""
		POST /api/2.0/hardwares/
		Create or update hardware model information.
		"""
		data = self._build_hardware_model_payload(
			name=name,
			hardware_id=hardware_id,
			physicalsubtype_id=physicalsubtype_id,
			physicalsubtype=physicalsubtype,
			size=size,
			depth_id=depth_id,
			depth=depth,
			width_ratio_id=width_ratio_id,
			width_ratio=width_ratio,
			blade_size_id=blade_size_id,
			blade_size=blade_size,
			vendor_id=vendor_id,
			vendor=vendor,
			front_image_id=front_image_id,
			front_image=front_image,
			back_image_id=back_image_id,
			back_image=back_image,
			network_device=network_device,
			blade_host=blade_host,
			add_ports_when_creating_device=add_ports_when_creating_device,
			part_number=part_number,
			watts=watts,
			specification_url=specification_url,
			end_of_life_date=end_of_life_date,
			end_of_support_date=end_of_support_date,
			notes=notes,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/2.0/hardwares/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_hardware_model(self, hardware_id: int) -> dict:
		"""
		DELETE /api/2.0/hardwares/{id}/
		Delete hardware model by ID.
		"""
		resolved_hardware_id = int(hardware_id)
		return self.auth.request(f"/api/2.0/hardwares/{resolved_hardware_id}/", method="DELETE")
