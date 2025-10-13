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

log = logging.getLogger("app")

__all__ = ("ServerRequestTrackingInterceptor",)


class ServerRequestTrackingInterceptor(ServerInterceptor):
    def __init__(self):
        # контекст это read-only свойство, invocation_metadata - так же, поэтому для
        # хранения extra данных будем использовать отдельный словарь
        self._context_data: dict[str, Any] = {}

    # и сразу метод, который вернет набор этих данных для заданного контекста
    def get_context_data(
        self,
        context: ServicerContext[Message, Message],
    ) -> dict[str, Any]:
        return self._context_data.get(context, {})

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
            self._context_data[context] = {"start-time": start_time, "request-id": request_id}

            try:
                # передаем вызов реальному обработчику
                response = await real_handler.unary_unary(request, context)
            except Exception as exc:
                log.error(f"{request_id} ошибка обработки запроса. {exc.__class__.__name__}: {str(exc)}")
                raise
            else:
                # если все прошло без ошибок и ответ получен, то дополняем временем завершения
                end_time = datetime.now(tz=ZoneInfo("Europe/Moscow"))
                self._context_data[context]["end-time"] = end_time
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
            finally:
                # и в любом случае удаляем запись из словаря для завершенного запроса, иначе они будут копиться,
                # так как запрос завершен - контекст удаляется. Но у нас в словаре контекст используется как ключ,
                # т.е. на него остается ссылка и python не удаляет этот объект. Тут бы подошел weakref словарь, но
                # из-за особенностей реализации объект context не поддерживает слабые ссылки, поэтому в finally
                # вручную делаем pop
                self._context_data.pop(context, None)

        # сохраняем реальных хендлер, что бы вызвать обернуть его кастомным
        real_handler = await continuation(handler_call_details)
        custom_handler = grpc.unary_unary_rpc_method_handler(
            behavior=track_request,
            request_deserializer=real_handler.request_deserializer,
            response_serializer=real_handler.response_serializer,
        )
        return custom_handler
