import asyncio
import logging
import re
from collections.abc import AsyncIterator

import grpc
from pb_restored import server_pb2, server_pb2_grpc
from rich.logging import RichHandler

from .interceptors import ClientSSAuthInterceptor, ClientUUAuthInterceptor

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)

CMD_TEMPLATE = {
    "host": "192.168.122.102",
    "host_params": {
        "credentials": {
            "login": "admin",
            "password": "P@ssw0rd",
        },
        "device": "cisco",
    },
    "string_result": True,
}


class ClientHandler:
    def __init__(self, stub: server_pb2_grpc.GnetcliStub):
        self._stub = stub
        self._queue: asyncio.Queue[server_pb2.CMD | None] = asyncio.Queue()

    async def _message_generator(self) -> AsyncIterator[server_pb2.CMD]:
        while True:
            cmd = await self._queue.get()
            if cmd is None:
                return
            yield server_pb2.CMD(
                cmd=cmd,
                **CMD_TEMPLATE,
            )

    async def _handle_server_responses(self, response_iterator: AsyncIterator[server_pb2.CMDResult]) -> None:
        async for message in response_iterator:
            if re.search(r"\bStatus\b|\bProtocol\b", message.out_str, flags=re.I):
                for m in re.finditer(r"(Gigabit\S+)\s+.*\bup\b\s+\bup\b", message.out_str):
                    interface = m.group(1)
                    await self._queue.put(f"show run interface {interface}")
            log.info(message.out_str)
            await self._queue.put(None)

    async def exec_chat(self) -> None:
        await self._queue.put("show ip int br")
        response_iterator = self._stub.ExecChat(self._message_generator())
        await self._handle_server_responses(response_iterator)

    async def exec(self) -> None:
        cmd = "show ip int br"
        response: server_pb2.CMDResult = await self._stub.Exec(
            server_pb2.CMD(cmd=cmd, **CMD_TEMPLATE),
        )
        log.info(response.out_str)
        interfaces = re.findall(r"(Gigabit\S+)\s+.*\bup\b\s+\bup\b", response.out_str)
        tasks = [
            self._stub.Exec(
                server_pb2.CMD(cmd=f"show run interface {interface}", **CMD_TEMPLATE),
            )
            for interface in interfaces
        ]
        async for result in asyncio.as_completed(tasks):
            log.info(result.result().out_str)


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        interceptors=[
            ClientUUAuthInterceptor("mylogin", "mysecret"),
            ClientSSAuthInterceptor("mylogin", "mysecret"),
        ],
    ) as channel:
        stub = server_pb2_grpc.GnetcliStub(channel)
        handler = ClientHandler(stub)

        log.warning("EXEC")
        await handler.exec()

        log.warning("EXEC-CHAT")
        await handler.exec_chat()


if __name__ == "__main__":
    asyncio.run(main())
