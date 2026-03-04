"""SigV4-signed HTTP client for CloudSecure API Gateway."""

import json

import botocore.auth
import botocore.awsrequest
import botocore.session
import requests


class CloudSecureAPI:
    """HTTP client that signs requests with AWS SigV4 for IAM-authenticated API Gateway."""

    def __init__(self, endpoint: str, profile: str | None = None,
                 region: str | None = None):
        self.endpoint = endpoint.rstrip("/")
        self.region = region or "eu-west-1"

        session = botocore.session.Session(profile=profile)
        self.credentials = session.get_credentials().get_frozen_credentials()

    def _sign_request(self, method: str, url: str, body: str | None = None,
                      headers: dict | None = None) -> dict:
        """Sign a request using SigV4 and return signed headers."""
        request = botocore.awsrequest.AWSRequest(
            method=method,
            url=url,
            data=body,
            headers=headers or {},
        )

        signer = botocore.auth.SigV4Auth(self.credentials, "execute-api", self.region)
        signer.add_auth(request)
        return dict(request.headers)

    def request(self, method: str, path: str, body: dict | None = None) -> dict:
        """Make a signed API request and return the parsed JSON response."""
        url = f"{self.endpoint}/{path.lstrip('/')}"
        json_body = json.dumps(body) if body else None

        headers = {"Content-Type": "application/json"} if body else {}
        signed_headers = self._sign_request(method, url, json_body, headers)

        response = requests.request(
            method=method,
            url=url,
            data=json_body,
            headers=signed_headers,
            timeout=30,
        )

        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError):
            data = {"raw": response.text}

        if response.status_code >= 400:
            error_msg = data.get("error", data.get("message", response.text))
            raise RuntimeError(f"API error ({response.status_code}): {error_msg}")

        return data

    def get(self, path: str) -> dict:
        return self.request("GET", path)

    def post(self, path: str, body: dict) -> dict:
        return self.request("POST", path, body)
