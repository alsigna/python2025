# python -m unittest discover -s ./c18_pytest/src/s08_stub/ -v

from typing import Any, Self, cast
from unittest import TestCase

import httpx

from c18_pytest.src.s08_stub.netbox_api_handler import NetboxAPIHandler


class ResponseStub:
    def __init__(self, data: dict[str, Any]):
        self._data = data

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self._data


class ClientStub(httpx.Client):
    def __init__(self, responses: list[dict[str, Any]]):
        self._responses = [cast(httpx.Response, ResponseStub(r)) for r in responses]
        self._calls = 0

    def get(self, url: str, params=None) -> ResponseStub:
        resp = self._responses[self._calls]
        self._calls += 1
        return resp

    def close(self) -> None:
        return None


class StubNetbox(NetboxAPIHandler):
    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args) -> None:
        return None


class NetboxAPIHandlerTestCase(TestCase):
    NETBOX_VERSION = "4.3.6"

    @classmethod
    def setUpClass(cls):
        cls.netbox = StubNetbox("http://fake-url", "fake-token")

        data = {"netbox-version": "4.3.6"}
        cls.netbox.session = ClientStub([data])

    def test_get(self) -> None:
        with self.netbox:
            response = self.netbox.get("/api/status/")
        version = response[0].get("netbox-version")
        self.assertEqual(self.NETBOX_VERSION, version)
