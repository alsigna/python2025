import asyncio
import logging
import re
from collections.abc import AsyncIterator

import grpc
from rich.logging import RichHandler

from pb import scrapli_grpc_pb2_grpc
from pb.scrapli_grpc_pb2 import Command, Host, Platform, Response

log = logging.getLogger("client")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


HOST = Host(
    host="192.168.122.101",
    platform=Platform.PLATFORM_CISCO_IOSXE,
    auth_username="admin",
    auth_password="P@ssw0rd",  # noqa: S106
)


class ClientHandler:
    def __init__(self, stub: scrapli_grpc_pb2_grpc.ScrapliServiceStub):
        self._stub = stub
        self._queue: asyncio.Queue[Command] = asyncio.Queue()
        self._counter = 0

    async def _message_generator(self) -> AsyncIterator[Command]:
        while True:
            cmd = await self._queue.get()
            log.debug(cmd)
            if cmd is None:
                return
            yield Command(
                command=cmd,
                host=HOST,
            )

    async def _handle_server_responses(self, response_iterator: AsyncIterator[Response]) -> None:
        async for message in response_iterator:
            self._counter -= 1
            if message.channel_input == "show ip int br":
                for m in re.finditer(r"(Gigabit\S+)\s+.*\bup\b\s+\bup\b", message.result):
                    interface = m.group(1)
                    await self.add_command(f"show run interface {interface}")
            log.info(message.result)

            if self._counter == 0:
                await self._queue.put(None)

    async def add_command(self, command: str) -> None:
        await self._queue.put(command)
        self._counter += 1

    async def exec_chat(self) -> None:
        await self.add_command("show version")
        await self.add_command("show ip int br")
        response_iterator = self._stub.SendCommandChat(self._message_generator())
        await self._handle_server_responses(response_iterator)


async def main() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = scrapli_grpc_pb2_grpc.ScrapliServiceStub(channel)
        handler = ClientHandler(stub)
        log.warning("EXEC-CHAT")
        await handler.exec_chat()


if __name__ == "__main__":
    asyncio.run(main())
