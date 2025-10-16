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
        log.info(f"новый запрос: '{request.target}'")
        ok, msg = await PingHandler().handle(request.target)
        return PingReply(ok=ok, msg=msg)


async def main() -> None:
    server = grpc.aio.server(
        options=[
            ("grpc.keepalive_time_ms", 5000),  # отправляем keepalive каждые 5 секунд
            ("grpc.keepalive_timeout_ms", 2000),  # ждем ответ 2 секунд
            ("grpc.keepalive_permit_without_calls", True),  # отправлять keepalive даже без активных rpc
            ("grpc.http2.max_pings_without_data", 2),  # максимум keepalive без ответов
            ("grpc.http2.min_time_between_pings_ms", 5000),  # интервал между keepalive
            ("grpc.http2.min_ping_interval_without_data_ms", 2000),  # интервал в отсутствии обмена
            ("grpc.max_connection_idle_ms", 15000),  # время бездействия соединения
            ("grpc.max_connection_age_ms", 120000),  # время жизни соединения (даже активного)
            ("grpc.max_connection_age_grace_ms", 5000),  # грейс период для закрытия сессии
        ],
    )
    ping_pb2_grpc.add_PingServiceServicer_to_server(PingService(), server)  # type: ignore[no-untyped-call]
    server.add_insecure_port("[::]:50051")
    log.info("gRPC сервер запущен на порту 50051")

    await server.start()

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
