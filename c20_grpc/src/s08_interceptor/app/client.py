import asyncio
import time
from collections.abc import Awaitable, Callable
from random import randint
from typing import TypeVar

import grpc
from google.protobuf.message import Message
from grpc.aio import (
    AioRpcError,
    Call,
    ClientCallDetails,
    ClientInterceptor,
    UnaryUnaryCall,
    UnaryUnaryClientInterceptor,
)
from pb import hello_pb2_grpc
from pb.hello_pb2 import HelloRequest, HelloResponse

Request = TypeVar("Request", bound=Message)
Response = TypeVar("Response", bound=Message)


def log(msg: str) -> None:
    print(f"{time.perf_counter() - t0:.3f} сек: - {msg}")


class LoggingClientInterceptor(UnaryUnaryClientInterceptor):  # type: ignore[type-arg]
    async def intercept_unary_unary(
        self,
        continuation: Callable[
            [ClientCallDetails, Request],
            Awaitable[UnaryUnaryCall[Request, Response]],
        ],
        client_call_details: ClientCallDetails,
        request: Request,
    ) -> Response:
        log(
            f"[LoggingClientInterceptor] запрос, method: {client_call_details.method}, "
            f"metadata: {client_call_details.metadata}",
        )
        # continuation возвращает корутину на UnaryUnaryCall
        call = await continuation(client_call_details, request)
        log("[LoggingClientInterceptor] call получен")
        # UnaryUnaryCall реализует __await__, поэтому и его можем ожидать
        response = await call
        log("[LoggingClientInterceptor] response получен")
        initial_metadata = await call.initial_metadata()
        trailing_metadata = await call.trailing_metadata()

        log(f"[LoggingClientInterceptor] ответ, method={client_call_details.method}: {initial_metadata=}")
        log(f"[LoggingClientInterceptor] ответ, method={client_call_details.method}: {trailing_metadata=}")

        return response


class RandomDelayInterceptor(UnaryUnaryClientInterceptor):  # type: ignore[type-arg]
    async def intercept_unary_unary(
        self,
        continuation: Callable[
            [ClientCallDetails, Request],
            Awaitable[UnaryUnaryCall[Request, Response]],
        ],
        client_call_details: ClientCallDetails,
        request: Request,
    ) -> Response:
        await asyncio.sleep(randint(2, 15) / 10)
        return await continuation(client_call_details, request)


class CustomMetadataInterceptor(UnaryUnaryClientInterceptor):  # type: ignore[type-arg]
    async def intercept_unary_unary(
        self,
        continuation: Callable[
            [ClientCallDetails, Request],
            Awaitable[UnaryUnaryCall[Request, Response]],
        ],
        client_call_details: ClientCallDetails,
        request: Request,
    ) -> Response:
        custom_metadata = []
        for metadata in client_call_details.metadata:
            if metadata[0] != "user-agent":
                custom_metadata.append(metadata)

        # и такой вариант тоже не подходит, так как стандартные заголовки добавляются
        # после работы интерцепторов, поэтому они перепишут назначаемое тут значение
        custom_metadata.append(("user-agent", "my-grpc-client/0.0.2"))

        updated_call_details = ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=custom_metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
        )
        return await continuation(updated_call_details, request)


class RateLimitInterceptor(UnaryUnaryClientInterceptor):  # type: ignore[type-arg]
    def __init__(self, max_requests: int):
        self.max_requests = max_requests
        self.current_tokens = max_requests
        self.last_check = time.monotonic()
        self.lock = asyncio.Lock()

    async def intercept_unary_unary(
        self,
        continuation: Callable[
            [ClientCallDetails, Request],
            Awaitable[UnaryUnaryCall[Request, Response]],
        ],
        client_call_details: ClientCallDetails,
        request: Request,
    ) -> Response:
        def update_tokens() -> None:
            # считаем сколько времени прошло с прошлого запроса
            now = time.monotonic()
            elapsed = now - self.last_check
            self.last_check = now

            # наполняем корзину токенами за прошедшее время
            self.current_tokens += elapsed * self.max_requests
            # и проверяем, что бы за максимум не вылезли
            if self.current_tokens > self.max_requests:
                self.current_tokens = float(self.max_requests)

        async with self.lock:
            update_tokens()

            # если токенов не хватает, то спим столько времени, что бы накопилось до одного токена
            if self.current_tokens < 1.0:
                # 1.0 - self.current_tokens - сколько токенов осталось
                # self.max_requests - скорость восполнения токенов (токенов/сек)
                # (1.0 - self.current_tokens) / self.max_requests - столько нужно подождать, что бы добить до 1
                delay = (1.0 - self.current_tokens) / self.max_requests
                log(f"{self.current_tokens=:.04f}, {delay=:.04f}")
                await asyncio.sleep(delay)
                update_tokens()

            # уменьшаем число токенов
            self.current_tokens -= 1.0
        # и делаем запрос за рамками lock
        return await continuation(client_call_details, request)


async def main() -> None:
    invocation_metadata = [
        ("client-version", "0.0.1"),
        # в grpc клиентские метаданные дополняют стандартные, а не заменяют их, поэтому установка тут
        # user-agent ни к чему не приведет, на сервере все равно будет стандартные
        ("user-agent", "my-grpc-client"),
    ]
    interceptors: list[ClientInterceptor] = [
        RandomDelayInterceptor(),
        RateLimitInterceptor(3),
        LoggingClientInterceptor(),
        CustomMetadataInterceptor(),
    ]
    async with grpc.aio.insecure_channel(
        target="localhost:50051",
        interceptors=interceptors,
        # поэтому переписываем user-agent во время создания канала через опции. Или используем другие названия
        # хедеров, типа x-user-agent
        # options=[
        #     ("grpc.primary_user_agent", "my-grpc-client/0.0.1"),
        # ],
    ) as channel:
        stub = hello_pb2_grpc.HelloServiceStub(
            channel=channel,
        )
        calls: list[Call[HelloResponse]] = [
            stub.Hello(
                HelloRequest(msg=f"user-{i:02}", delay=i),
                metadata=invocation_metadata,
            )
            for i in range(1, 11)
        ]
        log("все запросы созданы")
        async for call in asyncio.as_completed(calls):
            try:
                result = await call
            except AioRpcError as exc:
                log(f"ошибка в запросе. {exc.code()}, {exc.details()}")
            else:
                log(f"получен ответ на запрос: {result.msg=} / {result.delay=} / {result.status=}")
        log("все ответы получены")


if __name__ == "__main__":
    t0 = time.perf_counter()
    asyncio.run(main())
