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

import grpc
from grpc.aio import ServicerContext
from pb import hello_pb2_grpc
from pb.hello_pb2 import HelloRequest, HelloResponse
from rich.logging import RichHandler

from .interceptors import (
    ServerHelloDelayInterceptor,
    ServerLoggingInterceptor,
    ServerRateLimitInterceptor,
    ServerRequestTrackingInterceptor,
    ServerRequestTrackingInterceptorV2,
)

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


# поскольку нам нужно состояние хранить, то мы создаем интерцептор глобально, а не в момент
# объявления сервера
# request_tracking_interceptor = ServerRequestTrackingInterceptor()


class HelloHandler:
    @classmethod
    async def handle(
        cls,
        request: HelloRequest,
        context: ServicerContext[HelloRequest, HelloResponse],
    ) -> HelloResponse:
        # это для ServerRequestTrackingInterceptor
        # context_data = request_tracking_interceptor.get_context_data(context)
        # request_id = context_data.get("request-id")
        # это для ServerRequestTrackingInterceptorV2
        request_id = context.request_id
        log.info(f"{request_id}: запрос '{request.msg}' начал обрабатываться")
        await asyncio.sleep(request.delay)
        log.info(f"{request_id}: запрос '{request.msg}' обработан")
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
    ) -> HelloRequest:
        return await HelloHandler.handle(request, context)


async def main() -> None:
    server = grpc.aio.server(
        interceptors=[
            ServerRateLimitInterceptor(3),
            # request_tracking_interceptor,
            ServerRequestTrackingInterceptorV2(),
            ServerLoggingInterceptor(),
            ServerHelloDelayInterceptor(),
        ],
    )
    hello_pb2_grpc.add_HelloServiceServicer_to_server(
        servicer=HelloService(),
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
