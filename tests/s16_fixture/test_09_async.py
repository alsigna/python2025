import asyncio
from collections.abc import AsyncIterator, Iterator
from os import getenv

import httpx
import pytest

from c18_pytest.src.s16_fixture.netbox_api_handler import NetboxAPIHandler


@pytest.mark.api()
class TestNetboxAPIHandler:
    NETBOX_VERSION = "4.4.0"

    @pytest.fixture()
    def session(self) -> Iterator[httpx.Client]:
        test_netbox_url = getenv("TEST_NETBOX_URL")
        test_netbox_token = getenv("TEST_NETBOX_TOKEN")
        with NetboxAPIHandler(test_netbox_url, test_netbox_token) as _session:
            yield _session

    @pytest.fixture()
    async def asession(self) -> AsyncIterator[httpx.AsyncClient]:
        test_netbox_url = getenv("TEST_NETBOX_URL")
        test_netbox_token = getenv("TEST_NETBOX_TOKEN")
        async with NetboxAPIHandler(test_netbox_url, test_netbox_token) as _asession:
            yield _asession

    def test_get(self, session: httpx.Client) -> None:
        response = session.get("/api/status/")

        assert isinstance(response, list)
        assert len(response) == 1
        version = response[0].get("netbox-version")
        assert version == self.NETBOX_VERSION

    @pytest.mark.asyncio()
    async def test_aget_1(self, asession: httpx.AsyncClient) -> None:
        loop = asyncio.get_running_loop()
        print(f"test_aget_1: {id(loop)=}")

        response = await asession.aget("/api/status/")

        assert isinstance(response, list)
        assert len(response) == 1
        version = response[0].get("netbox-version")
        assert version == self.NETBOX_VERSION

    @pytest.mark.asyncio()
    async def test_aget_2(self, asession: httpx.AsyncClient) -> None:
        loop = asyncio.get_running_loop()
        print(f"test_aget_1: {id(loop)=}")

        response = await asession.aget("/api/status/")

        assert isinstance(response, list)
        assert len(response) == 1
        version = response[0].get("netbox-version")
        assert version == self.NETBOX_VERSION
