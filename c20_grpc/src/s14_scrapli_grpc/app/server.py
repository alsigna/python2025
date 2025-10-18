import asyncio
import traceback
from collections.abc import AsyncIterator

import grpc
from grpc.aio import ServicerContext
from pb import scrapli_grpc_pb2_grpc
from pb.scrapli_grpc_pb2 import Command, Result

from .logger import log
from .scrapli_service_handler import ScrapliServiceHandler


class ScrapliServiceServicer(scrapli_grpc_pb2_grpc.ScrapliServiceServicer):
    async def SendCommand(  # noqa: N802
        self,
        request: Command,
        context: ServicerContext[Command, Result],
    ) -> Result:
        try:
            result = await ScrapliServiceHandler.handle(request, context)
        except Exception as exc:
            traceback.print_exc()
            raise exc
        else:
            return result

    async def SendCommandChat(  # noqa: N802
        self,
        request_iterator: AsyncIterator[Command],
        context: ServicerContext[Command, Result],
    ) -> AsyncIterator[Result]:
        async for result in ScrapliServiceHandler.handle_chat(request_iterator, context):
            yield result


async def main() -> None:
    server = grpc.aio.server()
    scrapli_grpc_pb2_grpc.add_ScrapliServiceServicer_to_server(ScrapliServiceServicer(), server)
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
