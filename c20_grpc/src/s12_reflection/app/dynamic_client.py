import asyncio
import logging
from collections.abc import AsyncIterator

import grpc
from google.protobuf import descriptor_pool
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.message_factory import GetMessageClass
from grpc_reflection.v1alpha import reflection_pb2_grpc
from grpc_reflection.v1alpha.reflection_pb2 import ServerReflectionRequest
from rich.logging import RichHandler

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
rh = RichHandler(markup=True, show_path=False, omit_repeated_times=False)
rh.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(rh)


async def list_services() -> AsyncIterator[ServerReflectionRequest]:
    yield ServerReflectionRequest(list_services="")


async def file_containing_symbol(service_name: str) -> AsyncIterator[ServerReflectionRequest]:
    yield ServerReflectionRequest(file_containing_symbol=service_name)


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        reflection_stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        response_stream = reflection_stub.ServerReflectionInfo(list_services())
        log.info("доступные сервисы")
        async for response in response_stream:
            for service in response.list_services_response.service:
                log.info(f"- {service.name}")

        # задаем имя сервиса
        service_name = "app.hello.v1.HelloService"
        # его дескрипторы
        response_stream = reflection_stub.ServerReflectionInfo(file_containing_symbol(service_name))
        # собираем дескрипторы в пул
        pool = descriptor_pool.DescriptorPool()
        async for response in response_stream:
            file_descriptors = response.file_descriptor_response.file_descriptor_proto
            for file_descriptor in file_descriptors:
                pool.Add(FileDescriptorProto.FromString(file_descriptor))

        # достаём типы сообщений
        hello_request_desc = pool.FindMessageTypeByName("app.hello.v1.HelloRequest")
        hello_response_desc = pool.FindMessageTypeByName("app.hello.v1.HelloResponse")

        # factory = message_factory.MessageFactory(pool)
        HelloRequest = GetMessageClass(hello_request_desc)
        HelloResponse = GetMessageClass(hello_response_desc)

        # создаём сообщение запроса
        request = HelloRequest(msg="hello", delay=2)
        # вызываем RPC динамически
        method = "/app.hello.v1.HelloService/Hello"
        stub = channel.unary_unary(
            method,
            request_serializer=request.SerializeToString,
            response_deserializer=HelloResponse.FromString,
        )

        log.info("отправляем запрос...")
        response = await stub(request)
        log.info("ответ от сервера:")
        log.info(response)


if __name__ == "__main__":
    asyncio.run(main())
