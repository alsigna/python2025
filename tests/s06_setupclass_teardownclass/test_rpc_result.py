# python -m unittest discover -s ./c18_pytest/src/s06_setupclass_teardownclass/
# python -m unittest discover -s ./c18_pytest/src/s06_setupclass_teardownclass/ -v
# python -W ignore::DeprecationWarning  -m unittest discover -s ./c18_pytest/src/s06_setupclass_teardownclass/ -v
# export TEST_REDIS_HOST=localhost TEST_REDIS_PORT=6380

from os import getenv
from unittest import TestCase

from redis import Redis
from rq.job import Job, JobStatus
from rq.queue import Queue

from c18_pytest.src.s06_setupclass_teardownclass.exceptions import RPCUnknownJobStatusError
from c18_pytest.src.s06_setupclass_teardownclass.rpc_result import RPCResult


class RPCResultTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_redis_host = getenv("TEST_REDIS_HOST")
        test_redis_port = getenv("TEST_REDIS_PORT")
        test_redis_db = getenv("TEST_REDIS_DB", 0)
        test_redis_password = getenv("TEST_REDIS_PASSWORD")

        if not all((test_redis_host, test_redis_port)):
            raise EnvironmentError("Тестовая среда не готова")

        redis = Redis(
            host=test_redis_host,
            port=test_redis_port,
            db=test_redis_db,
            password=test_redis_password,
        )

        cls.queue = Queue(
            name="test_queue",
            connection=redis,
        )
        cls.job: Job = cls.queue.enqueue(
            f="tasks.test_func_name.test_func_name",
            args=(1, 2),
            kwargs={"a": "a", "b": "b"},
        )
        cls.instance = RPCResult(cls.job)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.job.delete()
        cls.queue.delete()

    def test_job_id(self) -> None:
        self.assertEqual(self.instance.job_id, self.job.id)

    def test_job_live_cycle(self) -> None:
        result = "test-result"

        # начальное состояние
        self.assertFalse(self.instance.is_failed)
        self.assertFalse(self.instance.is_finished)
        self.assertIsNone(self.instance.result)
        self.assertEqual(self.job.get_status(), JobStatus.QUEUED)

        # имитируем завершение через rq-api
        self.job._result = result
        self.job.set_status(JobStatus.FINISHED)
        self.job.save()
        # можно и напрямую в redis ходить:
        # self.job.connection.hset(
        #     name=self.job.key,
        #     mapping={
        #         "result": self.job.serializer.dumps(result),
        #         "status": JobStatus.FINISHED,
        #     },
        # )

        # проверяем конечное состояние
        self.assertFalse(self.instance.is_failed)
        self.assertTrue(self.instance.is_finished)
        self.assertEqual(self.instance.result, result)
        self.assertEqual(self.job.get_status(), JobStatus.FINISHED)

    def test_unknown_status(self) -> None:
        self.instance._is_finished = False
        self.job.set_status(JobStatus.DEFERRED)
        self.job.save()
        with self.assertRaisesRegex(
            expected_exception=RPCUnknownJobStatusError,
            expected_regex=f"неизвестный статус {self.job.id}: {JobStatus.DEFERRED}",
        ):
            _ = self.instance.is_finished
