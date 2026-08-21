from urllib.parse import urlencode

from ...admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_ipam_dns:
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

	def d42_get_dns_zones(
		self,
		cloud_infra_id: int = None,
		domain: str = None,
		dns_zone_id: int = None,
		nameserver: str = None,
		tags: str = None,
		tags_and: str = None,
		include_cols: str = None,
		custom_fields_and: str = None,
		custom_fields_or: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/1.0/dns/zones/
		Retrieve DNS zones.
		"""
		params = {}

		if cloud_infra_id is not None:
			params["cloud_infra_id"] = int(cloud_infra_id)
		if domain is not None:
			params["domain"] = domain
		if dns_zone_id is not None:
			params["id"] = int(dns_zone_id)
		if nameserver is not None:
			params["nameserver"] = nameserver
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if include_cols is not None:
			params["include_cols"] = include_cols
		if custom_fields_and is not None:
			params["custom_fields_and"] = custom_fields_and
		if custom_fields_or is not None:
			params["custom_fields_or"] = custom_fields_or
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/1.0/dns/zones/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def _build_dns_zone_payload(
		self,
		name: str,
		nameserver: str,
		notes: str = None,
		vrf_group: str = None,
		vrf_group_id: int = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		data = {
			"name": name,
			"nameserver": nameserver,
		}

		if notes is not None:
			data["notes"] = notes
		if vrf_group is not None:
			data["vrf_group"] = vrf_group
		if vrf_group_id is not None:
			data["vrf_group_id"] = int(vrf_group_id)
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove

		return data

	def d42_post_dns_zones(
		self,
		name: str,
		nameserver: str,
		notes: str = None,
		vrf_group: str = None,
		vrf_group_id: int = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		"""
		POST /api/1.0/dns/zones/
		Create/update DNS zone.
		"""
		data = self._build_dns_zone_payload(
			name=name,
			nameserver=nameserver,
			notes=notes,
			vrf_group=vrf_group,
			vrf_group_id=vrf_group_id,
			tags=tags,
			tags_remove=tags_remove,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/dns/zones/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_dns_zone(self, id: int) -> dict:
		"""
		DELETE /api/1.0/dns/zones/{id}/
		Delete DNS zone by ID.
		"""
		resolved_id = int(id)
		return self.auth.request(f"/api/1.0/dns/zones/{resolved_id}/", method="DELETE")

	def d42_get_dns_records(
		self,
		domain: str = None,
		record_type: str = None,
		content_contains: str = None,
		name: str = None,
		nameserver: str = None,
		content: str = None,
		tags: str = None,
		tags_and: str = None,
		dns_zone: str = None,
		ttl: str = None,
		change_date: str = None,
		limit: int = None,
		offset: int = None,
	) -> dict:
		"""
		GET /api/1.0/dns/records/
		Retrieve DNS records.
		"""
		params = {}

		if domain is not None:
			params["domain"] = domain
		if record_type is not None:
			params["type"] = record_type
		if content_contains is not None:
			params["content_contains"] = content_contains
		if name is not None:
			params["name"] = name
		if nameserver is not None:
			params["nameserver"] = nameserver
		if content is not None:
			params["content"] = content
		if tags is not None:
			params["tags"] = tags
		if tags_and is not None:
			params["tags_and"] = tags_and
		if dns_zone is not None:
			params["dns_zone"] = dns_zone
		if ttl is not None:
			params["ttl"] = ttl
		if change_date is not None:
			params["change_date"] = change_date
		if limit is not None:
			params["limit"] = int(limit)
		if offset is not None:
			params["offset"] = int(offset)

		endpoint = "/api/1.0/dns/records/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def _build_dns_record_payload(
		self,
		domain: str,
		record_type: str,
		nameserver: str = None,
		name: str = None,
		content: str = None,
		content_raw: str = None,
		new_content: str = None,
		new_content_raw: str = None,
		prio: str = None,
		ttl: str = None,
		tags: str = None,
		tags_remove: str = None,
		change_date: int = None,
	) -> dict:
		data = {
			"domain": domain,
			"type": record_type,
		}

		if nameserver is not None:
			data["nameserver"] = nameserver
		if name is not None:
			data["name"] = name
		if content is not None:
			data["content"] = content
		if content_raw is not None:
			data["content_raw"] = content_raw
		if new_content is not None:
			data["new_content"] = new_content
		if new_content_raw is not None:
			data["new_content_raw"] = new_content_raw
		if prio is not None:
			data["prio"] = prio
		if ttl is not None:
			data["ttl"] = ttl
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove
		if change_date is not None:
			data["change_date"] = int(change_date)

		return data

	def d42_post_dns_records(
		self,
		domain: str,
		record_type: str,
		nameserver: str = None,
		name: str = None,
		content: str = None,
		content_raw: str = None,
		new_content: str = None,
		new_content_raw: str = None,
		prio: str = None,
		ttl: str = None,
		tags: str = None,
		tags_remove: str = None,
		change_date: int = None,
	) -> dict:
		"""
		POST /api/1.0/dns/records/
		Create/update DNS record.
		"""
		data = self._build_dns_record_payload(
			domain=domain,
			record_type=record_type,
			nameserver=nameserver,
			name=name,
			content=content,
			content_raw=content_raw,
			new_content=new_content,
			new_content_raw=new_content_raw,
			prio=prio,
			ttl=ttl,
			tags=tags,
			tags_remove=tags_remove,
			change_date=change_date,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/dns/records/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_dns_record(self, id: int) -> dict:
		"""
		DELETE /api/1.0/dns/records/{id}/
		Delete DNS record by ID.
		"""
		resolved_id = int(id)
		return self.auth.request(f"/api/1.0/dns/records/{resolved_id}/", method="DELETE")
