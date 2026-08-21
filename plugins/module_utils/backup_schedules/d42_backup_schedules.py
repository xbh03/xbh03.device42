from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_backup_schedules:
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
		port: int = 4343,
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

	def d42_get_backup_schedules(self) -> dict:
		"""
		GET /api/1.0/backup_schedules/
		Get backup schedules.
		"""
		return self.auth.request("/api/1.0/backup_schedules/", method="GET")

	def d42_post_backup_schedule(
		self,
		name: str,
		method: str,
		schedule_time: str,
		job_id: int = None,
		schedule_days: str = None,
	) -> dict:
		"""
		POST /api/1.0/backup_schedules/
		Create or update a backup schedule.
		"""
		data = {
			"name": name,
			"method": str(method),
			"schedule_time": schedule_time,
		}

		if job_id is not None:
			data["job_id"] = int(job_id)
		if schedule_days is not None:
			data["schedule_days"] = schedule_days

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/backup_schedules/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_backup_schedule(self, job_id: int) -> dict:
		"""
		DELETE /api/1.0/backup_schedules/{ID}/
		Delete a scheduled backup by ID.
		"""
		resolved_job_id = int(job_id)
		endpoint = f"/api/1.0/backup_schedules/{resolved_job_id}/"
		return self.auth.request(endpoint, method="DELETE")
