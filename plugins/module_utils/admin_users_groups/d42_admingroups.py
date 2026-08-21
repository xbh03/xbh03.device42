from urllib.parse import urlencode

from .d42_token_authentication import d42_token_authentication


class d42_admingroups:
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

	def d42_get_admingroups(self, include_cols: str = None) -> dict:
		"""
		GET /api/1.0/admingroups/
		Get all admin groups.

		Returns a payload like:
		{
		  "admingroups": [
		    {
		      "id": 6,
		      "members": ["User1", "User2"],
		      "name": "System Generated Read, Add and Edit"
		    }
		  ],
		  "total_count": 1,
		  "limit": 1000,
		  "offset": 0
		}
		"""
		params = {}

		if include_cols is not None:
			params["include_cols"] = include_cols

		endpoint = "/api/1.0/admingroups/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_post_admingroups(
		self,
		group_id: int = None,
		name: str = None,
		members: str = None,
		members_remove: str = None,
		permissions: str = None,
		permissions_remove: str = None,
	) -> dict:
		"""
		POST /api/1.0/admingroups/
		Create/update admin groups.
		"""
		if group_id is None and name is None:
			if self.module and hasattr(self.module, "fail_json"):
				self.module.fail_json(msg="Either group_id or name is required for admin group create/update.")
			raise ValueError("Either group_id or name is required for admin group create/update.")

		data = {}

		if group_id is not None:
			data["id"] = int(group_id)
		if name is not None:
			data["name"] = name
		if members is not None:
			data["members"] = members
		if members_remove is not None:
			data["members_remove"] = members_remove
		if permissions is not None:
			data["permissions"] = permissions
		if permissions_remove is not None:
			data["permissions_remove"] = permissions_remove

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/admingroups/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_admingroup(self, group_id: int) -> dict:
		"""
		DELETE /api/1.0/admingroups/{id}/
		Delete an admin group by ID.
		"""
		resolved_group_id = int(group_id)
		return self.auth.request(f"/api/1.0/admingroups/{resolved_group_id}/", method="DELETE")
