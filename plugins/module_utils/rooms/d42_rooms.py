from urllib.parse import urlencode

from ..admin_users_groups.d42_token_authentication import d42_token_authentication


class d42_rooms:
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

	def d42_get_rooms(self, name: str = None, building_id: int = None, building: str = None) -> dict:
		"""
		GET /api/1.0/rooms/
		Retrieve information about all rooms.
		"""
		params = {}

		if name is not None:
			params["name"] = name
		if building_id is not None:
			params["building_id"] = int(building_id)
		if building is not None:
			params["building"] = building

		endpoint = "/api/1.0/rooms/"
		if params:
			endpoint = f"{endpoint}?{urlencode(params)}"

		return self.auth.request(endpoint, method="GET")

	def d42_get_room_by_id(self, room_id: int) -> dict:
		"""
		GET /api/1.0/rooms/{ID}/
		Retrieve detailed information about a specific room.
		"""
		resolved_room_id = int(room_id)
		return self.auth.request(f"/api/1.0/rooms/{resolved_room_id}/", method="GET")

	def _build_room_payload(
		self,
		name: str = None,
		building_id: int = None,
		building: str = None,
		notes: str = None,
		horizontal_grid_numbering: str = None,
		horizontal_grid_start: str = None,
		vertical_grid_numbering: str = None,
		vertical_grid_start: str = None,
		uom: str = None,
		height: str = None,
		grid_rows: str = None,
		grid_cols: str = None,
		raised_floor: str = None,
		raised_floor_height: str = None,
		groups: str = None,
		reverse_xaxis: str = None,
		reverse_yaxis: str = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		data = {}

		if name is not None:
			data["name"] = name
		if building_id is not None:
			data["building_id"] = int(building_id)
		if building is not None:
			data["building"] = building
		if notes is not None:
			data["notes"] = notes
		if horizontal_grid_numbering is not None:
			data["horizontal_grid_numbering"] = horizontal_grid_numbering
		if horizontal_grid_start is not None:
			data["horizontal_grid_start"] = horizontal_grid_start
		if vertical_grid_numbering is not None:
			data["vertical_grid_numbering"] = vertical_grid_numbering
		if vertical_grid_start is not None:
			data["vertical_grid_start"] = vertical_grid_start
		if uom is not None:
			data["uom"] = uom
		if height is not None:
			data["height"] = height
		if grid_rows is not None:
			data["grid_rows"] = grid_rows
		if grid_cols is not None:
			data["grid_cols"] = grid_cols
		if raised_floor is not None:
			data["raised_floor"] = raised_floor
		if raised_floor_height is not None:
			data["raised_floor_height"] = raised_floor_height
		if groups is not None:
			data["groups"] = groups
		if reverse_xaxis is not None:
			data["reverse_xaxis"] = reverse_xaxis
		if reverse_yaxis is not None:
			data["reverse_yaxis"] = reverse_yaxis
		if tags is not None:
			data["tags"] = tags
		if tags_remove is not None:
			data["tags_remove"] = tags_remove

		return data

	def d42_post_rooms(
		self,
		name: str,
		building_id: int = None,
		building: str = None,
		notes: str = None,
		horizontal_grid_numbering: str = None,
		horizontal_grid_start: str = None,
		vertical_grid_numbering: str = None,
		vertical_grid_start: str = None,
		uom: str = None,
		height: str = None,
		grid_rows: str = None,
		grid_cols: str = None,
		raised_floor: str = None,
		raised_floor_height: str = None,
		groups: str = None,
		reverse_xaxis: str = None,
		reverse_yaxis: str = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		"""
		POST /api/1.0/rooms/
		Create or update a room.
		Requires name and one of building_id/building for new room creation.
		"""
		data = self._build_room_payload(
			name=name,
			building_id=building_id,
			building=building,
			notes=notes,
			horizontal_grid_numbering=horizontal_grid_numbering,
			horizontal_grid_start=horizontal_grid_start,
			vertical_grid_numbering=vertical_grid_numbering,
			vertical_grid_start=vertical_grid_start,
			uom=uom,
			height=height,
			grid_rows=grid_rows,
			grid_cols=grid_cols,
			raised_floor=raised_floor,
			raised_floor_height=raised_floor_height,
			groups=groups,
			reverse_xaxis=reverse_xaxis,
			reverse_yaxis=reverse_yaxis,
			tags=tags,
			tags_remove=tags_remove,
		)

		payload = urlencode(data)
		return self.auth.request(
			"/api/1.0/rooms/",
			method="POST",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_put_room(
		self,
		room_id: int,
		name: str = None,
		building_id: int = None,
		building: str = None,
		notes: str = None,
		horizontal_grid_numbering: str = None,
		horizontal_grid_start: str = None,
		vertical_grid_numbering: str = None,
		vertical_grid_start: str = None,
		uom: str = None,
		height: str = None,
		grid_rows: str = None,
		grid_cols: str = None,
		raised_floor: str = None,
		raised_floor_height: str = None,
		groups: str = None,
		reverse_xaxis: str = None,
		reverse_yaxis: str = None,
		tags: str = None,
		tags_remove: str = None,
	) -> dict:
		"""
		PUT /api/1.0/rooms/{ID}/
		Update an existing room.
		"""
		resolved_room_id = int(room_id)
		data = self._build_room_payload(
			name=name,
			building_id=building_id,
			building=building,
			notes=notes,
			horizontal_grid_numbering=horizontal_grid_numbering,
			horizontal_grid_start=horizontal_grid_start,
			vertical_grid_numbering=vertical_grid_numbering,
			vertical_grid_start=vertical_grid_start,
			uom=uom,
			height=height,
			grid_rows=grid_rows,
			grid_cols=grid_cols,
			raised_floor=raised_floor,
			raised_floor_height=raised_floor_height,
			groups=groups,
			reverse_xaxis=reverse_xaxis,
			reverse_yaxis=reverse_yaxis,
			tags=tags,
			tags_remove=tags_remove,
		)

		payload = urlencode(data)
		return self.auth.request(
			f"/api/1.0/rooms/{resolved_room_id}/",
			method="PUT",
			data=payload,
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)

	def d42_delete_room(self, room_id: int) -> dict:
		"""
		DELETE /api/1.0/rooms/{ID}/
		Delete a room by ID.
		"""
		resolved_room_id = int(room_id)
		return self.auth.request(f"/api/1.0/rooms/{resolved_room_id}/", method="DELETE")
