from typing import Any, Literal, Self

import requests

NETBOX_TOKEN = "fe7ec39d2863d3b04860bd86ec28c2e2ff526ded"
NETBOX_URL = "https://demo.netbox.dev/api/dcim/devices/"


class NetboxRequestBuilder:
    def __init__(self):
        self._method = "GET"
        self._url = ""
        self._headers = {}
        self._params = {}
        self._timeout = 5

    def method(self, method: Literal["get", "post"] = "get") -> Self:
        self._method = method.upper()
        return self

    def url(self, url: str) -> Self:
        self._url = url
        return self

    def add_header(self, key: str, value: str) -> Self:
        self._headers[key] = value
        return self

    def add_params(self, key: str, value: str) -> Self:
        if key in self._params:
            if isinstance(self._params[key], list):
                self._params[key].append(value)
            else:
                self._params[key] = [self._params[key], value]
        else:
            self._params[key] = value
        return self

    def timeout(self, timeout: int = 5) -> Self:
        self._timeout = timeout
        return self

    def send(self) -> dict[str, Any]:
        response = requests.request(
            method=self._method,
            url=self._url,
            params=self._params,
            headers=self._headers,
            timeout=self._timeout,
        )
        print(response.url)
        response.raise_for_status()
        return response.json()


builder = NetboxRequestBuilder()
data = (
    builder.method("get")
    .url(NETBOX_URL)
    .add_header("Authorization", f"Token {NETBOX_TOKEN}")
    .add_header("Content-Type", "application/json")
    .add_header("Accept", "application/json")
    .add_params("manufacturer", "cisco")
    .add_params("role", "router")
    .add_params("role", "switch")
    .add_params("brief", True)
    .send()
)
