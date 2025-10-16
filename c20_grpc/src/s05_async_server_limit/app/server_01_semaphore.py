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
from random import randint

import grpc
from grpc.aio import ServicerContext
from pb import ping_pb2_grpc
from pb.ping_pb2 import PingReply, PingRequest
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


semaphore = asyncio.Semaphore(10)


# логика отдельно
class PingHandler:
    @classmethod
    async def handle(cls, target: str) -> tuple[bool, str]:
        await asyncio.sleep(randint(50, 200) / 100)
        log.info(f"запрос '{target}' обработан")
        return True, f"ответ на запрос '{target}'"


# gRPC сервер отдельно
class PingService(ping_pb2_grpc.PingServiceServicer):
    async def Ping(  # noqa: N802
        self,
        request: PingRequest,
        context: ServicerContext[PingRequest, PingReply],
    ) -> PingReply:
        async with semaphore:
            log.info(f"новый запрос: '{request.target}'")
            ok, msg = await PingHandler.handle(request.target)
            return PingReply(ok=ok, msg=msg)


async def main() -> None:
    # асинхронный сервер доступен в модуле grpc.aio
    server = grpc.aio.server()

    # регистрируем сервис
    ping_pb2_grpc.add_PingServiceServicer_to_server(PingService(), server)  # type: ignore[no-untyped-call]
    server.add_insecure_port("[::]:50051")
    log.info("gRPC сервер запущен на порту 50051")

    # запуск
    await server.start()

    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        log.info("Остановка сервера...")
        # 5 секунд на graceful shutdown
        await server.stop(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Сервер прерван пользователем")
