import asyncio
import subprocess
from random import randint

import grpc
from grpc.aio import Call

from c20_grpc.src.s04_async_client_server.app.pb import ping_pb2, ping_pb2_grpc


def show_tcp_sessions() -> None:
    lsof = subprocess.run(
        ["lsof", "-iTCP:50051"],  # noqa: S607
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    print(lsof.stdout)


async def main() -> None:
    # # один запрос
    # async with grpc.aio.insecure_channel(
    #     target="localhost:50051",
    # ) as channel:
    #     # show_tcp_sessions()
    #     # await channel.channel_ready()
    #     # show_tcp_sessions()

    #     stub = ping_pb2_grpc.PingServiceStub(channel)

    #     request = ping_pb2.PingRequest(target="example.com")
    #     call: Call = stub.Ping(request)
    #     response: ping_pb2.PingReply = await call
    #     # stub.Ping(request) возвращает Call объект (UnaryUnaryCall в нашем случае)
    #     # делая await call получаем PingReply, кроме этого у call объекта есть свои параметры,
    #     # например метаданные и пр (посмотрим позже)
    #     # если это не нужно, то можно сразу await ответа, без промежуточного call объекта
    #     # response = await stub.Ping(request)
    #     print(type(response))
    #     print("Ответ от сервера:", response)
    #     # show_tcp_sessions()

    # много запросов, вынесем в отдельную функцию
    async def make_request(num: int) -> None:
        await asyncio.sleep(randint(10, 100) / 100)
        await stub.Ping(ping_pb2.PingRequest(target=f"user-{num:02}"))

    async with grpc.aio.insecure_channel(
        target="localhost:50051",
    ) as channel:
        # show_tcp_sessions()
        # await channel.channel_ready()
        # show_tcp_sessions()

        stub = ping_pb2_grpc.PingServiceStub(channel)
        tasks = [make_request(i) for i in range(500)]
        print("запросы созданы")
        await asyncio.gather(*tasks)
        print("ответы получены")
        # show_tcp_sessions()


if __name__ == "__main__":
    asyncio.run(main())
