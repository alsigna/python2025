import asyncio
import json
from collections.abc import AsyncGenerator
from time import perf_counter
from types import TracebackType
from typing import Any, Self
from urllib.parse import urlencode

import httpx

NETBOX_TOKEN = "34ab7e43f2ae0dde2fc3dd6469bd9384b0c2fd9c"
NETBOX_URL = "https://demo.netbox.dev"
PARAMS = [("limit", 5)]


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class NetboxAPIHandler:
    def __init__(self, base_url: str, token: str, session_limit: int = 10) -> None:
        self.base_url = base_url
        self.token = token
        self.session_limit = session_limit
        self.session: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        self.session = httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(
                verify=False,
                limits=httpx.Limits(
                    max_connections=self.session_limit,
                ),
            ),
            base_url=self.base_url,
            headers={
                "Authorization": f"Token {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "demo-python2025",
            },
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        if self.session is not None:
            await self.session.aclose()
        self.session = None

    async def devices(self) -> AsyncGenerator[dict[str, Any]]:
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")

        _next_url = "/api/dcim/devices/?" + urlencode(PARAMS)
        while _next_url is not None:
            response: httpx.Response = await self.session.get(url=_next_url)
            log(f"get url: {response.url}")
            response.raise_for_status()
            response_json = response.json()
            _next_url = response_json.get("next")
            for device in response_json.get("results", []):
                await asyncio.sleep(0.1)
                yield device

    async def patch_device(self, device_id: int, device_data: dict[str, Any]) -> None:
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")

        data = json.dumps(device_data)
        response: httpx.Response = await self.session.patch(
            url=f"/api/dcim/devices/{device_id}/",
            data=data,
        )
        log(f"patch url: {response.url}, data: {data}")
        response.raise_for_status()


async def main() -> None:
    async with NetboxAPIHandler(NETBOX_URL, NETBOX_TOKEN) as netbox:
        patch_tasks: list[asyncio.Task] = []
        async for device in netbox.devices():
            log(f"{device['name']}, {device['id']}, {device['role']['slug']}")

            patch_tasks.append(
                asyncio.create_task(
                    netbox.patch_device(device["id"], {"description": ""}),
                ),
            )
        await asyncio.gather(*patch_tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
