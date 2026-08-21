from urllib.parse import urlencode

from ...admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_ipam_switches:
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

	def _build_switch_payload(
		self,
		switch_template_id: str,
		device: str = None,
		device_id: str = None,
		devices: str = None,
		device_ids: str = None,
		assets: str = None,
		asset_ids: str = None,
	) -> dict:
		data = {"switch_template_id": switch_template_id}

		if device is not None:
			data["device"] = device
		if device_id is not None:
			data["device_id"] = device_id
		if devices is not None:
			data["devices"] = devices
		if device_ids is not None:
			data["device_ids"] = device_ids
		if assets is not None:
			data["assets"] = assets
		if asset_ids is not None:
			data["asset_ids"] = asset_ids

		return data

	def d42_post_switches(
		self,
		switch_template_id: str,
		device: str = None,
		device_id: str = None,
		devices: str = None,
		device_ids: str = None,
		assets: str = None,
		asset_ids: str = None,
	) -> dict:
		"""
		POST /api/1.0/switches/
		Add switch/switch ports using switch template.
		"""
		if switch_template_id is None:
			self.module.fail_json(msg="switch_template_id is required.")

		if device is None and device_id is None:
			self.module.fail_json(msg="Either device or device_id is required.")

		data = self._build_switch_payload(
			switch_template_id=switch_template_id,
			device=device,
			device_id=device_id,
			devices=devices,
			device_ids=device_ids,
			assets=assets,
			asset_ids=asset_ids,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/switches/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)
