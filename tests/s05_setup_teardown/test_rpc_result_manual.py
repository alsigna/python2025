# python -m unittest discover -s ./c18_pytest/src/s05_setup_teardown/
# python -m unittest discover -s ./c18_pytest/src/s05_setup_teardown/ -v
# export TEST_REDIS_HOST=localhost TEST_REDIS_PORT=6380
from os import getenv
from unittest import TestCase

from redis import Redis
from rq.job import Job
from rq.queue import Queue

from c18_pytest.src.s05_setup_teardown.rpc_result import RPCResult

##
## сначала manual пример: _create_instance и _clear делаем руками,
## затем auto - подготовка через setUp/tearDown
##

# подготовка/очистка к тесту делается вручную
# - создать job
# - провести тест
# - удалить job


class RPCResultTestCase(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        self.job: Job | None = None
        self.instance: RPCResult | None = None
        self.queue: Queue | None = None
        super().__init__(*args, **kwargs)

    def _create_instance(self) -> None:
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
        self.queue = Queue(
            name="test_queue",
            connection=redis,
        )
        self.job: Job = self.queue.enqueue(
            f="tasks.test_func_name.test_func_name",
            args=(1, 2),
            kwargs={"a": "a", "b": "b"},
        )
        self.instance = RPCResult(self.job)

    def _clear(self) -> None:
        self.job.delete()
        self.queue.delete()

    def test_job_id(self) -> None:
        self._create_instance()
        self.assertEqual(self.instance.job_id, self.job.id)
        # вручную распечатать и посмотреть в база, без _clear, что джоба остается
        # print()
        # print(self.instance.job_id)
        # print(self.job.id)
        self._clear()
