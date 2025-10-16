import asyncio

import grpc
from grpc.aio import UnaryUnaryCall
from pb import ping_pb2_grpc
from pb.ping_pb2 import PingReply, PingRequest


async def main() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = ping_pb2_grpc.PingServiceStub(channel)  # type: ignore[no-untyped-call]

        call: UnaryUnaryCall[PingRequest, PingReply] = stub.Ping(
            PingRequest(target="target"),
        )
        result: PingReply = await call

        print(await call.code())
        print(await call.details())
        print(await call.initial_metadata())
        print(await call.trailing_metadata())
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
