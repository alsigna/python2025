import logging
from collections.abc import Awaitable, Callable

from grpc import HandlerCallDetails, RpcMethodHandler
from grpc.aio import ServerInterceptor

log = logging.getLogger("app")

__all__ = ("ServerLoggingInterceptor",)


# простой интерцептор для логирования
class ServerLoggingInterceptor(ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        # в handler_call_details есть метадата и rpc метод:
        # handler_call_details.invocation_metadata
        # handler_call_details.method
        log.debug(f"[LoggingServerInterceptor] получен запрос для method={handler_call_details.method}")
        log.debug(f"[LoggingServerInterceptor] получен запрос для method={handler_call_details.invocation_metadata}")
        return await continuation(handler_call_details)
