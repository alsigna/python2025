r"""восстановление из бинарного дампа.

python -m grpc_tools.protoc \
  --proto_path=./proto_restored \
  --descriptor_set_in=./proto_restored/server.desc \
  --python_out=./pb_restored \
  --mypy_out=./pb_restored \
  --grpc_python_out=./pb_restored \
  hello.proto

sed -i '' 's/^import \([^ ]*\)_pb2 as \([^ ]*\)__pb2/from . import \1_pb2 as \2__pb2/' ./pb_restored/*_pb2_grpc.py
"""

import asyncio
import logging
from collections.abc import AsyncIterator

import grpc
from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet
from grpc_reflection.v1alpha import reflection_pb2_grpc
from grpc_reflection.v1alpha.reflection_pb2 import ServerReflectionRequest, ServerReflectionResponse
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


async def list_services() -> None:
    # запрос для получения списка сервисов. list_services - вернуть список всех сервисов
    async def request_generator() -> AsyncIterator[ServerReflectionRequest]:
        yield ServerReflectionRequest(list_services="")

    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        # рефлексия это bidir stream сервис, поэтому нужен асинхронный генератор сообщений
        # даже для одного сообщения
        response_stream: AsyncIterator[ServerReflectionResponse] = stub.ServerReflectionInfo(request_generator())
        # поток ответов от сервера обрабатываем через цикл
        async for response in response_stream:
            for service in response.list_services_response.service:
                log.info(f"доступное имя сервиса: {service.name}")


async def describe_service(service_name: str) -> None:
    # file_containing_symbol - имя файла, в котором описан сервис
    async def request_generator() -> AsyncIterator[ServerReflectionRequest]:
        yield ServerReflectionRequest(file_containing_symbol=service_name)

    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        fds = FileDescriptorSet()
        response_stream: AsyncIterator[ServerReflectionResponse] = stub.ServerReflectionInfo(request_generator())
        async for response in response_stream:
            file_descriptors = response.file_descriptor_response.file_descriptor_proto
            log.info(f"Сервис {service_name} описан в {len(file_descriptors)} proto-файлах.")
            # каждый дескриптор это серриализованный google.protobuf.descriptor_pb2.FileDescriptorProto
            # поэтому если нужно дальше смотреть, то нужно распаковать это сообщение
            for raw_fd in file_descriptors:
                fd = FileDescriptorProto.FromString(raw_fd)
                fds.file.append(fd)
                log.info(f"Имя файла {fd.name}")
                log.info(f"Содержимое файла (дамп):\n{fd.SerializeToString()}")
                log.info(f"Содержимое файла (человеческое):\n{fd}")
        # если нужно восстановить proto файлы, то сохраняем
        with open("./proto_restored/server.desc", "wb") as f:
            f.write(fds.SerializeToString())


if __name__ == "__main__":
    # asyncio.run(list_services())
    asyncio.run(describe_service("app.hello.v1.HelloService"))
