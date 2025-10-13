import asyncio

import grpc
from grpc.aio import Call

from c20_grpc.src.s06_context.app.pb import ping_pb2, ping_pb2_grpc


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
    ) as channel:
        stub = ping_pb2_grpc.PingServiceStub(channel)

        call: Call = stub.Ping(
            ping_pb2.PingRequest(target="target"),
        )
        result: ping_pb2.PingReply = await call

        print(await call.code())
        print(await call.details())
        print(await call.initial_metadata())
        print(await call.trailing_metadata())
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
