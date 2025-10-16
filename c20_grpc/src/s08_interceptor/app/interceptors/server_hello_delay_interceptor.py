import logging
from collections.abc import Awaitable, Callable

import grpc
from grpc import HandlerCallDetails, RpcMethodHandler
from grpc.aio import ServerInterceptor, ServicerContext
from pb.hello_pb2 import HelloRequest, HelloResponse

log = logging.getLogger("app")


__all__ = ("ServerHelloDelayInterceptor",)


# если в запросах к Hello есть delay <= 0, то отвечаем через интерцептор, а не дергаем метод сервисера
class ServerHelloDelayInterceptor(ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        next_handler = await continuation(handler_call_details)
        # если запрос не к Hello, то пропускаем его
        if not handler_call_details.method.endswith("/Hello"):
            return next_handler

        # в серверном интерцепторе есть доступ только к имени сервиса и метаданным, поэтому, что бы
        # извлечь сам запрос и проверить в нем какие-либо поля, нужно сделать искусственный обработчик
        # по сути тоже самое, что мы делали в сервисере, только в нем async def Hello автоматически оборачивался
        # в хендлер, а нам придется это руками сделать. Поэтому создаем обработчик, такая же функция как и
        # async def Hello в сервисере в котором можно уже реализовывать какую-то логику на базе проверок запроса
        # её можно реализовать как отдельную функцию в классе (в следующем примере) так и как вложенную функцию
        async def custom_handler(
            request: HelloRequest,
            context: ServicerContext[HelloRequest, HelloResponse],
        ) -> HelloResponse:
            log.debug(f"[ValidateHelloDelayInterceptor] запрос в custom_handler: {request.msg=}, {request.delay=}")
            if request.delay <= 0:
                log.debug("[ValidateHelloDelayInterceptor] сброс запроса из-за delay <= 0")
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "delay должен быть > 0",
                )
            log.debug("[ValidateHelloDelayInterceptor] запрос с delay > 0 отправлен на обработку")
            return await next_handler.unary_unary(request, context)

        # и делаем хендлер вокруг нее, указывая как разбирать/собирать запросы
        rpc_method_handler = grpc.unary_unary_rpc_method_handler(
            behavior=custom_handler,
            request_deserializer=next_handler.request_deserializer,
            response_serializer=next_handler.response_serializer,
        )
        return rpc_method_handler
