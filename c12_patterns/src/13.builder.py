from typing import Any, Literal, Self, cast

import requests

NETBOX_TOKEN = "b91ad8c15445553d0c7d1bdc726535b3b52c3a12"  # noqa: S105
NETBOX_URL = "https://demo.netbox.dev/api/dcim/devices/"


class NetboxRequestBuilder:
    def __init__(self) -> None:
        self._method = "GET"
        self._url = ""
        self._headers: dict[str, str] = {}
        self._params: dict[str, list[str]] = {}
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
            self._params[key].append(value)
        else:
            self._params[key] = [value]
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
        return cast(dict[str, Any], response.json())


if __name__ == "__main__":
    builder = NetboxRequestBuilder()
    request = (
        builder.method("get")
        .url(NETBOX_URL)
        .add_header("Authorization", f"Token {NETBOX_TOKEN}")
        .add_header("Content-Type", "application/json")
        .add_header("Accept", "application/json")
        .add_params("manufacturer", "cisco")
        .add_params("role", "router")
        .add_params("role", "core-switch")
    )
    brief = False
    if brief:
        request.add_params("brief", "true")
    data = request.send()
    # print(data)
