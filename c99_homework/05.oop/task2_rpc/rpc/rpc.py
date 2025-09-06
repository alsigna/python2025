import time
from types import TracebackType
from typing import Literal, Self

from redis import Redis
from rq import Queue

from .rpc_method import RPCMethod
from .rpc_result import RPCResult


class RPC:
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_password: str | None = None,
    ) -> None:
        self._redis = Redis(redis_host, redis_port, redis_db, redis_password)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self._redis.close()
        return False

    def __getattr__(self, name: str) -> RPCMethod:
        queue = Queue(connection=self._redis)
        return RPCMethod(queue, name)

    def _gather(self, *tasks: RPCResult) -> bool:
        for task in tasks:
            if not task.is_finished:
                return False
        return True

    def gather(self, *tasks: RPCResult) -> None:
        while True:
            if self._gather(*tasks):
                return
            else:
                time.sleep(0.5)
