import logging
import uuid
from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import grpc
from google.protobuf.message import Message
from grpc import HandlerCallDetails, RpcMethodHandler
from grpc.aio import ServerInterceptor, ServicerContext

__all__ = ("ServerRequestTrackingInterceptorV2",)

log = logging.getLogger("app")


# либо тоже самое через обертку контекста
class ContextWrapper:
    def __init__(self, context: ServicerContext[Message, Message], **extra: str) -> None:
        self._context = context
        self._extra = extra

    def __getattr__(self, item: Any) -> Any:
        if item in self._extra:
            return self._extra[item]
        return getattr(self._context, item)

    def __setattr__(self, key: str, value: Any) -> None:
        if key in ("_context", "_extra"):
            super().__setattr__(key, value)
        else:
            self._extra[key] = value


class ServerRequestTrackingInterceptorV2(ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        async def track_request(
            request: Message,
            context: ServicerContext[Message, Message],
        ) -> Message:
            # генерируем/заполняем данные о запросе
            start_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
            request_id = str(uuid.uuid4())

            wrapped_context = ContextWrapper(
                context=context,
                request_id=request_id,
                start_time=start_time,
            )

            try:
                # передаем вызов реальному обработчику
                response = await real_handler.unary_unary(request, wrapped_context)
            except Exception as exc:
                log.error(f"{request_id} ошибка обработки запроса. {exc.__class__.__name__}: {str(exc)}")
                raise
            else:
                # если все прошло без ошибок и ответ получен, то дополняем временем завершения
                end_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
                wrapped_context.end_time = end_time
                # и заодно устанавливаем trailing_metadata
                context.set_trailing_metadata(
                    [
                        ("request-id", request_id),
                        ("start-time", str(start_time)),
                        ("end-time", str(end_time)),
                    ],
                )
                # отдаем ответ дальше по стеку
                return response

        # сохраняем реальных хендлер, что бы вызвать обернуть его кастомным
        real_handler = await continuation(handler_call_details)
        custom_handler = grpc.unary_unary_rpc_method_handler(
            behavior=track_request,
            request_deserializer=real_handler.request_deserializer,
            response_serializer=real_handler.response_serializer,
        )
        return custom_handler
