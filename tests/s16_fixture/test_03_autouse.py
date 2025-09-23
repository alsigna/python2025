from collections.abc import Iterator
from os import getenv
from typing import Any

import pytest
from redis import Redis
from rq.job import Job, JobStatus
from rq.queue import Queue

from c18_pytest.src.s16_fixture.rpc_result import RPCResult

# pytestmark = pytest.mark.redis()


@pytest.mark.redis()
class TestRPCResult:
    @pytest.fixture(autouse=True)
    def _create_instance(self) -> Iterator[None]:
        test_redis_host = getenv("TEST_REDIS_HOST", "")
        test_redis_port = getenv("TEST_REDIS_PORT", 0)
        test_redis_db = getenv("TEST_REDIS_DB", 0)
        test_redis_password = getenv("TEST_REDIS_PASSWORD")

        redis = Redis(
            host=test_redis_host,
            port=test_redis_port,
            db=test_redis_db,
            password=test_redis_password,
        )

        queue = Queue(
            name="test_queue",
            connection=redis,
        )
        job: Job = queue.enqueue(
            f="tasks.test_func_name.test_func_name",
            args=(1, 2),
            kwargs={"a": "a", "b": "b"},
        )
        self.instance: RPCResult[Any] = RPCResult(job=job)

        yield

        job.delete()
        queue.delete()

    # @pytest.mark.redis
    def test_is_finished_after_creation(self) -> None:
        # фикстура выполняется каждый раз для каждого теста (пока scope не смотрели)
        # поэтому в каждом тесте будет свой instance и своя job в redis
        # pytest -m redis -v -s
        # pytest -k test_is_finished_ -v -s
        print(f"\n-----> {self.instance.job_id=}")
        assert not self.instance.is_finished

    # @pytest.mark.redis
    def test_is_finished_after_finish(self) -> None:
        self.instance._job.set_status(JobStatus.FINISHED)  # noqa: SLF001
        self.instance._job.save()  # noqa: SLF001

        print(f"\n-----> {self.instance.job_id=}")
        assert self.instance.is_finished
