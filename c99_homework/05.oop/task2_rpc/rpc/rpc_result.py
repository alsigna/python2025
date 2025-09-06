import time
from typing import Generic, TypeVar

from rq.job import Job, JobStatus

from .exceptions import RPCFailedJobError, RPCUnknownJobStatusError

T = TypeVar("T")


class RPCResult(Generic[T]):
    def __init__(self, job: Job):
        self.job_id = job.id
        self._job = job
        self._is_failed = False
        self._is_finished = False
        self._exc_info: str | None = None
        self._result: T | None = None

    @property
    def result(self) -> T | None:
        return self._result

    @property
    def is_failed(self) -> bool:
        self._update_status()
        return self._is_failed

    @property
    def is_finished(self) -> bool:
        self._update_status()
        return self._is_finished

    def _update_status(self) -> None:
        if self._is_finished:
            return
        status: JobStatus | None = self._job.get_status()
        # ошибка внутри функции (ZeroDivisionError: division by zero):
        #  - job.get_status() = JobStatus.FAILED
        #  - job.is_finished = False
        #  - job.job.is_failed = True
        #  - job.exc_info = traceback в текстовом виде
        match status:
            case JobStatus.QUEUED | JobStatus.STARTED:
                self._is_finished = False
                self._is_failed = False
            case JobStatus.FINISHED:
                self._is_finished = True
                self._is_failed = False
                self._result = self._job.result
            case JobStatus.FAILED:
                self._is_finished = True
                self._is_failed = True
                self._exc_info = self._job.exc_info
            case _:
                raise RPCUnknownJobStatusError(f"неизвестный статус {self._job.id}: {status}")

    def wait_for_result(self) -> None:
        while not self._is_finished:
            time.sleep(0.5)
            self._update_status()

    def raise_for_status(self) -> None:
        if not self._is_finished or not self._is_failed:
            return
        raise RPCFailedJobError(self._exc_info)
