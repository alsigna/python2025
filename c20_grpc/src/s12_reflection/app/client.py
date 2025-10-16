import asyncio
import logging

import grpc
from grpc.aio import AioRpcError, UnaryUnaryCall
from pb_restored import hello_pb2_grpc
from pb_restored.hello_pb2 import HelloRequest, HelloResponse
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        options=[("grpc.primary_user_agent", "my-grpc-client/0.0.1")],
    ) as channel:
        stub = hello_pb2_grpc.HelloServiceStub(channel)
        # тут на самом деле list[Call] будет, но Call не наследуется от Awaitable
        # и mypy не знает, что Call это awaitable объект и дальше будет ругаться
        # поэтому делаем более общую аннотацию вместо list[Awaitable[HelloResponse]],
        # либо от указываем как ниже сделано, потому что UnaryUnaryCall реализует __await__
        calls: list[UnaryUnaryCall[HelloRequest, HelloResponse]] = [
            stub.Hello(
                HelloRequest(msg=f"user-{i:02}", delay=i),
            )
            for i in range(1, 2)
        ]
        log.info("все запросы созданы")
        async for call in asyncio.as_completed(calls):
            try:
                result = await call
            except AioRpcError as exc:
                log.error(f"ошибка в запросе. {exc.code()}, {exc.details()}")
            else:
                log.info(f"получен ответ на запрос: {result.msg=} / {result.delay=} / {result.status=}")
        log.info("все ответы получены")


if __name__ == "__main__":
    asyncio.run(main())
