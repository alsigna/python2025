import asyncio
from collections.abc import AsyncIterator

import grpc
from grpc.aio import ServicerContext
from grpc_reflection.v1alpha import reflection

from pb import scrapli_grpc_pb2_grpc
from pb.scrapli_grpc_pb2 import DESCRIPTOR as SCRAPLI_SERVICE_DESCRIPTOR
from pb.scrapli_grpc_pb2 import Command, Response

from .logger import log
from .scrapli_handler import ScrapliHandler


class ScrapliServicer(scrapli_grpc_pb2_grpc.ScrapliServiceServicer):
    async def SendCommandChat(  # noqa: N802
        self,
        request_iterator: AsyncIterator[Command],
        context: ServicerContext[Command, Response],
    ) -> AsyncIterator[Response]:
        async for response in ScrapliHandler.handle_chat(request_iterator, context):
            yield response

    async def SendCommand(  # noqa: N802
        self,
        request: Command,
        context: ServicerContext[Command, Response],
    ) -> Response:
        return await ScrapliHandler.handle(request, context)


async def main() -> None:
    server = grpc.aio.server()
    scrapli_grpc_pb2_grpc.add_ScrapliServiceServicer_to_server(ScrapliServicer(), server)
    services = (
        SCRAPLI_SERVICE_DESCRIPTOR.services_by_name["ScrapliService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(services, server)

    server.add_insecure_port("[::]:50051")
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
        log.info("Сервер прерван пользователем")
        log.info("Сервер прерван пользователем")
