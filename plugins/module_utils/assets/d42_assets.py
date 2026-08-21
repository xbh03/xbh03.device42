from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_assets:
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

	def d42_get_assets(
		self,
		asset_no: str = None,
		serial_no: str = None,
		last_updated_lt: str = None,
		last_updated_gt: str = None,
		first_added_lt: str = None,
		first_added_gt: str = None,
		asset_type: str = None,
		asset_id: int = None,
		service_level: str = None,
		customer: str = None,
		tags: str = None,
		tags_and: str = None,
		asset_no_contains: str = None,
		custom_fields_and: str = None,
		custom_fields_or: str = None,
		related_device_id: int = None,
		include_cols: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/1.0/assets/
		Retrieve basic information about all assets.
		"""
		params = {}

		if asset_no is not None:
			params["asset_no"] = asset_no
		if serial_no is not None:
			params["serial_no"] = serial_no
		if last_updated_lt is not None:
			params["last_updated_lt"] = last_updated_lt
		if last_updated_gt is not None:
			params["last_updated_gt"] = last_updated_gt
		if first_added_lt is not None:
			params["first_added_lt"] = first_added_lt
		if first_added_gt is not None:
			params["first_added_gt"] = first_added_gt
		if asset_type is not None:
			params["type"] = asset_type
		if asset_id is not None:
			params["asset_id"] = int(asset_id)
		if service_level is not None:
			params["service_level"] = service_level
		if customer is not None:
			params["customer"] = customer
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if asset_no_contains is not None:
			params["asset_no_contains"] = asset_no_contains
		if custom_fields_and is not None:
			params["custom_fields_and"] = custom_fields_and
		if custom_fields_or is not None:
			params["custom_fields_or"] = custom_fields_or
		if related_device_id is not None:
			params["related_device_id"] = int(related_device_id)
		if include_cols is not None:
			params["include_cols"] = include_cols
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/1.0/assets/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_asset_by_id(self, asset_id: int, include_cols: str = None) -> dict:
		"""
		GET /api/1.0/assets/{id}/
		Retrieve detailed information about a specific asset.
		"""
		resolved_asset_id = int(asset_id)
		endpoint = f"/api/1.0/assets/{resolved_asset_id}/"

		if include_cols is not None:
			endpoint = f"{endpoint}?{urlencode({'include_cols': include_cols})}"

		return self.auth.request(endpoint, method="GET")

	def _build_asset_payload(
		self,
		name: str = None,
		asset: str = None,
		asset_type: str = None,
		service_level: str = None,
		back_connection_type: str = None,
		tap_module_model_id: int = None,
		tap_module_model: str = None,
		tap_module_host_id: int = None,
		tap_module_host: str = None,
		object_category: str = None,
		new_object_category: str = None,
		storage_room: str = None,
		in_service: str = None,
		device_ids: str = None,
		device_name: str = None,
		reversed: str = None,
		building: str = None,
		serial_no: str = None,
		asset_no: str = None,
		customer: str = None,
		storage_room_id: int = None,
		location: str = None,
		notes: str = None,
		vendor: str = None,
		imgfile_id: int = None,
		img: str = None,
		back_image_id: int = None,
		back_image: str = None,
		rack: str = None,
		rack_id: int = None,
		start_at: str = None,
		size: int = None,
		orientation: str = None,
		where: str = None,
		x_pos: int = None,
		depth: str = None,
		device_id: int = None,
		tags: str = None,
		tags_remove: str = None,
		patch_panel_model_id: int = None,
		patch_panel_model: str = None,
		numbering_start_from: int = None,
		patch_panel_module_model_id: int = None,
		patch_panel_module_model: str = None,
		module_host_id: int = None,
		module_host: str = None,
		slot_no: int = None,
		width_ratio: str = None,
		category: str = None,
	) -> dict:
		data = {}

		if name is not None:
			data["name"] = name
		if asset is not None:
			data["asset"] = asset
		if asset_type is not None:
			data["type"] = asset_type
		if service_level is not None:
			data["service_level"] = service_level
		if back_connection_type is not None:
			data["back_connection_type"] = back_connection_type
		if tap_module_model_id is not None:
			data["tap_module_model_id"] = int(tap_module_model_id)
		if tap_module_model is not None:
			data["tap_module_model"] = tap_module_model
		if tap_module_host_id is not None:
			data["tap_module_host_id"] = int(tap_module_host_id)
		if tap_module_host is not None:
			data["tap_module_host"] = tap_module_host
		if object_category is not None:
			data["object_category"] = object_category
		if new_object_category is not None:
			data["new_object_category"] = new_object_category
		if storage_room is not None:
			data["storage_room"] = storage_room
		if in_service is not None:
			data["in_service"] = in_service
		if device_ids is not None:
			data["device_ids"] = device_ids
		if device_name is not None:
			data["device_name"] = device_name
		if reversed is not None:
			data["reversed"] = reversed
		if building is not None:
			data["building"] = building
		if serial_no is not None:
			data["serial_no"] = serial_no
		if asset_no is not None:
			data["asset_no"] = asset_no
		if customer is not None:
			data["customer"] = customer
		if storage_room_id is not None:
			data["storage_room_id"] = int(storage_room_id)
		if location is not None:
			data["location"] = location
		if notes is not None:
			data["notes"] = notes
		if vendor is not None:
			data["vendor"] = vendor
		if imgfile_id is not None:
			data["imgfile_id"] = int(imgfile_id)
		if img is not None:
			data["img"] = img
		if back_image_id is not None:
			data["back_image_id"] = int(back_image_id)
		if back_image is not None:
			data["back_image"] = back_image
		if rack is not None:
			data["rack"] = rack
		if rack_id is not None:
			data["rack_id"] = int(rack_id)
		if start_at is not None:
			data["start_at"] = start_at
		if size is not None:
			data["size"] = int(size)
		if orientation is not None:
			data["orientation"] = orientation
		if where is not None:
			data["where"] = where
		if x_pos is not None:
			data["x_pos"] = int(x_pos)
		if depth is not None:
			data["depth"] = depth
		if device_id is not None:
			data["device_id"] = int(device_id)
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if patch_panel_model_id is not None:
			data["patch_panel_model_id"] = int(patch_panel_model_id)
		if patch_panel_model is not None:
			data["patch_panel_model"] = patch_panel_model
		if numbering_start_from is not None:
			data["numbering_start_from"] = int(numbering_start_from)
		if patch_panel_module_model_id is not None:
			data["patch_panel_module_model_id"] = int(patch_panel_module_model_id)
		if patch_panel_module_model is not None:
			data["patch_panel_module_model"] = patch_panel_module_model
		if module_host_id is not None:
			data["module_host_id"] = int(module_host_id)
		if module_host is not None:
			data["module_host"] = module_host
		if slot_no is not None:
			data["slot_no"] = int(slot_no)
		if width_ratio is not None:
			data["width_ratio"] = width_ratio
		if category is not None:
			data["category"] = category

		return data

	def d42_post_assets(
		self,
		name: str = None,
		asset_type: str = None,
		service_level: str = None,
		back_connection_type: str = None,
		tap_module_model_id: int = None,
		tap_module_model: str = None,
		tap_module_host_id: int = None,
		tap_module_host: str = None,
		object_category: str = None,
		new_object_category: str = None,
		storage_room: str = None,
		in_service: str = None,
		device_ids: str = None,
		device_name: str = None,
		reversed: str = None,
		building: str = None,
		serial_no: str = None,
		asset_no: str = None,
		customer: str = None,
		storage_room_id: int = None,
		location: str = None,
		notes: str = None,
		vendor: str = None,
		imgfile_id: int = None,
		img: str = None,
		back_image_id: int = None,
		back_image: str = None,
		rack: str = None,
		rack_id: int = None,
		start_at: str = None,
		size: int = None,
		orientation: str = None,
		where: str = None,
		x_pos: int = None,
		depth: str = None,
		device_id: int = None,
		tags: str = None,
		tags_remove: str = None,
		patch_panel_model_id: int = None,
		patch_panel_model: str = None,
		numbering_start_from: int = None,
		patch_panel_module_model_id: int = None,
		patch_panel_module_model: str = None,
		module_host_id: int = None,
		module_host: str = None,
		slot_no: int = None,
		width_ratio: str = None,
	) -> dict:
		"""
		POST /api/1.0/assets/
		Create or update assets.
		"""
		data = self._build_asset_payload(
			name=name,
			asset_type=asset_type,
			service_level=service_level,
			back_connection_type=back_connection_type,
			tap_module_model_id=tap_module_model_id,
			tap_module_model=tap_module_model,
			tap_module_host_id=tap_module_host_id,
			tap_module_host=tap_module_host,
			object_category=object_category,
			new_object_category=new_object_category,
			storage_room=storage_room,
			in_service=in_service,
			device_ids=device_ids,
			device_name=device_name,
			reversed=reversed,
			building=building,
			serial_no=serial_no,
			asset_no=asset_no,
			customer=customer,
			storage_room_id=storage_room_id,
			location=location,
			notes=notes,
			vendor=vendor,
			imgfile_id=imgfile_id,
			img=img,
			back_image_id=back_image_id,
			back_image=back_image,
			rack=rack,
			rack_id=rack_id,
			start_at=start_at,
			size=size,
			orientation=orientation,
			where=where,
			x_pos=x_pos,
			depth=depth,
			device_id=device_id,
			tags=tags,
			tags_remove=tags_remove,
			patch_panel_model_id=patch_panel_model_id,
			patch_panel_model=patch_panel_model,
			numbering_start_from=numbering_start_from,
			patch_panel_module_model_id=patch_panel_module_model_id,
			patch_panel_module_model=patch_panel_module_model,
			module_host_id=module_host_id,
			module_host=module_host,
			slot_no=slot_no,
			width_ratio=width_ratio,
		)

		if not data:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="At least one parameter is required for asset create/update.")
			raise ValueError("At least one parameter is required for asset create/update.")

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/assets/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_put_assets_modify(
		self,
		asset_id: int = None,
		asset: str = None,
		name: str = None,
		asset_type: str = None,
		service_level: str = None,
		back_connection_type: str = None,
		tap_module_model_id: int = None,
		tap_module_model: str = None,
		tap_module_host_id: int = None,
		tap_module_host: str = None,
		object_category: str = None,
		new_object_category: str = None,
		storage_room: str = None,
		in_service: str = None,
		device_ids: str = None,
		device_name: str = None,
		reversed: str = None,
		building: str = None,
		serial_no: str = None,
		asset_no: str = None,
		customer: str = None,
		storage_room_id: int = None,
		location: str = None,
		notes: str = None,
		vendor: str = None,
		imgfile_id: int = None,
		img: str = None,
		back_image_id: int = None,
		back_image: str = None,
		rack: str = None,
		rack_id: int = None,
		start_at: str = None,
		size: int = None,
		orientation: str = None,
		where: str = None,
		x_pos: int = None,
		depth: str = None,
		device_id: int = None,
		tags: str = None,
		tags_remove: str = None,
		patch_panel_model_id: int = None,
		patch_panel_model: str = None,
		numbering_start_from: int = None,
		patch_panel_module_model_id: int = None,
		patch_panel_module_model: str = None,
		module_host_id: int = None,
		module_host: str = None,
		slot_no: int = None,
		width_ratio: str = None,
	) -> dict:
		"""
		PUT /api/1.0/assets/
		Modify assets by asset_id or asset name.
		"""
		if asset_id is None and asset is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either asset_id or asset is required for asset modify.")
			raise ValueError("Either asset_id or asset is required for asset modify.")

		data = self._build_asset_payload(
			name=name,
			asset=asset,
			asset_type=asset_type,
			service_level=service_level,
			back_connection_type=back_connection_type,
			tap_module_model_id=tap_module_model_id,
			tap_module_model=tap_module_model,
			tap_module_host_id=tap_module_host_id,
			tap_module_host=tap_module_host,
			object_category=object_category,
			new_object_category=new_object_category,
			storage_room=storage_room,
			in_service=in_service,
			device_ids=device_ids,
			device_name=device_name,
			reversed=reversed,
			building=building,
			serial_no=serial_no,
			asset_no=asset_no,
			customer=customer,
			storage_room_id=storage_room_id,
			location=location,
			notes=notes,
			vendor=vendor,
			imgfile_id=imgfile_id,
			img=img,
			back_image_id=back_image_id,
			back_image=back_image,
			rack=rack,
			rack_id=rack_id,
			start_at=start_at,
			size=size,
			orientation=orientation,
			where=where,
			x_pos=x_pos,
			depth=depth,
			device_id=device_id,
			tags=tags,
			tags_remove=tags_remove,
			patch_panel_model_id=patch_panel_model_id,
			patch_panel_model=patch_panel_model,
			numbering_start_from=numbering_start_from,
			patch_panel_module_model_id=patch_panel_module_model_id,
			patch_panel_module_model=patch_panel_module_model,
			module_host_id=module_host_id,
			module_host=module_host,
			slot_no=slot_no,
			width_ratio=width_ratio,
		)

		if asset_id is not None:
			data["asset_id"] = int(asset_id)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/assets/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_put_asset_by_id(
		self,
		asset_id: int,
		name: str = None,
		asset_type: str = None,
		service_level: str = None,
		back_connection_type: str = None,
		tap_module_model_id: int = None,
		tap_module_model: str = None,
		tap_module_host_id: int = None,
		tap_module_host: str = None,
		object_category: str = None,
		new_object_category: str = None,
		storage_room: str = None,
		in_service: str = None,
		device_ids: str = None,
		device_name: str = None,
		reversed: str = None,
		building: str = None,
		serial_no: str = None,
		asset_no: str = None,
		customer: str = None,
		storage_room_id: int = None,
		location: str = None,
		notes: str = None,
		vendor: str = None,
		imgfile_id: int = None,
		img: str = None,
		back_image_id: int = None,
		back_image: str = None,
		rack: str = None,
		rack_id: int = None,
		start_at: str = None,
		size: int = None,
		orientation: str = None,
		where: str = None,
		x_pos: int = None,
		depth: str = None,
		device_id: int = None,
		tags: str = None,
		tags_remove: str = None,
		patch_panel_model_id: int = None,
		patch_panel_model: str = None,
		numbering_start_from: int = None,
		patch_panel_module_model_id: int = None,
		patch_panel_module_model: str = None,
		module_host_id: int = None,
		module_host: str = None,
		slot_no: int = None,
		width_ratio: str = None,
		category: str = None,
	) -> dict:
		"""
		PUT /api/1.0/assets/{id}/
		Modify a specific asset by ID.
		"""
		resolved_asset_id = int(asset_id)
		data = self._build_asset_payload(
			name=name,
			asset_type=asset_type,
			service_level=service_level,
			back_connection_type=back_connection_type,
			tap_module_model_id=tap_module_model_id,
			tap_module_model=tap_module_model,
			tap_module_host_id=tap_module_host_id,
			tap_module_host=tap_module_host,
			object_category=object_category,
			new_object_category=new_object_category,
			storage_room=storage_room,
			in_service=in_service,
			device_ids=device_ids,
			device_name=device_name,
			reversed=reversed,
			building=building,
			serial_no=serial_no,
			asset_no=asset_no,
			customer=customer,
			storage_room_id=storage_room_id,
			location=location,
			notes=notes,
			vendor=vendor,
			imgfile_id=imgfile_id,
			img=img,
			back_image_id=back_image_id,
			back_image=back_image,
			rack=rack,
			rack_id=rack_id,
			start_at=start_at,
			size=size,
			orientation=orientation,
			where=where,
			x_pos=x_pos,
			depth=depth,
			device_id=device_id,
			tags=tags,
			tags_remove=tags_remove,
			patch_panel_model_id=patch_panel_model_id,
			patch_panel_model=patch_panel_model,
			numbering_start_from=numbering_start_from,
			patch_panel_module_model_id=patch_panel_module_model_id,
			patch_panel_module_model=patch_panel_module_model,
			module_host_id=module_host_id,
			module_host=module_host,
			slot_no=slot_no,
			width_ratio=width_ratio,
			category=category,
		)

		payload = urlencode(data)
		return self.auth.request(
			f"/api/1.0/assets/{resolved_asset_id}/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_asset(self, asset_id: int) -> dict:
		"""
		DELETE /api/1.0/assets/{id}/
		Delete an asset by ID.
		"""
		resolved_asset_id = int(asset_id)
		return self.auth.request(f"/api/1.0/assets/{resolved_asset_id}/", method="DELETE")

	def d42_put_custom_field_asset(
		self,
		key: str,
		asset_id: int = None,
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
		notes: str = None,
		clear_notes: str = None,
		bulk_fields: str = None,
		multi_select: str = None,
	) -> dict:
		"""
		PUT /api/1.0/custom_fields/asset/
		Set custom fields for assets.
		Requires key and one of asset_id/name.
		"""
		if asset_id is None and name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either asset_id or name is required for asset custom field update.")
			raise ValueError("Either asset_id or name is required for asset custom field update.")

		data = {"key": key}

		if asset_id is not None:
			data["id"] = int(asset_id)
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
			"/api/1.0/custom_fields/asset/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)
