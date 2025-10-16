import asyncio
import subprocess
import time

import grpc
from pb import ping_pb2, ping_pb2_grpc


def show_tcp_sessions() -> None:
    lsof = subprocess.run(  # noqa: S603
        ["lsof", "-iTCP:50051"],  # noqa: S607
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    print(lsof.stdout)


async def main() -> None:
    async with grpc.aio.insecure_channel(
        "localhost:50051",
        options=[
            ("grpc.keepalive_time_ms", 0),  # 0 = не шлёт ping
        ],
    ) as channel:
        show_tcp_sessions()
        await channel.channel_ready()
        show_tcp_sessions()
        for i in range(30):
            print(f"{i:02} сек")
            show_tcp_sessions()
            time.sleep(1)
        show_tcp_sessions()


if __name__ == "__main__":
    asyncio.run(main())
