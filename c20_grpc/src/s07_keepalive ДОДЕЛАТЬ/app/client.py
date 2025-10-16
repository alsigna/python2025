import asyncio
import time

import grpc
from pb import ping_pb2, ping_pb2_grpc


async def main() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = ping_pb2_grpc.PingServiceStub(channel)

        tasks = [stub.Ping(ping_pb2.PingRequest(target=f"target-{i:02}")) for i in range(1)]
        print("запросы созданы")
        await asyncio.sleep(1)
        time.sleep(120)
        async for task in asyncio.as_completed(tasks):
            print(f"получен ответ на запрос {task.result().msg}")
        print("ответы получены")


if __name__ == "__main__":
    asyncio.run(main())
