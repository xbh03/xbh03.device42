import json
import base64
from datetime import datetime, timezone

import requests


class d42_token_authentication:
    def __init__(
        self,
        host: str,
        module: object,
        result: object,
        sslverify,
        proto: str = "https",
        port: int = 443,
        debug: bool = False,
        client_key: str = None,
        client_secret_key: str = None,
        userid: str = None,
        password: str = None,
        timeout: int = 60,
    ):
        self.debug = debug
        self.host = host
        self.proto = proto
        self.port = port

        self.module = module
        self.result = result

        self.client_key = client_key
        self.client_secret_key = client_secret_key
        self.userid = userid
        self.password = password
        self.timeout = int(timeout) if timeout is not None else 60

        self.r = requests.Session()
        self.r.verify = sslverify

        # Cache token in memory for this class instance.
        self._token = None
        self._token_expires_ts = 0
        self._token_id = None

        has_client_key = bool(self.client_key)
        has_client_secret = bool(self.client_secret_key)
        has_userid = bool(self.userid)
        has_password = bool(self.password)
        has_client_pair = has_client_key and has_client_secret
        has_user_pair = has_userid and has_password

        if has_client_key != has_client_secret:
            self._fail("Provide both client_key and client_secret_key for token authentication.")

        if has_userid != has_password:
            self._fail("Provide both userid and password for basic authentication.")

        if has_client_pair and has_user_pair:
            self._fail(
                "Provide either client_key/client_secret_key for token authentication "
                "or userid/password for basic authentication, not both."
            )

        if has_client_pair:
            self.auth_mode = "token"
        elif has_user_pair:
            self.auth_mode = "basic"
        else:
            self._fail(
                "Authentication credentials are required: provide client_key/client_secret_key or userid/password."
            )

    def _base_url(self) -> str:
        return f"{self.proto}://{self.host}:{self.port}"

    def _fail(self, msg: str, **kwargs):
        if self.module and hasattr(self.module, "fail_json"):
            payload = {"msg": msg}
            payload.update(kwargs)
            self.module.fail_json(**payload)
        raise RuntimeError(msg)

    def _parse_expire_ts(self, payload: dict) -> int:
        expires = payload.get("expires")
        ttl = payload.get("ttl", 0)

        if isinstance(expires, str):
            try:
                # API returns UTC timestamps such as 2022-02-03T19:23:03.267Z.
                dt = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                return int(dt.timestamp())
            except ValueError:
                pass

        now_ts = int(datetime.now(timezone.utc).timestamp())
        try:
            # Device42 returns ttl in minutes.
            ttl_seconds = int(ttl) * 60
        except (TypeError, ValueError):
            ttl_seconds = 0
        return now_ts + ttl_seconds

    def __d42curlreq(self, url: str, method: str = "GET", data=None, headers=None) -> dict:
        full_url = f"{self._base_url()}{url}"
        req_headers = headers or {}
        req_data = data
        if data is not None and not isinstance(data, (str, bytes, bytearray)):
            req_data = json.dumps(data)

        if self.debug and self.module:
            self.module.warn(f"[d42 debug] >>> {method} {full_url}")
            safe_headers = {k: ("***" if k.lower() == "authorization" else v) for k, v in req_headers.items()}
            self.module.warn(f"[d42 debug] headers: {safe_headers}")
            self.module.warn(f"[d42 debug] body: {req_data!r}")

        try:
            response = self.r.request(
                method=method,
                url=full_url,
                headers=req_headers,
                data=req_data,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            self._fail(f"Device42 API request failed: {exc}", endpoint=url, method=method)

        if self.debug and self.module:
            self.module.warn(f"[d42 debug] <<< status={response.status_code} content-type={response.headers.get('Content-Type','')}")
            self.module.warn(f"[d42 debug] response body: {response.text[:2000]}")

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                payload = response.json()
            except ValueError:
                payload = {"raw": response.text}
        else:
            payload = {"raw": response.text}

        if not response.ok:
            self._fail(
                "Device42 API returned an error",
                status_code=response.status_code,
                endpoint=url,
                response=payload,
            )

        return payload

    def d42_api_token_authentication(self) -> str:
        """
        Request a token from Device42 API Client endpoint.
        Requires client_key and client_secret_key (API Client credentials from Device42 UI).
        These are passed as Basic Auth; the token is then used as Bearer on subsequent calls.
        """
        if self.auth_mode != "token":
            self._fail("Token authentication is not available in basic auth mode.")

        if not self.client_key or not self.client_secret_key:
            self._fail(
                "client_key and client_secret_key are required for token authentication. "
                "Create an API Client in Device42 UI and provide its key and secret key."
            )

        credentials = base64.b64encode(
            f"{self.client_key}:{self.client_secret_key}".encode()
        ).decode()

        payload = self.__d42curlreq(
            "/tauth/1.0/token/",
            method="POST",
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        token = payload.get("token")
        if not token:
            self._fail("Device42 token response does not contain 'token'", response=payload)

        # Keep a small safety margin to avoid using token at exact expiry time.
        expires_ts = self._parse_expire_ts(payload)
        self._token = token
        self._token_id = payload.get("token_id")
        self._token_expires_ts = max(0, expires_ts - 15)
        return token

    def d42_delete_api_token(self, token_id: int = None) -> dict:
        """
        Delete a Device42 API token.
        If token_id is not provided, use cached token_id from last authentication.
        """
        resolved_token_id = token_id if token_id is not None else self._token_id
        if resolved_token_id is None:
            self._fail(
                "token_id is required to delete API token. Authenticate first or provide token_id explicitly."
            )

        payload = self.request(f"/tauth/1.0/token/{resolved_token_id}/", method="DELETE")

        # Token was revoked: clear local cache so next calls get a fresh token.
        self._token = None
        self._token_id = None
        self._token_expires_ts = 0
        return payload

    def get_bearer_token(self, force_refresh: bool = False) -> str:
        now_ts = int(datetime.now(timezone.utc).timestamp())
        if (
            not force_refresh
            and self._token
            and self._token_expires_ts
            and now_ts < self._token_expires_ts
        ):
            return self._token
        return self.d42_api_token_authentication()

    def get_auth_headers(self, headers: dict = None, force_refresh: bool = False) -> dict:
        if self.auth_mode == "basic":
            basic_creds = base64.b64encode(f"{self.userid}:{self.password}".encode()).decode()
            req_headers = {"Authorization": f"Basic {basic_creds}"}
        else:
            req_headers = {"Authorization": f"Bearer {self.get_bearer_token(force_refresh=force_refresh)}"}
        if headers:
            req_headers.update(headers)
        return req_headers

    def request(self, url: str, method: str = "GET", data=None, headers=None) -> dict:
        auth_headers = self.get_auth_headers(headers=headers)
        full_url = f"{self._base_url()}{url}"
        req_data = data
        if data is not None and not isinstance(data, (str, bytes, bytearray)):
            req_data = json.dumps(data)

        try:
            response = self.r.request(
                method=method,
                url=full_url,
                headers=auth_headers,
                data=req_data,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            self._fail(f"Device42 authenticated request failed: {exc}", endpoint=url, method=method)

        if response.status_code == 401 and self.auth_mode == "token":
            auth_headers = self.get_auth_headers(headers=headers, force_refresh=True)
            try:
                response = self.r.request(
                    method=method,
                    url=full_url,
                    headers=auth_headers,
                    data=req_data,
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                self._fail(
                    f"Device42 authenticated retry request failed: {exc}",
                    endpoint=url,
                    method=method,
                )

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                payload = response.json()
            except ValueError:
                payload = {"raw": response.text}
        else:
            payload = {"raw": response.text}

        if not response.ok:
            self._fail(
                "Device42 authenticated API returned an error",
                status_code=response.status_code,
                endpoint=url,
                response=payload,
                auth_mode=self.auth_mode,
            )

        return payload