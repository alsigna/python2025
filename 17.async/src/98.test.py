import asyncio
import socket
from types import TracebackType
from typing import Any, Self

import aiohttp

NETBOX_TOKEN = "734e96018b4dfe18716e24d3e7b4b32adbb4ad80"
NETBOX_URL = "https://demo.netbox.dev"


class NetboxAPIHandler:
    def __init__(self, base_url: str, token: str, connection_limit: int = 10) -> None:
        self._base_url = base_url
        self._token = token
        self._limit = connection_limit
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=self._limit,
                limit_per_host=self._limit,
                ssl=False,
                family=socket.AF_INET,
            ),
            base_url=self._base_url,
            raise_for_status=True,
            headers={
                "Authorization": f"Token {self._token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=aiohttp.ClientTimeout(
                total=0.1,
                connect=0.1,
            ),
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        await self._session.close()
        self._session = None

    async def get(self, url) -> dict[str, Any]:
        if self._session is None:
            raise RuntimeError("метод используется в контекстном менеджере")
        try:
            async with self._session.get(url=url) as response:
                response_json = await response.json()
        except asyncio.TimeoutError:
            print("TIMEOUT")
            return
        return response_json


async def main() -> None:
    async with NetboxAPIHandler(NETBOX_URL, NETBOX_TOKEN) as netbox:
        result = await netbox.get("/api/dcim/devices/27/")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
