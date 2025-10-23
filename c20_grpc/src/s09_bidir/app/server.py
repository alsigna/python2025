import asyncio
import logging
from collections.abc import AsyncIterator

import grpc
from grpc.aio import ServicerContext
from pb import chat_pb2_grpc
from pb.chat_pb2 import ChatMessage
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


class ChatHandler:
    @classmethod
    async def handle(
        cls,
        request_iterator: AsyncIterator[ChatMessage],
        context: ServicerContext[ChatMessage, ChatMessage],
    ) -> AsyncIterator[ChatMessage]:
        async for message in request_iterator:
            log.info(f"{message.user=}, {message.msg=}")
            await asyncio.sleep(0.2)
            yield ChatMessage(
                user="Server",
                msg=message.msg[::-1],
            )


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    async def Chat(  # noqa: N802
        self,
        request_iterator: AsyncIterator[ChatMessage],
        context: ServicerContext[ChatMessage, ChatMessage],
    ) -> AsyncIterator[ChatMessage]:
        # первый подход:
        async for message in request_iterator:
            log.info(f"{message.user=}, {message.msg=}")
            await asyncio.sleep(0.2)
            yield ChatMessage(
                user="Server",
                msg=message.msg[::-1],
            )

        # # выносим обработку в отдельный класс
        # async for msg in ChatHandler.handle(request_iterator, context):
        #     yield msg


async def main() -> None:
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        servicer=ChatService(),
        server=server,
    )
    server.add_insecure_port(
        address="[::]:50051",
    )
    await server.start()
    log.info("gRPC сервер запущен на порту 50051")

    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        log.info("Остановка сервера...")
        await server.stop(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Сервер прерван пользователем")
