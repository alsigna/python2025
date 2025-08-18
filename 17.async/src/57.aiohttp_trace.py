import asyncio
import socket
from datetime import datetime
from time import perf_counter
from types import SimpleNamespace, TracebackType
from typing import Any, Self
from zoneinfo import ZoneInfo

import aiohttp

NETBOX_TOKEN = "734e96018b4dfe18716e24d3e7b4b32adbb4ad80"
NETBOX_URL = "https://demo.netbox.dev"


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class HTTPTrace:
    @classmethod
    def _get_trace_config(cls) -> aiohttp.TraceConfig:
        trace_config = aiohttp.TraceConfig()
        # инициализация запроса
        trace_config.on_request_start.append(cls._trace_on_request_start)
        # dns lookup завершен
        trace_config.on_dns_resolvehost_end.append(cls._trace_on_dns_resolvehost_end)
        # начало установления соединения
        trace_config.on_connection_create_start.append(cls._trace_on_connection_create_start)
        # завершение запроса
        trace_config.on_request_end.append(cls._trace_on_request_end)
        # если исключение
        trace_config.on_request_exception.append(cls._trace_on_request_exception)
        return trace_config

    @classmethod
    async def _trace_on_request_start(
        cls,
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: aiohttp.TraceRequestStartParams,
    ) -> None:
        start_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        log(f"инициализация '{params.method}' запроса на '{params.url}'")
        params.headers["Authorization"] = "strip"
        trace_config_ctx.start_time = start_time

    @classmethod
    async def _trace_on_dns_resolvehost_end(
        cls,
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: aiohttp.TraceDnsResolveHostEndParams,
    ) -> None:
        log(f"DNS lookup завершен, host: '{params.host}'")

    @classmethod
    async def _trace_on_connection_create_start(
        cls,
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: aiohttp.TraceConnectionCreateStartParams,
    ) -> None:
        log("установление сессии с сервером")

    @classmethod
    async def _trace_on_request_end(
        cls,
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: aiohttp.TraceRequestEndParams,
    ) -> None:
        end_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        elapsed_time = (end_time - trace_config_ctx.start_time).total_seconds()
        log(f"завершен '{params.method}' запрос к '{params.url}'")
        log(f"статус-код: '{params.response.status}, время выполнения: {elapsed_time} секунд")

    @classmethod
    async def _trace_on_request_exception(
        cls,
        session: aiohttp.ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: aiohttp.TraceRequestExceptionParams,
    ) -> None:
        log(f"получено исключение в '{params.method}' запросе к '{params.url}': <{params.exception}>")
        log(f"детали исключения: {params.exception.args}")


class NetboxAPIHandler:
    def __init__(
        self,
        base_url: str,
        token: str,
        connection_limit: int = 10,
        trace: bool = False,
    ) -> None:
        self._base_url = base_url
        self._token = token
        self._limit = connection_limit
        self._session: aiohttp.ClientSession | None = None
        self._trace = trace

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
            timeout=aiohttp.ClientTimeout(total=5),
            trace_configs=[HTTPTrace._get_trace_config()] if self._trace else None,
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
            log("TIMEOUT")
            return
        except aiohttp.ClientResponseError as exc:
            log(f"ошибка запроса: {exc.message}")
            log(f"\tстатус-код: {exc.status}")
            log(f"\trequest-id: {exc.headers['X-Request-ID']}")
            return
        return response_json


async def main() -> None:
    async with NetboxAPIHandler(NETBOX_URL, NETBOX_TOKEN, trace=True) as netbox:
        await netbox.get("/api/dcim/devices/27/")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
