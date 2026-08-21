from urllib.parse import urlencode

from ...admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_ipam_subnets:
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

	def d42_get_subnets(
		self,
		name: str = None,
		vrf_group_id: str = None,
		vrf_group: str = None,
		parent_subnet_id: str = None,
		parent_subnet: str = None,
		customer_id: str = None,
		customer: str = None,
		subnet_id: str = None,
		mask_bits: str = None,
		mask_bits_lt: str = None,
		mask_bits_gt: str = None,
		description: str = None,
		range_begin: str = None,
		range_end: str = None,
		gateway: str = None,
		tags: str = None,
		tags_and: str = None,
		custom_fields_and: str = None,
		custom_fields_or: str = None,
		service_level: str = None,
		category: str = None,
		category_id: str = None,
		vlan_id: str = None,
		network: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/1.0/subnets/
		Get all subnets.
		"""
		params = {}

		if name is not None:
			params["name"] = name
		if vrf_group_id is not None:
			params["vrf_group_id"] = vrf_group_id
		if vrf_group is not None:
			params["vrf_group"] = vrf_group
		if parent_subnet_id is not None:
			params["parent_subnet_id"] = parent_subnet_id
		if parent_subnet is not None:
			params["parent_subnet"] = parent_subnet
		if customer_id is not None:
			params["customer_id"] = customer_id
		if customer is not None:
			params["customer"] = customer
		if subnet_id is not None:
			params["subnet_id"] = subnet_id
		if mask_bits is not None:
			params["mask_bits"] = mask_bits
		if mask_bits_lt is not None:
			params["mask_bits_lt"] = mask_bits_lt
		if mask_bits_gt is not None:
			params["mask_bits_gt"] = mask_bits_gt
		if description is not None:
			params["description"] = description
		if range_begin is not None:
			params["range_begin"] = range_begin
		if range_end is not None:
			params["range_end"] = range_end
		if gateway is not None:
			params["gateway"] = gateway
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if custom_fields_and is not None:
			params["custom_fields_and"] = custom_fields_and
		if custom_fields_or is not None:
			params["custom_fields_or"] = custom_fields_or
		if service_level is not None:
			params["service_level"] = service_level
		if category is not None:
			params["category"] = category
		if category_id is not None:
			params["category_id"] = category_id
		if vlan_id is not None:
			params["vlan_id"] = vlan_id
		if network is not None:
			params["network"] = network
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/1.0/subnets/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_subnet_by_id(self, subnet_id: int) -> dict:
		"""
		GET /api/1.0/subnets/{subnet_id}/
		Get subnet by ID.
		"""
		resolved_subnet_id = int(subnet_id)
		return self.auth.request(f"/api/1.0/subnets/{resolved_subnet_id}/", method="GET")

	def _build_subnet_payload(
		self,
		network: str = None,
		mask_bits: str = None,
		vrf_group_id: int = None,
		vrf_group: str = None,
		name: str = None,
		subnet_type: str = None,
		type_id: int = None,
		service_level: str = None,
		service_level_id: int = None,
		description: str = None,
		gateway: str = None,
		range_begin: str = None,
		range_end: str = None,
		parent_vlan_id: str = None,
		parent_subnet_id: str = None,
		customer_id: str = None,
		notes: str = None,
		assigned: str = None,
		allocated: str = None,
		auto_add_ips: str = None,
		category: str = None,
		new_category: str = None,
		category_id: str = None,
		new_category_id: str = None,
		parent_subnet_name: str = None,
		parent_subnet: str = None,
	) -> dict:
		data = {}

		if network is not None:
			data["network"] = network
		if mask_bits is not None:
			data["mask_bits"] = mask_bits
		if vrf_group_id is not None:
			data["vrf_group_id"] = int(vrf_group_id)
		if vrf_group is not None:
			data["vrf_group"] = vrf_group
		if name is not None:
			data["name"] = name
		if subnet_type is not None:
			data["type"] = subnet_type
		if type_id is not None:
			data["type_id"] = int(type_id)
		if service_level is not None:
			data["service_level"] = service_level
		if service_level_id is not None:
			data["service_level_id"] = int(service_level_id)
		if description is not None:
			data["description"] = description
		if gateway is not None:
			data["gateway"] = gateway
		if range_begin is not None:
			data["range_begin"] = range_begin
		if range_end is not None:
			data["range_end"] = range_end
		if parent_vlan_id is not None:
			data["parent_vlan_id"] = parent_vlan_id
		if parent_subnet_id is not None:
			data["parent_subnet_id"] = parent_subnet_id
		if customer_id is not None:
			data["customer_id"] = customer_id
		if notes is not None:
			data["notes"] = notes
		if assigned is not None:
			data["assigned"] = assigned
		if allocated is not None:
			data["allocated"] = allocated
		if auto_add_ips is not None:
			data["auto_add_ips"] = auto_add_ips
		if category is not None:
			data["category"] = category
		if new_category is not None:
			data["new_category"] = new_category
		if category_id is not None:
			data["category_id"] = category_id
		if new_category_id is not None:
			data["new_category_id"] = new_category_id
		if parent_subnet_name is not None:
			data["parent_subnet_name"] = parent_subnet_name
		if parent_subnet is not None:
			data["parent_subnet"] = parent_subnet

		return data

	def d42_post_subnets(
		self,
		network: str,
		mask_bits: str,
		vrf_group_id: int = None,
		vrf_group: str = None,
		name: str = None,
		subnet_type: str = None,
		type_id: int = None,
		service_level: str = None,
		service_level_id: int = None,
		description: str = None,
		gateway: str = None,
		range_begin: str = None,
		range_end: str = None,
		parent_vlan_id: str = None,
		parent_subnet_id: str = None,
		customer_id: str = None,
		notes: str = None,
		assigned: str = None,
		allocated: str = None,
		auto_add_ips: str = None,
		category: str = None,
		new_category: str = None,
		category_id: str = None,
		new_category_id: str = None,
		parent_subnet_name: str = None,
		parent_subnet: str = None,
	) -> dict:
		"""
		POST /api/1.0/subnets/
		Create or update subnet.
		"""
		data = self._build_subnet_payload(
			network=network,
			mask_bits=mask_bits,
			vrf_group_id=vrf_group_id,
			vrf_group=vrf_group,
			name=name,
			subnet_type=subnet_type,
			type_id=type_id,
			service_level=service_level,
			service_level_id=service_level_id,
			description=description,
			gateway=gateway,
			range_begin=range_begin,
			range_end=range_end,
			parent_vlan_id=parent_vlan_id,
			parent_subnet_id=parent_subnet_id,
			customer_id=customer_id,
			notes=notes,
			assigned=assigned,
			allocated=allocated,
			auto_add_ips=auto_add_ips,
			category=category,
			new_category=new_category,
			category_id=category_id,
			new_category_id=new_category_id,
			parent_subnet_name=parent_subnet_name,
			parent_subnet=parent_subnet,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/subnets/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_put_subnets(
		self,
		id: int,
		vrf_group_id: int = None,
		vrf_group: str = None,
		name: str = None,
		subnet_type: str = None,
		type_id: int = None,
		service_level: str = None,
		service_level_id: int = None,
		description: str = None,
		gateway: str = None,
		range_begin: str = None,
		range_end: str = None,
		parent_vlan_id: str = None,
		parent_subnet_id: str = None,
		customer_id: str = None,
		notes: str = None,
		assigned: str = None,
		allocated: str = None,
		auto_add_ips: str = None,
		category: str = None,
		new_category: str = None,
		category_id: str = None,
		new_category_id: str = None,
		parent_subnet_name: str = None,
		parent_subnet: str = None,
	) -> dict:
		"""
		PUT /api/1.0/subnets/
		Create or update specific subnet.
		"""
		data = self._build_subnet_payload(
			vrf_group_id=vrf_group_id,
			vrf_group=vrf_group,
			name=name,
			subnet_type=subnet_type,
			type_id=type_id,
			service_level=service_level,
			service_level_id=service_level_id,
			description=description,
			gateway=gateway,
			range_begin=range_begin,
			range_end=range_end,
			parent_vlan_id=parent_vlan_id,
			parent_subnet_id=parent_subnet_id,
			customer_id=customer_id,
			notes=notes,
			assigned=assigned,
			allocated=allocated,
			auto_add_ips=auto_add_ips,
			category=category,
			new_category=new_category,
			category_id=category_id,
			new_category_id=new_category_id,
			parent_subnet_name=parent_subnet_name,
			parent_subnet=parent_subnet,
		)
		data["id"] = int(id)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/subnets/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_subnet(self, subnet_id: int, merge_associated: str = None) -> dict:
		"""
		DELETE /api/1.0/subnets/{subnet_id}/
		Delete subnet by ID.
		"""
		resolved_subnet_id = int(subnet_id)
		payload = None
		headers = None

		if merge_associated is not None:
			payload = urlencode({"merge_associated": merge_associated})
			headers = {"Content-Type": "application/x-www-form-urlencoded"}

		return self.auth.request(
			f"/api/1.0/subnets/{resolved_subnet_id}/",
			method="DELETE",
			data=payload,
			headers=headers,
		)
