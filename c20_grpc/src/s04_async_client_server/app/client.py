import asyncio
import subprocess
from random import randint

import grpc
from grpc.aio import UnaryUnaryCall
from pb import ping_pb2_grpc
from pb.ping_pb2 import PingReply, PingRequest


def show_tcp_sessions() -> None:
    lsof = subprocess.run(  # noqa: S603
        ["lsof", "-iTCP:50051"],  # noqa: S607
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    print(lsof.stdout)


async def main_single() -> None:
    # один запрос
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
    ) as channel:
        # show_tcp_sessions()
        # await channel.channel_ready()
        # show_tcp_sessions()

        stub = ping_pb2_grpc.PingServiceStub(channel)  # type: ignore[no-untyped-call]

        request = PingRequest(target="example.com")
        call: UnaryUnaryCall[PingRequest, PingReply] = stub.Ping(request)
        response: PingReply = await call
        # stub.Ping(request) возвращает Call объект (UnaryUnaryCall в нашем случае)
        # делая await call получаем PingReply, кроме этого у call объекта есть свои параметры,
        # например метаданные и пр (посмотрим позже)
        # если это не нужно, то можно сразу await ответа, без промежуточного call объекта
        # response = await stub.Ping(request)
        print(type(response))
        print("Ответ от сервера:", response)
        # show_tcp_sessions()


async def main_multi() -> None:

    # много запросов, вынесем в отдельную функцию
    async def make_request(num: int) -> None:
        await asyncio.sleep(randint(10, 100) / 100)
        await stub.Ping(PingRequest(target=f"user-{num:02}"))

    async with grpc.aio.insecure_channel(
        target="localhost:50051",
    ) as channel:
        # show_tcp_sessions()
        # await channel.channel_ready()
        # show_tcp_sessions()

        stub = ping_pb2_grpc.PingServiceStub(channel)  # type: ignore[no-untyped-call]
        tasks = [make_request(i) for i in range(500)]
        print("запросы созданы")
        await asyncio.gather(*tasks)
        print("ответы получены")
        # show_tcp_sessions()


if __name__ == "__main__":
    # asyncio.run(main_single())
    asyncio.run(main_multi())
