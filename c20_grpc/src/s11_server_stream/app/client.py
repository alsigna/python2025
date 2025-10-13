import asyncio
import logging
from collections.abc import AsyncIterator

import grpc
from rich.logging import RichHandler

from c20_grpc.src.s11_server_stream.app.pb import chars_pb2_grpc
from c20_grpc.src.s11_server_stream.app.pb.chars_pb2 import CharMessage

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        options=[("grpc.primary_user_agent", "my-grpc-client/0.0.1")],
    ) as channel:
        stub = chars_pb2_grpc.CharServiceStub(channel)
        async for response in stub.TextToChars(CharMessage(msg="abcde")):
            log.info(f">> {response.msg}")


if __name__ == "__main__":
    asyncio.run(main())
