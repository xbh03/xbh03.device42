from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_devices:
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

	def d42_get_devices(
		self,
		include_cols: str = None,
		device_id: int = None,
		name: str = None,
		serial_no: str = None,
		serial_no_contains: str = None,
		asset_no: str = None,
		asset_no_contains: str = None,
		uuid: str = None,
		in_service: str = None,
		service_level: str = None,
		service_level_id: int = None,
		device_type: str = None,
		type_id: int = None,
		last_edited_lt: str = None,
		last_edited_gt: str = None,
		first_added_lt: str = None,
		first_added_gt: str = None,
		objectcategory_id: int = None,
		objectcategory: str = None,
		tags: str = None,
		tags_and: str = None,
		cluster_device_id: int = None,
		customer_id: int = None,
		customer: str = None,
		hardware_id: int = None,
		hardware: str = None,
		device_host_chassis_id: int = None,
		device_virtual_host_id: int = None,
		rack_id: int = None,
		virtualsubtype: str = None,
		virtualsubtype_id: int = None,
		os_id: int = None,
		os_name: str = None,
		custom_fields_and: str = None,
		custom_fields_or: str = None,
		virtual_host: str = None,
		blade_chassis: str = None,
		physicalsubtype: str = None,
		physicalsubtype_id: int = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/2.0/devices/
		Retrieve information about all devices (v2).
		"""
		params = {}

		if include_cols is not None:
			params["include_cols"] = include_cols
		if device_id is not None:
			params["device_id"] = int(device_id)
		if name is not None:
			params["name"] = name
		if serial_no is not None:
			params["serial_no"] = serial_no
		if serial_no_contains is not None:
			params["serial_no_contains"] = serial_no_contains
		if asset_no is not None:
			params["asset_no"] = asset_no
		if asset_no_contains is not None:
			params["asset_no_contains"] = asset_no_contains
		if uuid is not None:
			params["uuid"] = uuid
		if in_service is not None:
			params["in_service"] = in_service
		if service_level is not None:
			params["service_level"] = service_level
		if service_level_id is not None:
			params["service_level_id"] = int(service_level_id)
		if device_type is not None:
			params["type"] = device_type
		if type_id is not None:
			params["type_id"] = int(type_id)
		if last_edited_lt is not None:
			params["last_edited_lt"] = last_edited_lt
		if last_edited_gt is not None:
			params["last_edited_gt"] = last_edited_gt
		if first_added_lt is not None:
			params["first_added_lt"] = first_added_lt
		if first_added_gt is not None:
			params["first_added_gt"] = first_added_gt
		if objectcategory_id is not None:
			params["objectcategory_id"] = int(objectcategory_id)
		if objectcategory is not None:
			params["objectcategory"] = objectcategory
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if cluster_device_id is not None:
			params["cluster_device_id"] = int(cluster_device_id)
		if customer_id is not None:
			params["customer_id"] = int(customer_id)
		if customer is not None:
			params["customer"] = customer
		if hardware_id is not None:
			params["hardware_id"] = int(hardware_id)
		if hardware is not None:
			params["hardware"] = hardware
		if device_host_chassis_id is not None:
			params["device_host_chassis_id"] = int(device_host_chassis_id)
		if device_virtual_host_id is not None:
			params["device_virtual_host_id"] = int(device_virtual_host_id)
		if rack_id is not None:
			params["rack_id"] = int(rack_id)
		if virtualsubtype is not None:
			params["virtualsubtype"] = virtualsubtype
		if virtualsubtype_id is not None:
			params["virtualsubtype_id"] = int(virtualsubtype_id)
		if os_id is not None:
			params["os_id"] = int(os_id)
		if os_name is not None:
			params["os_name"] = os_name
		if custom_fields_and is not None:
			params["custom_fields_and"] = custom_fields_and
		if custom_fields_or is not None:
			params["custom_fields_or"] = custom_fields_or
		if virtual_host is not None:
			params["virtual_host"] = virtual_host
		if blade_chassis is not None:
			params["blade_chassis"] = blade_chassis
		if physicalsubtype is not None:
			params["physicalsubtype"] = physicalsubtype
		if physicalsubtype_id is not None:
			params["physicalsubtype_id"] = int(physicalsubtype_id)
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/2.0/devices/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def _build_device_payload(
		self,
		device_id: int = None,
		serial_no: str = None,
		name: str = None,
		asset_no: str = None,
		uuid: str = None,
		virtual_host: str = None,
		in_service: str = None,
		device_type_id: int = None,
		device_type: str = None,
		physicalsubtype_id: int = None,
		physicalsubtype: str = None,
		network_device: str = None,
		blade_chassis: str = None,
		manufacturer: str = None,
		hardware_id: int = None,
		hardware: str = None,
		new_hardware: str = None,
		virtual_host_device_id: int = None,
		virtual_host_device: str = None,
		host_chassis_device_id: int = None,
		host_chassis_device: str = None,
		bladeno: int = None,
		chassisslot_id: int = None,
		service_level_id: int = None,
		service_level: str = None,
		customer_id: int = None,
		customer: str = None,
		customers: str = None,
		customers_remove: str = None,
		additional_location: str = None,
		building_id: int = None,
		building: str = None,
		storage_room: str = None,
		storage_room_id: int = None,
		notes: str = None,
		objectcategory_id: int = None,
		objectcategory: str = None,
		dont_inherit: str = None,
		virtualsubtype_id: int = None,
		virtualsubtype: str = None,
		datacenter: str = None,
		ram_size: str = None,
		ram_size_type_id: int = None,
		ram_size_type: str = None,
		total_cpus: int = None,
		core_per_cpu: int = None,
		threads_per_core: int = None,
		cpu_speed: str = None,
		hz_id: int = None,
		hz: str = None,
		hard_disk_count: int = None,
		hard_disk_size: str = None,
		hard_disk_size_type_id: int = None,
		hard_disk_size_type: str = None,
		hw_sw_raid_id: int = None,
		hw_sw_raid: str = None,
		raid_type_id: int = None,
		raid_type: str = None,
		devices_in_clusters_ids: str = None,
		nonauthoritativealiases: str = None,
		nonauthoritativealiases_remove: str = None,
		aliases: str = None,
		aliases_remove: str = None,
		tags: str = None,
		tags_remove: str = None,
		bios_version: str = None,
		bios_release_date: str = None,
		bios_revision: str = None,
		bios_fw_revision: str = None,
		bios_vendor: str = None,
	) -> dict:
		data = {}

		if device_id is not None:
			data["device_id"] = int(device_id)
		if serial_no is not None:
			data["serial_no"] = serial_no
		if name is not None:
			data["name"] = name
		if asset_no is not None:
			data["asset_no"] = asset_no
		if uuid is not None:
			data["uuid"] = uuid
		if virtual_host is not None:
			data["virtual_host"] = virtual_host
		if in_service is not None:
			data["in_service"] = in_service
		if device_type_id is not None:
			data["type_id"] = int(device_type_id)
		if device_type is not None:
			data["type"] = device_type
		if physicalsubtype_id is not None:
			data["physicalsubtype_id"] = int(physicalsubtype_id)
		if physicalsubtype is not None:
			data["physicalsubtype"] = physicalsubtype
		if network_device is not None:
			data["network_device"] = network_device
		if blade_chassis is not None:
			data["blade_chassis"] = blade_chassis
		if manufacturer is not None:
			data["manufacturer"] = manufacturer
		if hardware_id is not None:
			data["hardware_id"] = int(hardware_id)
		if hardware is not None:
			data["hardware"] = hardware
		if new_hardware is not None:
			data["new_hardware"] = new_hardware
		if virtual_host_device_id is not None:
			data["virtual_host_device_id"] = int(virtual_host_device_id)
		if virtual_host_device is not None:
			data["virtual_host_device"] = virtual_host_device
		if host_chassis_device_id is not None:
			data["host_chassis_device_id"] = int(host_chassis_device_id)
		if host_chassis_device is not None:
			data["host_chassis_device"] = host_chassis_device
		if bladeno is not None:
			data["bladeno"] = int(bladeno)
		if chassisslot_id is not None:
			data["chassisslot_id"] = int(chassisslot_id)
		if service_level_id is not None:
			data["service_level_id"] = int(service_level_id)
		if service_level is not None:
			data["service_level"] = service_level
		if customer_id is not None:
			data["customer_id"] = int(customer_id)
		if customer is not None:
			data["customer"] = customer
		if customers is not None:
			data["customers"] = customers
		if customers_remove is not None:
			data["customers_remove"] = customers_remove
		if additional_location is not None:
			data["additional_location"] = additional_location
		if building_id is not None:
			data["building_id"] = int(building_id)
		if building is not None:
			data["building"] = building
		if storage_room is not None:
			data["storage_room"] = storage_room
		if storage_room_id is not None:
			data["storage_room_id"] = int(storage_room_id)
		if notes is not None:
			data["notes"] = notes
		if objectcategory_id is not None:
			data["objectcategory_id"] = int(objectcategory_id)
		if objectcategory is not None:
			data["objectcategory"] = objectcategory
		if dont_inherit is not None:
			data["dont_inherit"] = dont_inherit
		if virtualsubtype_id is not None:
			data["virtualsubtype_id"] = int(virtualsubtype_id)
		if virtualsubtype is not None:
			data["virtualsubtype"] = virtualsubtype
		if datacenter is not None:
			data["datacenter"] = datacenter
		if ram_size is not None:
			data["ram_size"] = ram_size
		if ram_size_type_id is not None:
			data["ram_size_type_id"] = int(ram_size_type_id)
		if ram_size_type is not None:
			data["ram_size_type"] = ram_size_type
		if total_cpus is not None:
			data["total_cpus"] = int(total_cpus)
		if core_per_cpu is not None:
			data["core_per_cpu"] = int(core_per_cpu)
		if threads_per_core is not None:
			data["threads_per_core"] = int(threads_per_core)
		if cpu_speed is not None:
			data["cpu_speed"] = cpu_speed
		if hz_id is not None:
			data["hz_id"] = int(hz_id)
		if hz is not None:
			data["hz"] = hz
		if hard_disk_count is not None:
			data["hard_disk_count"] = int(hard_disk_count)
		if hard_disk_size is not None:
			data["hard_disk_size"] = hard_disk_size
		if hard_disk_size_type_id is not None:
			data["hard_disk_size_type_id"] = int(hard_disk_size_type_id)
		if hard_disk_size_type is not None:
			data["hard_disk_size_type"] = hard_disk_size_type
		if hw_sw_raid_id is not None:
			data["hw_sw_raid_id"] = int(hw_sw_raid_id)
		if hw_sw_raid is not None:
			data["hw_sw_raid"] = hw_sw_raid
		if raid_type_id is not None:
			data["raid_type_id"] = int(raid_type_id)
		if raid_type is not None:
			data["raid_type"] = raid_type
		if devices_in_clusters_ids is not None:
			data["devices_in_clusters_ids"] = devices_in_clusters_ids
		if nonauthoritativealiases is not None:
			data["nonauthoritativealiases"] = nonauthoritativealiases
		if nonauthoritativealiases_remove is not None:
			data["nonauthoritativealiases_remove"] = nonauthoritativealiases_remove
		if aliases is not None:
			data["aliases"] = aliases
		if aliases_remove is not None:
			data["aliases_remove"] = aliases_remove
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if bios_version is not None:
			data["bios_version"] = bios_version
		if bios_release_date is not None:
			data["bios_release_date"] = bios_release_date
		if bios_revision is not None:
			data["bios_revision"] = bios_revision
		if bios_fw_revision is not None:
			data["bios_fw_revision"] = bios_fw_revision
		if bios_vendor is not None:
			data["bios_vendor"] = bios_vendor

		return data

	def d42_post_devices(
		self,
		device_id: int = None,
		serial_no: str = None,
		name: str = None,
		asset_no: str = None,
		uuid: str = None,
		virtual_host: str = None,
		in_service: str = None,
		device_type_id: int = None,
		device_type: str = None,
		physicalsubtype_id: int = None,
		physicalsubtype: str = None,
		network_device: str = None,
		blade_chassis: str = None,
		manufacturer: str = None,
		hardware_id: int = None,
		hardware: str = None,
		new_hardware: str = None,
		virtual_host_device_id: int = None,
		virtual_host_device: str = None,
		host_chassis_device_id: int = None,
		host_chassis_device: str = None,
		bladeno: int = None,
		chassisslot_id: int = None,
		service_level_id: int = None,
		service_level: str = None,
		customer_id: int = None,
		customer: str = None,
		customers: str = None,
		customers_remove: str = None,
		additional_location: str = None,
		building_id: int = None,
		building: str = None,
		storage_room: str = None,
		storage_room_id: int = None,
		notes: str = None,
		objectcategory_id: int = None,
		objectcategory: str = None,
		dont_inherit: str = None,
		virtualsubtype_id: int = None,
		virtualsubtype: str = None,
		datacenter: str = None,
		ram_size: str = None,
		ram_size_type_id: int = None,
		ram_size_type: str = None,
		total_cpus: int = None,
		core_per_cpu: int = None,
		threads_per_core: int = None,
		cpu_speed: str = None,
		hz_id: int = None,
		hz: str = None,
		hard_disk_count: int = None,
		hard_disk_size: str = None,
		hard_disk_size_type_id: int = None,
		hard_disk_size_type: str = None,
		hw_sw_raid_id: int = None,
		hw_sw_raid: str = None,
		raid_type_id: int = None,
		raid_type: str = None,
		devices_in_clusters_ids: str = None,
		nonauthoritativealiases: str = None,
		nonauthoritativealiases_remove: str = None,
		aliases: str = None,
		aliases_remove: str = None,
		tags: str = None,
		tags_remove: str = None,
		bios_version: str = None,
		bios_release_date: str = None,
		bios_revision: str = None,
		bios_fw_revision: str = None,
		bios_vendor: str = None,
	) -> dict:
		"""
		POST /api/2.0/devices/
		Create or update a device.
		"""
		data = self._build_device_payload(
			device_id=device_id,
			serial_no=serial_no,
			name=name,
			asset_no=asset_no,
			uuid=uuid,
			virtual_host=virtual_host,
			in_service=in_service,
			device_type_id=device_type_id,
			device_type=device_type,
			physicalsubtype_id=physicalsubtype_id,
			physicalsubtype=physicalsubtype,
			network_device=network_device,
			blade_chassis=blade_chassis,
			manufacturer=manufacturer,
			hardware_id=hardware_id,
			hardware=hardware,
			new_hardware=new_hardware,
			virtual_host_device_id=virtual_host_device_id,
			virtual_host_device=virtual_host_device,
			host_chassis_device_id=host_chassis_device_id,
			host_chassis_device=host_chassis_device,
			bladeno=bladeno,
			chassisslot_id=chassisslot_id,
			service_level_id=service_level_id,
			service_level=service_level,
			customer_id=customer_id,
			customer=customer,
			customers=customers,
			customers_remove=customers_remove,
			additional_location=additional_location,
			building_id=building_id,
			building=building,
			storage_room=storage_room,
			storage_room_id=storage_room_id,
			notes=notes,
			objectcategory_id=objectcategory_id,
			objectcategory=objectcategory,
			dont_inherit=dont_inherit,
			virtualsubtype_id=virtualsubtype_id,
			virtualsubtype=virtualsubtype,
			datacenter=datacenter,
			ram_size=ram_size,
			ram_size_type_id=ram_size_type_id,
			ram_size_type=ram_size_type,
			total_cpus=total_cpus,
			core_per_cpu=core_per_cpu,
			threads_per_core=threads_per_core,
			cpu_speed=cpu_speed,
			hz_id=hz_id,
			hz=hz,
			hard_disk_count=hard_disk_count,
			hard_disk_size=hard_disk_size,
			hard_disk_size_type_id=hard_disk_size_type_id,
			hard_disk_size_type=hard_disk_size_type,
			hw_sw_raid_id=hw_sw_raid_id,
			hw_sw_raid=hw_sw_raid,
			raid_type_id=raid_type_id,
			raid_type=raid_type,
			devices_in_clusters_ids=devices_in_clusters_ids,
			nonauthoritativealiases=nonauthoritativealiases,
			nonauthoritativealiases_remove=nonauthoritativealiases_remove,
			aliases=aliases,
			aliases_remove=aliases_remove,
			tags=tags,
			tags_remove=tags_remove,
			bios_version=bios_version,
			bios_release_date=bios_release_date,
			bios_revision=bios_revision,
			bios_fw_revision=bios_fw_revision,
			bios_vendor=bios_vendor,
		)

		if not data:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="At least one parameter is required for device create/update.")
			raise ValueError("At least one parameter is required for device create/update.")

		payload = urlencode(data)
		return self.auth.request(
			"/api/2.0/devices/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_get_device_by_id(self, device_id: int, include_cols: str = None) -> dict:
		"""
		GET /api/2.0/devices/{id}/
		Retrieve detailed information about a specific device.
		"""
		resolved_device_id = int(device_id)
		endpoint = f"/api/2.0/devices/{resolved_device_id}/"

		if include_cols is not None:
			endpoint = f"{endpoint}?{urlencode({'include_cols': include_cols})}"

		return self.auth.request(endpoint, method="GET")

	def d42_put_device_by_id(
		self,
		device_id: int,
		name: str = None,
		asset_no: str = None,
		uuid: str = None,
		virtual_host: str = None,
		in_service: str = None,
		device_type_id: int = None,
		device_type: str = None,
		physicalsubtype_id: int = None,
		physicalsubtype: str = None,
		network_device: str = None,
		blade_chassis: str = None,
		manufacturer: str = None,
		hardware_id: int = None,
		hardware: str = None,
		new_hardware: str = None,
		virtual_host_device_id: int = None,
		virtual_host_device: str = None,
		host_chassis_device_id: int = None,
		host_chassis_device: str = None,
		bladeno: int = None,
		chassisslot_id: int = None,
		service_level_id: int = None,
		service_level: str = None,
		customer_id: int = None,
		customer: str = None,
		customers: str = None,
		customers_remove: str = None,
		additional_location: str = None,
		building_id: int = None,
		storage_room: str = None,
		storage_room_id: int = None,
		notes: str = None,
		objectcategory_id: int = None,
		objectcategory: str = None,
		dont_inherit: str = None,
		virtualsubtype_id: int = None,
		virtualsubtype: str = None,
		datacenter: str = None,
		ram_size: str = None,
		ram_size_type_id: int = None,
		ram_size_type: str = None,
		total_cpus: int = None,
		core_per_cpu: int = None,
		threads_per_core: int = None,
		cpu_speed: str = None,
		hz_id: int = None,
		hz: str = None,
		hard_disk_count: int = None,
		hard_disk_size: str = None,
		hard_disk_size_type_id: int = None,
		hard_disk_size_type: str = None,
		hw_sw_raid_id: int = None,
		hw_sw_raid: str = None,
		raid_type_id: int = None,
		raid_type: str = None,
		devices_in_clusters_ids: str = None,
		nonauthoritativealiases: str = None,
		nonauthoritativealiases_remove: str = None,
		aliases: str = None,
		aliases_remove: str = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		"""
		PUT /api/2.0/devices/{id}/
		Update a specific device by ID.
		"""
		resolved_device_id = int(device_id)
		data = self._build_device_payload(
			name=name,
			asset_no=asset_no,
			uuid=uuid,
			virtual_host=virtual_host,
			in_service=in_service,
			device_type_id=device_type_id,
			device_type=device_type,
			physicalsubtype_id=physicalsubtype_id,
			physicalsubtype=physicalsubtype,
			network_device=network_device,
			blade_chassis=blade_chassis,
			manufacturer=manufacturer,
			hardware_id=hardware_id,
			hardware=hardware,
			new_hardware=new_hardware,
			virtual_host_device_id=virtual_host_device_id,
			virtual_host_device=virtual_host_device,
			host_chassis_device_id=host_chassis_device_id,
			host_chassis_device=host_chassis_device,
			bladeno=bladeno,
			chassisslot_id=chassisslot_id,
			service_level_id=service_level_id,
			service_level=service_level,
			customer_id=customer_id,
			customer=customer,
			customers=customers,
			customers_remove=customers_remove,
			additional_location=additional_location,
			building_id=building_id,
			storage_room=storage_room,
			storage_room_id=storage_room_id,
			notes=notes,
			objectcategory_id=objectcategory_id,
			objectcategory=objectcategory,
			dont_inherit=dont_inherit,
			virtualsubtype_id=virtualsubtype_id,
			virtualsubtype=virtualsubtype,
			datacenter=datacenter,
			ram_size=ram_size,
			ram_size_type_id=ram_size_type_id,
			ram_size_type=ram_size_type,
			total_cpus=total_cpus,
			core_per_cpu=core_per_cpu,
			threads_per_core=threads_per_core,
			cpu_speed=cpu_speed,
			hz_id=hz_id,
			hz=hz,
			hard_disk_count=hard_disk_count,
			hard_disk_size=hard_disk_size,
			hard_disk_size_type_id=hard_disk_size_type_id,
			hard_disk_size_type=hard_disk_size_type,
			hw_sw_raid_id=hw_sw_raid_id,
			hw_sw_raid=hw_sw_raid,
			raid_type_id=raid_type_id,
			raid_type=raid_type,
			devices_in_clusters_ids=devices_in_clusters_ids,
			nonauthoritativealiases=nonauthoritativealiases,
			nonauthoritativealiases_remove=nonauthoritativealiases_remove,
			aliases=aliases,
			aliases_remove=aliases_remove,
			tags=tags,
			tags_remove=tags_remove,
		)

		if not data:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="At least one update parameter is required for device PUT.")
			raise ValueError("At least one update parameter is required for device PUT.")

		payload = urlencode(data)
		return self.auth.request(
			f"/api/2.0/devices/{resolved_device_id}/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_device(self, device_id: int, delete_vms: str = None) -> dict:
		"""
		DELETE /api/2.0/devices/{id}/
		Delete a device by ID.
		"""
		resolved_device_id = int(device_id)

		data = None
		headers = None
		if delete_vms is not None:
			data = urlencode({"delete_vms": delete_vms})
			headers = {"Content-Type": "application/x-www-form-urlencoded"}

		return self.auth.request(
			f"/api/2.0/devices/{resolved_device_id}/",
			method="DELETE",
			data=data,
			headers=headers,
		)
		
	def d42_put_custom_field_device(
		self,
		key: str,
		device_id: int = None,
		name: str = None,
		asset: str = None,
		serial: str = None,
		type: str = None,
		mandatory: str = None,
		filterable: str = None,
		log_for_api: str = None,
		include_in_context_popups: str = None,
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
		PUT /api/1.0/device/custom_field/
		Set custom fields for devices.
		Requires key and one of device_id/name/asset/serial.
		"""
		if device_id is None and name is None and asset is None and serial is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="One of device_id, name, asset, or serial is required for device custom field update.")
			raise ValueError("One of device_id, name, asset, or serial is required for device custom field update.")

		data = {"key": key}

		if device_id is not None:
			data["device_id"] = int(device_id)
		if name is not None:
			data["name"] = name
		if asset is not None:
			data["asset"] = asset
		if serial is not None:
			data["serial"] = serial
		if type is not None:
			data["type"] = type
		if mandatory is not None:
			data["mandatory"] = mandatory
		if filterable is not None:
			data["filterable"] = filterable
		if log_for_api is not None:
			data["log_for_api"] = log_for_api
		if include_in_context_popups is not None:
			data["include_in_context_popups"] = include_in_context_popups
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
			"/api/1.0/device/custom_field/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_get_device_mountpoints(
		self,
		device_id: int = None,
		filesystem: str = None,
		fstype: str = None,
	) -> dict:
		"""
		GET /api/2.0/device/mountpoints/
		Get device mountpoints.
		"""
		params = {}

		if device_id is not None:
			params["device_id"] = int(device_id)
		if filesystem is not None:
			params["filesystem"] = filesystem
		if fstype is not None:
			params["fstype"] = fstype

		endpoint = "/api/2.0/device/mountpoints/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")
