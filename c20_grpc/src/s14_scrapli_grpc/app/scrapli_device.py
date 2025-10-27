from types import TracebackType
from typing import Any, Literal, Self

from scrapli import AsyncScrapli
from scrapli.response import Response

from pb.scrapli_grpc_pb2 import Host, Platform

__all__ = ("ScrapliDevice",)


class ScrapliDevice:
    def __init__(self, host: Host) -> None:
        self.host = host.host
        self.auth_username = host.auth_username
        self.auth_password = host.auth_password
        self.auth_secondary = host.auth_secondary or host.auth_password
        self.platform = host.platform
        # PLATFORM_CISCO_IOSXE => cisco_iosxe
        self.platform = Platform.Name(host.platform).split("_", 1)[1].lower()
        self.cli: AsyncScrapli = AsyncScrapli(**self.scrapli)

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "auth_username": self.auth_username,
            "auth_password": self.auth_password,
            "auth_secondary": self.auth_secondary,
            "platform": self.platform,
            "transport": "asyncssh",
            "host": self.host,
            "auth_strict_key": False,
            "port": 22,
            "transport_options": {
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1",
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
        await self.cli.open()

    async def aclose(self) -> None:
        await self.cli.close()

    async def send_command(self, command: str) -> Response:
        if not self.cli.isalive():
            await self.cli.open()

        response = await self.cli.send_command(command)
        return response
        return response
        return response
