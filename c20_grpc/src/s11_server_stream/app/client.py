import asyncio
import logging

import grpc
from pb import chars_pb2_grpc
from pb.chars_pb2 import CharMessage
from rich.logging import RichHandler

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
