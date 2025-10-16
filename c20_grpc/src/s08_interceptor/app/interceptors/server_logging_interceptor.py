import logging
import time
from collections.abc import Awaitable, Callable

import grpc
from google.protobuf.message import Message
from grpc import HandlerCallDetails, RpcMethodHandler
from grpc.aio import ServerInterceptor, ServicerContext

log = logging.getLogger("app")

__all__ = (
    "ServerLoggingInterceptor",
    "ServerLoggingInterceptorV2",
)


# простой интерцептор для логирования
class ServerLoggingInterceptor(ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Callable[
            [HandlerCallDetails],
            Awaitable[RpcMethodHandler],
        ],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        # в handler_call_details есть метадата и rpc метод:
        # handler_call_details.invocation_metadata
        # handler_call_details.method
        log.debug(f"[LoggingServerInterceptor] новый запрос, method={handler_call_details.method}")
        log.debug(f"[LoggingServerInterceptor] новый запрос, metadata={handler_call_details.invocation_metadata}")
        return await continuation(handler_call_details)


# расширенный интерцептор для логирования
class ServerLoggingInterceptorV2(ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Callable[
            [HandlerCallDetails],
            Awaitable[RpcMethodHandler],
        ],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        async def logging_wrapper(
            request: Message,
            context: ServicerContext[Message, Message],
        ):
            t0 = time.perf_counter()
            try:
                response = await original_unary_unary(request, context)
                status = context.code() or grpc.StatusCode.OK
                return response
            except grpc.RpcError as exc:
                status = exc.code()
                log.exception(f"[LoggingServerInterceptorV2] ошибка при вызове {method}: {exc}")
                raise
            finally:
                elapsed = time.perf_counter() - t0
                log.info(f"[LoggingServerInterceptorV2] вызов {method} завершён за {elapsed:.2f} сек ({status.name})")

        method = handler_call_details.method
        metadata = dict(handler_call_details.invocation_metadata or [])

        log.debug(f"[LoggingServerInterceptorV2] новый запрос, method={method}")
        log.debug(f"[LoggingServerInterceptorV2] новый запрос, metadata={metadata}")

        handler = await continuation(handler_call_details)

        # для примера берем только unary_unary, все остальное как есть пропускаем
        if not handler.unary_unary:
            return handler

        original_unary_unary = handler.unary_unary
        return grpc.unary_unary_rpc_method_handler(
            behavior=logging_wrapper,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )
