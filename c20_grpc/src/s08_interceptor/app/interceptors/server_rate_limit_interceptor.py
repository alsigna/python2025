import asyncio
import logging
import time
from collections.abc import Awaitable, Callable

import grpc
from google.protobuf.message import Message
from grpc import HandlerCallDetails, RpcMethodHandler
from grpc.aio import ServerInterceptor, ServicerContext

log = logging.getLogger("app")

__all__ = ("ServerRateLimitInterceptor",)


# пример рейт-лимитера на база корзины с токенами
class ServerRateLimitInterceptor(ServerInterceptor):
    def __init__(self, max_requests_per_sec: int):
        # максимальная емкость, она же скорость наполнения корзины
        self.max_requests = max_requests_per_sec * 1.05
        # сколько сейчас осталось токенов, на старте корзина полная
        self.current_tokens = float(max_requests_per_sec)
        # когда последний раз обновляли корзину
        self.last_check = time.monotonic()
        # корзина это общий ресурс, поэтому делаем с lock, что бы не было гонок
        self.lock = asyncio.Lock()

    # кастомный хендлер для сброса сессии
    async def drop_due_to_rate_limit(
        self,
        request: Message,
        context: ServicerContext[Message, Message],
    ) -> Message:
        await context.abort(
            code=grpc.StatusCode.RESOURCE_EXHAUSTED,
            details=f"превышен rate-limit сообщений: {int(self.max_requests)} в секунду",
        )

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        async with self.lock:
            # считаем сколько времени прошло с прошлого запроса
            now = time.monotonic()
            elapsed = now - self.last_check
            self.last_check = now
            # наполняем корзину токенами за прошедшее время
            self.current_tokens += elapsed * self.max_requests
            # и проверяем, что бы за максимум не вылезли
            if self.current_tokens > self.max_requests:
                self.current_tokens = float(self.max_requests)

            # если токенов не хватает, то отбиваем с ошибкой через кастомный хендлер
            if self.current_tokens < 1.0:
                log.warning(f"rate-limit превышен, {self.current_tokens=:.04f}")
                return grpc.unary_unary_rpc_method_handler(
                    behavior=self.drop_due_to_rate_limit,
                )
            # иначе уменьшаем количество токенов на 1 и передаем дальше на обработку
            else:
                self.current_tokens -= 1.0
        # саму дальнейшую обработку делаем вне lock, что бы не получить блокировку кода
        return await continuation(handler_call_details)
