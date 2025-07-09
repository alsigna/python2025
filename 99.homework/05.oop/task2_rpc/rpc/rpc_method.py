from typing import Any

from rq import Queue
from rq.job import Job

from .rpc_result import RPCResult


class RPCMethod:
    def __init__(self, queue: Queue, func_name: str) -> None:
        self._queue = queue
        self._func_name = func_name

    def __call__(self, *args: Any, **kwargs: Any) -> RPCResult[Any]:
        job: Job = self._queue.enqueue(
            f=f"tasks.{self._func_name}.{self._func_name}",
            args=args,
            kwargs=kwargs,
        )
        return RPCResult(job)
