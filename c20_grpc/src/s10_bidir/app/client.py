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


class ChatClientHandler:
    def __init__(self, stub: chat_pb2_grpc.ChatServiceStub):
        self._stub = stub
        self._queue: asyncio.Queue[ChatMessage | None] = asyncio.Queue()

    async def _message_generator(self) -> AsyncIterator[ChatMessage]:
        while True:
            msg = await self._queue.get()
            if msg is None:
                return
            print(msg)
            yield msg

    async def _handle_server_responses(self, response_iterator: AsyncIterator[ChatMessage]) -> None:
        print(response_iterator)
        print(type(response_iterator))
        async for message in response_iterator:
            log.info(f"{message.user=}, {message.msg=}")

            if len(message.msg) <= 1:
                log.info("последнее сообщение")
                await self._queue.put(None)
                return

            await self._queue.put(ChatMessage(user="Client", msg=message.msg[:-1]))

    async def chat(self) -> None:
        await self._queue.put(ChatMessage(user="Client", msg="12345"))
        response_iterator = self._stub.Chat(self._message_generator())
        await self._handle_server_responses(response_iterator)


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        options=[("grpc.primary_user_agent", "my-grpc-client/0.0.1")],
    ) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        handler = ChatClientHandler(stub)
        await handler.chat()


if __name__ == "__main__":
    asyncio.run(main())
