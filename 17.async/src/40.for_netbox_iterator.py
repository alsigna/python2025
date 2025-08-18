import asyncio
import json
from time import perf_counter
from types import TracebackType
from typing import Any, Self
from urllib.parse import urlencode

import httpx

NETBOX_TOKEN = "54536d673c05f56af3ec42705f642b95f1cf074a"
NETBOX_URL = "https://demo.netbox.dev"
PARAMS = [("limit", 10)]


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class NetboxAPIHandler:
    def __init__(self, base_url: str, token: str, session_limit: int = 10) -> None:
        self.base_url = base_url
        self.token = token
        self.session_limit = session_limit
        self.session: httpx.AsyncClient | None = None
        self._next_url: str | None = None
        self._current_page_results: list[dict[str, Any]] = []
        self._current_index: int = 0

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
        self._next_url = "/api/dcim/devices/?" + urlencode(PARAMS)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.session is not None:
            await self.session.aclose()
        self.session = None

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> dict[str, Any]:
        if self.session is None:
            raise RuntimeError("используйте контекстный менеджер")

        if self._current_index < len(self._current_page_results):
            device = self._current_page_results[self._current_index]
            self._current_index += 1
            await asyncio.sleep(0.1)
            return device

        if self._next_url is None:
            raise StopAsyncIteration

        response: httpx.Response = await self.session.get(url=self._next_url)
        log(f"get url: {response.url}")
        response.raise_for_status()
        response_json = response.json()
        self._next_url = response_json.get("next")
        self._current_page_results = response_json.get("results", [])
        self._current_index = 0

        if not self._current_page_results:
            raise StopAsyncIteration

        return await self.__anext__()

    async def patch_device(self, device_id: int, device_data: dict[str, Any]) -> None:
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")

        data = json.dumps(device_data)
        response: httpx.Response = await self.session.patch(
            url=f"/api/dcim/devices/{device_id}/",
            content=data,
        )
        log(f"patch url: {response.url}, data: {data}")
        response.raise_for_status()


async def main() -> None:
    async with NetboxAPIHandler(NETBOX_URL, NETBOX_TOKEN) as netbox:
        patch_tasks: list[asyncio.Task] = []
        async for device in netbox:
            log(f"{device['name']}, {device['id']}, {device['role']['slug']}")
            if device["role"]["slug"] != "router":
                continue

            patch_tasks.append(
                asyncio.create_task(
                    netbox.patch_device(device["id"], {"description": "test router - 2"}),
                ),
            )
        await asyncio.gather(*patch_tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
