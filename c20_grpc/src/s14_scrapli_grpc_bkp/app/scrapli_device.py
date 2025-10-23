from types import TracebackType
from typing import Any, Literal, Self

from pb.scrapli_grpc_pb2 import Host, Platform
from scrapli import AsyncScrapli

from .logger import log

__all__ = ("ScrapliDevice",)


class ScrapliDevice:
    def __init__(
        self,
        host: Host,
    ) -> None:
        self.host = host.host
        # PLATFORM_CISCO_IOSXE -> cisco_iosxe
        self.platform = Platform.Name(host.platform).split("_", 1)[1].lower()
        self.auth_username = host.auth_username
        self.auth_password = host.auth_password
        self.auth_secondary = host.auth_secondary
        self.cli: AsyncScrapli = AsyncScrapli(host=self.host, **self.scrapli)

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "transport": "asyncssh",
            "platform": self.platform,
            "auth_username": self.auth_username,
            "auth_password": self.auth_password,
            "auth_secondary": self.auth_secondary,
            "auth_strict_key": False,
            "transport_options": {
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ],
            },
        }

    async def __aenter__(self) -> Self:
        await self.aopen()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        await self.aclose()
        return False

    async def aopen(self) -> None:
        if self.cli.isalive():
            try:
                await self.cli.get_prompt()
            except Exception:
                log.warning(f"{self.host}: сессия с устройство оборвана")
            return

        try:
            await self.cli.open()
        except Exception as exc:
            log.exception(
                "{}: неизвестная ошибка ошибка открытия сессии, {}: {}".format(
                    self.host,
                    exc.__class__.__name__,
                    str(exc),
                ),
            )
            raise exc
        else:
            log.debug(f"{self.host}: сессия с устройством открыта")

    async def aclose(self) -> None:
        try:
            await self.cli.close()
        except Exception as exc:
            log.warning(
                "{}: ошибка закрытия сессии, {}: {}".format(
                    self.host,
                    exc.__class__.__name__,
                    str(exc),
                ),
            )
        else:
            log.debug(f"{self.host}: сессия с устройством закрыта")
