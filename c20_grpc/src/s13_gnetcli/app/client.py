import asyncio
import base64
import logging
from collections.abc import AsyncIterator

import grpc
from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet
from grpc.aio import AioRpcError, Call
from grpc_reflection.v1alpha import reflection, reflection_pb2, reflection_pb2_grpc
from rich.logging import RichHandler

from c20_grpc.src.s12_reflection.app.pb import hello_pb2_grpc
from c20_grpc.src.s12_reflection.app.pb.hello_pb2 import HelloRequest, HelloResponse

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)

username = "mylogin"
password = "mysecret"

token = base64.b64encode(f"{username}:{password}".encode()).decode()
metadata = [("authorization", f"Basic {token}")]


async def main() -> None:
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        options=[
            ("grpc.primary_user_agent", "my-grpc-client/0.0.1"),
        ],
    ) as channel:
        stub = hello_pb2_grpc.HelloServiceStub(
            channel=channel,
        )
        calls: list[Call[HelloResponse]] = [
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


async def list_services() -> None:
    # запрос для получения списка сервисов. list_services - вернуть список всех сервисов
    async def request_generator() -> AsyncIterator[reflection_pb2.ServerReflectionRequest]:
        yield reflection_pb2.ServerReflectionRequest(list_services="")

    async with grpc.aio.insecure_channel(
        target="localhost:50051",
    ) as channel:
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        # рефлексия это bidir stream сервис, поэтому нужен асинхронный генератор сообщений
        # даже для одного сообщения
        response_stream = stub.ServerReflectionInfo(request_generator(), metadata=metadata)

        # поток ответов от сервера обрабатываем через цикл
        async for response in response_stream:
            services = response.list_services_response.service
            for s in services:
                log.info(f"Доступный сервис: {s.name}")


async def describe_service(service_name: str) -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)

        # file_containing_symbol - имя файла, в котором описан сервис
        async def request_generator():
            yield reflection_pb2.ServerReflectionRequest(file_containing_symbol=service_name)

        fds = FileDescriptorSet()

        async for response in stub.ServerReflectionInfo(request_generator()):
            file_descriptors = response.file_descriptor_response.file_descriptor_proto
            log.info(f"Сервис {service_name} описан в {len(file_descriptors)} proto-файлах.")
            # каждый дескриптор это серриализованный google.protobuf.descriptor_pb2.FileDescriptorProto
            # поэтому если нужно дальше смотреть, то нужно распаковать это сообщение
            for raw_fd in file_descriptors:
                fd = FileDescriptorProto.FromString(raw_fd)
                fds.file.append(fd)
                log.info(f"Имя файла {fd.name}")
                # log.info(f"Содержимое файла (дамп):\n{fd.SerializeToString()}")
                # log.info(f"Содержимое файла (человеческое):\n{fd}")

        # with open("srv.desc", "wb") as f:
        #     f.write(fds.SerializeToString())


if __name__ == "__main__":
    asyncio.run(list_services())
    # asyncio.run(describe_service("app.hello.v1.HelloService"))
