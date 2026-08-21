from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_certificates:
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

	def d42_get_certificates(self, certificate_id: str = None) -> dict:
		"""
		GET /api/1.0/certificates/
		Return certificates added or discovered in Device42.
		"""
		params = {}

		if certificate_id is not None:
			params["certificate_id"] = certificate_id

		endpoint = "/api/1.0/certificates/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def _build_certificate_payload(
		self,
		id: str = None,
		dns: str = None,
		issued_to: str = None,
		issued_by: str = None,
		valid_from: str = None,
		valid_to: str = None,
		subject: str = None,
		version: str = None,
		serial_number: str = None,
		signature_algorithm: str = None,
		signature_hash: str = None,
		san: str = None,
		digital_signature_usage: str = None,
		content_commitment_usage: str = None,
		key_encipherment_usage: str = None,
		data_encipherment_usage: str = None,
		key_agreement_usage: str = None,
		key_cert_sign_usage: str = None,
		crl_sign_usage: str = None,
		encipher_only_usage: str = None,
		decipher_only_usage: str = None,
		extended_key_usage: str = None,
		vendor: str = None,
		end_point_type: str = None,
		end_point_id: str = None,
		groups: str = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		data = {}

		if id is not None:
			data["id"] = id
		if dns is not None:
			data["dns"] = dns
		if issued_to is not None:
			data["issued_to"] = issued_to
		if issued_by is not None:
			data["issued_by"] = issued_by
		if valid_from is not None:
			data["valid_from"] = valid_from
		if valid_to is not None:
			data["valid_to"] = valid_to
		if subject is not None:
			data["subject"] = subject
		if version is not None:
			data["version"] = version
		if serial_number is not None:
			data["serial_number"] = serial_number
		if signature_algorithm is not None:
			data["signature_algorithm"] = signature_algorithm
		if signature_hash is not None:
			data["signature_hash"] = signature_hash
		if san is not None:
			data["san"] = san
		if digital_signature_usage is not None:
			data["digital_signature_usage"] = digital_signature_usage
		if content_commitment_usage is not None:
			data["content_commitment_usage"] = content_commitment_usage
		if key_encipherment_usage is not None:
			data["key_encipherment_usage"] = key_encipherment_usage
		if data_encipherment_usage is not None:
			data["data_encipherment_usage"] = data_encipherment_usage
		if key_agreement_usage is not None:
			data["key_agreement_usage"] = key_agreement_usage
		if key_cert_sign_usage is not None:
			data["key_cert_sign_usage"] = key_cert_sign_usage
		if crl_sign_usage is not None:
			data["crl_sign_usage"] = crl_sign_usage
		if encipher_only_usage is not None:
			data["encipher_only_usage"] = encipher_only_usage
		if decipher_only_usage is not None:
			data["decipher_only_usage"] = decipher_only_usage
		if extended_key_usage is not None:
			data["extended_key_usage"] = extended_key_usage
		if vendor is not None:
			data["vendor"] = vendor
		if end_point_type is not None:
			data["end_point_type"] = end_point_type
		if end_point_id is not None:
			data["end_point_id"] = end_point_id
		if groups is not None:
			data["groups"] = groups
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove

		return data

	def d42_post_certificates(
		self,
		id: str = None,
		dns: str = None,
		issued_to: str = None,
		issued_by: str = None,
		valid_from: str = None,
		valid_to: str = None,
		subject: str = None,
		version: str = None,
		serial_number: str = None,
		signature_algorithm: str = None,
		signature_hash: str = None,
		san: str = None,
		digital_signature_usage: str = None,
		content_commitment_usage: str = None,
		key_encipherment_usage: str = None,
		data_encipherment_usage: str = None,
		key_agreement_usage: str = None,
		key_cert_sign_usage: str = None,
		crl_sign_usage: str = None,
		encipher_only_usage: str = None,
		decipher_only_usage: str = None,
		extended_key_usage: str = None,
		vendor: str = None,
		end_point_type: str = None,
		end_point_id: str = None,
		groups: str = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		"""
		POST /api/1.0/certificates/
		Create or update a certificate.
		If dns is provided it is the only required field; otherwise valid_from and valid_to are required.
		"""
		data = self._build_certificate_payload(
			id=id,
			dns=dns,
			issued_to=issued_to,
			issued_by=issued_by,
			valid_from=valid_from,
			valid_to=valid_to,
			subject=subject,
			version=version,
			serial_number=serial_number,
			signature_algorithm=signature_algorithm,
			signature_hash=signature_hash,
			san=san,
			digital_signature_usage=digital_signature_usage,
			content_commitment_usage=content_commitment_usage,
			key_encipherment_usage=key_encipherment_usage,
			data_encipherment_usage=data_encipherment_usage,
			key_agreement_usage=key_agreement_usage,
			key_cert_sign_usage=key_cert_sign_usage,
			crl_sign_usage=crl_sign_usage,
			encipher_only_usage=encipher_only_usage,
			decipher_only_usage=decipher_only_usage,
			extended_key_usage=extended_key_usage,
			vendor=vendor,
			end_point_type=end_point_type,
			end_point_id=end_point_id,
			groups=groups,
			tags=tags,
			tags_remove=tags_remove,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/certificates/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_certificate(self, certificate_id: int) -> dict:
		"""
		DELETE /api/1.0/certificates/{ID}/
		Delete a certificate by ID.
		"""
		resolved_id = int(certificate_id)
		return self.auth.request(f"/api/1.0/certificates/{resolved_id}/", method="DELETE")

	def d42_put_custom_field_certificate(
		self,
		key: str,
		certificate_id: int = None,
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
		PUT /api/1.0/custom_fields/certificate/
		Set custom fields for certificates.
		Requires key and one of certificate_id/name.
		"""
		if certificate_id is None and name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either certificate_id or name is required for certificate custom field update.")
			raise ValueError("Either certificate_id or name is required for certificate custom field update.")

		data = {"key": key}

		if certificate_id is not None:
			data["id"] = int(certificate_id)
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
			"/api/1.0/custom_fields/certificate/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)
