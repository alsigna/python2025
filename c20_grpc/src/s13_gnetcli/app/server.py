r"""async сервер, генерация proto.

python -m grpc_tools.protoc \
  --proto_path=./proto \
  --python_out=./app/pb \
  --grpc_python_out=./app/pb \
  --mypy_out=./app/pb \
  ./proto/*

python -m grpc_tools.protoc \
  --proto_path=. \
  --descriptor_set_in=srv.desc \
  --python_out=./restored \
  --grpc_python_out=./restored \
  hello.proto
"""

import asyncio
import logging

import grpc
from grpc.aio import ServicerContext
from grpc_reflection.v1alpha import reflection
from rich.logging import RichHandler

from c20_grpc.src.s12_reflection.app.pb import hello_pb2, hello_pb2_grpc

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


class HelloHandler:
    @classmethod
    async def handle(
        cls,
        request: hello_pb2.HelloRequest,
        context: ServicerContext[hello_pb2.HelloRequest, hello_pb2.HelloResponse],
    ) -> hello_pb2.HelloResponse:
        log.info(f"запрос '{request.msg}' начал обрабатываться")
        await asyncio.sleep(request.delay)
        log.info(f"запрос '{request.msg}' обработан")
        return hello_pb2.HelloResponse(
            msg=request.msg,
            delay=request.delay,
            status=hello_pb2.HelloResponse.Status.STATUS_OK,
        )


class HelloService(hello_pb2_grpc.HelloServiceServicer):
    async def Hello(  # noqa: N802
        self,
        request: hello_pb2.HelloRequest,
        context: ServicerContext[hello_pb2.HelloRequest, hello_pb2.HelloResponse],
    ) -> hello_pb2.HelloRequest:
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
        # app.hello.v1.HelloService или из переменных вытащить
        hello_pb2.DESCRIPTOR.services_by_name["HelloService"].full_name,
        # и сам сервис рефлексии добавляем grpc.reflection.v1alpha.ServerReflection или из переменной
        reflection.SERVICE_NAME,
    )
    # включаем рефлексию на сервисе
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
