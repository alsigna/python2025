"""async сервер, генерация proto.

python -m grpc_tools.protoc \
  --proto_path=./proto \
  --python_out=./app/pb \
  --grpc_python_out=./app/pb \
  --mypy_out=./app/pb \
  ./proto/*
"""

import asyncio
import logging
from collections.abc import AsyncIterator

import grpc
from grpc.aio import ServicerContext
from rich.logging import RichHandler

from c20_grpc.src.s11_server_stream.app.pb import chars_pb2_grpc
from c20_grpc.src.s11_server_stream.app.pb.chars_pb2 import CharMessage

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


class CharService(chars_pb2_grpc.CharServiceServicer):
    async def TextToChars(  # noqa: N802
        self,
        request: CharMessage,
        context: ServicerContext[CharMessage, CharMessage],
    ) -> AsyncIterator[CharMessage]:
        for char in request.msg:
            yield (CharMessage(msg=char))


async def main() -> None:
    server = grpc.aio.server()
    chars_pb2_grpc.add_CharServiceServicer_to_server(CharService(), server)
    server.add_insecure_port(address="[::]:50051")
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
