import asyncio
import logging

import grpc
from pb_restored import server_pb2, server_pb2_grpc
from rich.logging import RichHandler

from .interceptors import ClientAuthInterceptor

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)

cmd = {
    "cmd": "show version",
    "host": "192.168.122.108",
    "host_params": {
        "credentials": {"login": "admin", "password": "P@ssw0rd"},
        "device": "cisco",
    },
    "string_result": True,
}


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        interceptors=[ClientAuthInterceptor("mylogin", "mysecret")],
    ) as channel:
        stub = server_pb2_grpc.GnetcliStub(channel)
        result: server_pb2.CMDResult = await stub.Exec(server_pb2.CMD(**cmd))
        print(result.out_str)


if __name__ == "__main__":
    asyncio.run(main())
