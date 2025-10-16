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
from asyncio import Protocol, Queue
from dataclasses import dataclass
from datetime import datetime
from random import randint
from zoneinfo import ZoneInfo

import grpc
from google.protobuf.message import Message
from pb import ping_pb2, ping_pb2_grpc
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(
    markup=True,
    show_path=False,
    omit_repeated_times=True,
    rich_tracebacks=True,
)
rh.setFormatter(
    logging.Formatter(
        fmt="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ),
)
log.addHandler(rh)


class Handler(Protocol):
    async def handle(self, request: Message) -> Message: ...


@dataclass(frozen=True, slots=True)
class Task:
    handler: Handler
    reply_queue: Queue
    request: Message
    context: grpc.aio.ServicerContext


request_queue: Queue[Task] = Queue(maxsize=10)


# логика отдельно
class PingHandler:
    @classmethod
    async def handle(cls, request: ping_pb2.PingRequest) -> ping_pb2.PingReply:
        log.info(f"запрос '{request.target}' начал обрабатываться")
        await asyncio.sleep(2)
        # await asyncio.sleep(randint(50, 200) / 100)
        log.info(f"запрос '{request.target}' обработан")
        return ping_pb2.PingReply(
            ok=True,
            msg=f"ответ на запрос '{request.target}'",
        )


# gRPC сервер отдельно
class PingService(ping_pb2_grpc.PingServiceServicer):
    async def Ping(  # noqa: N802
        self,
        request: ping_pb2.PingRequest,
        context: grpc.aio.ServicerContext,
    ) -> ping_pb2.PingReply:
        response_queue: Queue[ping_pb2.PingReply] = Queue(maxsize=1)
        await request_queue.put(Task(PingHandler, response_queue, request, context))
        log.info(f"запрос '{request.target}' помещен в очередь")
        result = await response_queue.get()
        return result


async def worker(worker_id: int) -> None:
    log_prefix = f"worker-{worker_id:02}:"
    while True:
        task = await request_queue.get()
        log.info(f"{log_prefix} начал работы над запросом {task.request.target}")
        try:
            result = await task.handler.handle(task.request)
            await task.reply_queue.put(result)
        finally:
            request_queue.task_done()


async def main() -> None:
    # асинхронный сервер доступен в модуле grpc.aio
    server = grpc.aio.server()

    # регистрируем сервис
    ping_pb2_grpc.add_PingServiceServicer_to_server(PingService(), server)
    server.add_insecure_port("[::]:50051")
    log.info("gRPC сервер запущен на порту 50051")

    # запуск воркеров
    workers = [asyncio.create_task(worker(i)) for i in range(2)]

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
