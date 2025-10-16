import asyncio
import logging
from collections.abc import AsyncIterator

import grpc
from pb import chat_pb2_grpc
from pb.chat_pb2 import ChatMessage
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


async def generate_messages() -> AsyncIterator[ChatMessage]:
    for msg in ["привет", "тест", "пока"]:
        yield ChatMessage(user="Client", msg=msg)
        await asyncio.sleep(0.5)


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        options=[
            ("grpc.primary_user_agent", "my-grpc-client/0.0.1"),
        ],
    ) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(
            channel=channel,
        )
        async for response in stub.Chat(generate_messages()):
            print(f"> {response.user}: {response.msg}")


if __name__ == "__main__":
    asyncio.run(main())
