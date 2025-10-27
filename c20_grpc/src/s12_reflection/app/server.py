import asyncio
import logging

import grpc
from grpc.aio import ServicerContext
from grpc_reflection.v1alpha import reflection
from pb import hello_pb2_grpc
from pb.hello_pb2 import DESCRIPTOR as HELLO_DESCRIPTOR
from pb.hello_pb2 import HelloRequest, HelloResponse
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


class HelloHandler:
    @classmethod
    async def handle(
        cls,
        request: HelloRequest,
        context: ServicerContext[HelloRequest, HelloResponse],
    ) -> HelloResponse:
        log.info(f"запрос '{request.msg}' начал обрабатываться")
        await asyncio.sleep(request.delay)
        log.info(f"запрос '{request.msg}' обработан")
        return HelloResponse(
            msg=request.msg,
            delay=request.delay,
            status=HelloResponse.Status.STATUS_OK,
        )


class HelloService(hello_pb2_grpc.HelloServiceServicer):
    async def Hello(  # noqa: N802
        self,
        request: HelloRequest,
        context: ServicerContext[HelloRequest, HelloResponse],
    ) -> HelloResponse:
        return await HelloHandler.handle(request, context)


async def main() -> None:
    server = grpc.aio.server()
    hello_pb2_grpc.add_HelloServiceServicer_to_server(
        servicer=HelloService(),
        server=server,
    )

    # формируем кортеж с именами сервисов
    services = (
        # наши бизнес-сервисы
        # "app.hello.v1.HelloService",
        #   или из переменных вытащить
        HELLO_DESCRIPTOR.services_by_name["HelloService"].full_name,
        # и сам сервис рефлексии добавляем grpc.reflection.v1alpha.ServerReflection или из переменной
        reflection.SERVICE_NAME,
    )
    # включаем рефлексию на сервере
    reflection.enable_server_reflection(
        service_names=services,
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
        # 5 секунд на graceful shutdown
        await server.stop(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Сервер прерван пользователем")
