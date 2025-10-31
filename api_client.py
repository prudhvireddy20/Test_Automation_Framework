import requests
from typing import Dict, Any, Optional


class APIClient:

    def __init__(self, base_url: str, token: Optional[str] = None, timeout: Optional[float] = 10.0):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Content-Type": "application/json"})
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def register(self, username: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/register"
        resp = self.session.post(url, json={"username": username, "password": password}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def login(self, username: str, password: str) -> str:
        url = f"{self.base_url}/login"
        resp = self.session.post(url, auth=(username, password), timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        token = data.get("token")
        if not token:
            raise RuntimeError("No token returned from login")
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token

    def list_tenants(self) -> Dict[str, Any]:
        url = f"{self.base_url}/api/tenant"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def list_virtualservices(self) -> Dict[str, Any]:
        url = f"{self.base_url}/api/virtualservice"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_virtualservice(self, uuid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/virtualservice/{uuid}"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def put_virtualservice(self, uuid: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/virtualservice/{uuid}"
        resp = self.session.put(url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def list_serviceengines(self) -> Dict[str, Any]:
        url = f"{self.base_url}/api/serviceengine"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
