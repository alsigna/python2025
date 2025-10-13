import asyncio
from random import randint

import grpc

from c20_grpc.src.s05_async_server_limit.app.pb import ping_pb2, ping_pb2_grpc


async def main() -> None:
    # один запрос
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
    ) as channel:
        stub = ping_pb2_grpc.PingServiceStub(channel)
        request = ping_pb2.PingRequest(target="example.com")
        response = await stub.Ping(request)
        print("Ответ от сервера:", response)

    # ===============
    # много запросов
    async def make_request(num: int) -> None:
        await asyncio.sleep(randint(10, 100) / 100)
        target = f"user-{num:02}"
        try:
            await stub.Ping(ping_pb2.PingRequest(target=target))
        except grpc.aio.AioRpcError:
            print(f"ошибка в запросе {target}")

    async with grpc.aio.insecure_channel(
        target="localhost:50051",
    ) as channel:
        stub = ping_pb2_grpc.PingServiceStub(channel)
        tasks = [make_request(i) for i in range(50)]
        print("запросы созданы")
        await asyncio.gather(*tasks)
        print("ответы получены")


if __name__ == "__main__":
    asyncio.run(main())
