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
from asyncio import Queue
from random import randint
from typing import Protocol

import grpc
from google.protobuf.message import Message
from grpc.aio import ServicerContext
from pb import ping_pb2_grpc
from pb.ping_pb2 import PingReply, PingRequest
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


class Handler(Protocol):
    @classmethod
    async def handle(cls, request: Message) -> Message: ...


queue: Queue[tuple[type[Handler], Message, Queue[Message]]] = Queue(maxsize=10)


# логика отдельно
class PingHandler:
    @classmethod
    async def handle(cls, request: PingRequest) -> PingReply:
        await asyncio.sleep(randint(50, 200) / 100)
        log.info(f"запрос '{request.target}' обработан")
        return PingReply(
            ok=True,
            msg=f"ответ на запрос '{request.target}'",
        )


# gRPC сервер отдельно
class PingService(ping_pb2_grpc.PingServiceServicer):
    async def Ping(  # noqa: N802
        self,
        request: PingRequest,
        context: ServicerContext[PingRequest, PingReply],
    ) -> PingReply:
        # отдельная очередь для ответа именно на этот запрос
        response_queue: Queue[PingReply] = Queue(maxsize=1)

        try:
            queue.put_nowait((PingHandler, request, response_queue))  # type: ignore[arg-type]
            log.info(f"запрос '{request.target}' помещен в очередь")
        except asyncio.QueueFull:
            log.info(f"запрос '{request.target}' отброшен")
            context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
            context.set_details("сервер перегружен")
            return PingReply(ok=False, msg="очередь переполнена")

        # ждём результат от воркера
        return await response_queue.get()


async def worker(worker_id: int) -> None:
    while True:
        handler, request, response_queue = await queue.get()
        try:
            result = await handler.handle(request)
            await response_queue.put(result)
        finally:
            queue.task_done()


async def main() -> None:
    # асинхронный сервер доступен в модуле grpc.aio
    server = grpc.aio.server()

    # регистрируем сервис
    ping_pb2_grpc.add_PingServiceServicer_to_server(PingService(), server)  # type: ignore[no-untyped-call]
    server.add_insecure_port("[::]:50051")
    log.info("gRPC сервер запущен на порту 50051")

    # запуск воркеров
    workers = [asyncio.create_task(worker(i)) for i in range(5)]

    # запуск сервера
    await server.start()

    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        log.info("Остановка сервера...")
        # 5 секунд на graceful shutdown
        await server.stop(5)
        # стопаем воркеров
        for w in workers:
            w.cancel()
        # ждем пока воркеры будут завершены
        await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Сервер прерван пользователем")
