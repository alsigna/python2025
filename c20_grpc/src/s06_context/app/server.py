# кейсы:
# 1. когда клиент падает, а на сервере остаются его запросы, в примере делаем healthcheck через
#    context.send_initial_metadata(). НО metadata можно отправлять только один раз!
# 2. когда делаем return при переполнении очереди, то клиент падает. при этом уже поставленные задачи
#    продолжают обрабатываться, правим клиент, что бы он не падал

import asyncio
import logging
from asyncio import Queue
from dataclasses import dataclass
from datetime import datetime
from random import randint
from typing import Any, Generic, Protocol, TypeVar
from zoneinfo import ZoneInfo

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


T = TypeVar("T", bound=Message, contravariant=True)
R = TypeVar("R", bound=Message, covariant=True)


class Handler(Protocol[T, R]):
    @classmethod
    async def handle(cls, request: T) -> R: ...


@dataclass(frozen=True, slots=True)
class Task(Generic[T, R]):
    handler: type[Handler[T, R]]
    reply_queue: Queue[R]
    request: T
    context: ServicerContext[T, R]


request_queue: Queue[Task[Any, Any]] = Queue(maxsize=10)


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
            request_queue.put_nowait(Task(PingHandler, response_queue, request, context))
            log.info(f"запрос '{request.target}' помещен в очередь")
        except asyncio.QueueFull:
            log.info(f"запрос '{request.target}' отброшен")
            # # graceful завершение, когда нужно сказать клиенту о причинах
            # и отдать ту же структуру, что и при успешном ответе
            # context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
            # context.set_details("сервер перегружен")
            # return ping_pb2.PingReply(ok=False, msg="очередь переполнена")
            await context.abort(
                code=grpc.StatusCode.RESOURCE_EXHAUSTED,
                details="сервер перегружен",
            )

        # через context.send_initial_metadata мы делаем healthcheck клиента, если он провалился,
        # то grpc runtime видит это и пытается сделать отмену корутины (cancel), поэтому в эту
        # точку прилетает CanceledError
        return await response_queue.get()


# исходный код из прошлого примера
async def worker_v1(worker_id: int) -> None:
    log_prefix = f"worker-{worker_id:02}:"
    while True:
        task = await request_queue.get()
        log.info(f"{log_prefix} начал работы над запросом")
        try:
            result = await task.handler.handle(task.request)
            await task.reply_queue.put(result)
        finally:
            request_queue.task_done()


# добавили стартовую проверку через send_initial_metadata
async def worker_v2(worker_id: int) -> None:
    log_prefix = f"worker-{worker_id:02}:"
    while True:
        task = await request_queue.get()
        await asyncio.sleep(1)
        log.info(f"{log_prefix} получил новую задачу")

        # так делать бесполезно, не во всех ситуациях можно отловить отмену запроса
        if task.context.done():
            log.info(f"{log_prefix} отменил задачу: клиент уже не активен")
            continue

        try:
            # можно сделать попытку отправить метаданные
            await asyncio.wait_for(
                task.context.send_initial_metadata(()),
                timeout=0.2,
            )
        except Exception as exc:
            log.info(f"{log_prefix} запрос уже не активен. {exc.__class__.__name__} - {str(exc)}")
            # не делаем return, это завершит наш worker
            request_queue.task_done()
            continue

        log.info(f"{log_prefix} начал работы над запросом")
        try:
            result = await task.handler.handle(task.request)
            await task.reply_queue.put(result)
        finally:
            request_queue.task_done()


# воркер, который добавляем метаданные
async def worker_v3(worker_id: int) -> None:
    log_prefix = f"worker-{worker_id:02}:"
    while True:
        task = await request_queue.get()
        # метаданные, полученные от клиента:
        invocation_metadata = task.context.invocation_metadata()
        if invocation_metadata is not None:
            for key, value in invocation_metadata:
                log.debug(f"от клиента: {key}={value!r}")

        log.info(f"{log_prefix} начал работы над запросом")
        start_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        # отсылаем initial метаданные, от сервера к клиенту
        await task.context.send_initial_metadata(
            (("start-time", str(start_time)),),
        )
        log.info(f"{log_prefix} initial метаданные отправлены")
        try:
            result = await task.handler.handle(task.request)
            end_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
            # после завершения устанавливаем trailing метаданные
            task.context.set_trailing_metadata(
                (
                    ("end-time", str(end_time)),
                    ("worker", str(worker_id)),
                ),
            )
            log.info(f"{log_prefix} trailing метаданные установлены")
            # добавим details
            task.context.set_details("какое-то описание")
            await task.reply_queue.put(result)
        finally:
            request_queue.task_done()


async def main() -> None:
    # асинхронный сервер доступен в модуле grpc.aio
    server = grpc.aio.server()

    # регистрируем сервис
    ping_pb2_grpc.add_PingServiceServicer_to_server(PingService(), server)  # type: ignore[no-untyped-call]
    server.add_insecure_port("[::]:50051")
    log.info("gRPC сервер запущен на порту 50051")

    # запуск воркеров
    workers = [asyncio.create_task(worker_v3(i)) for i in range(2)]

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
