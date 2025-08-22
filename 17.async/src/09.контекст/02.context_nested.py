import asyncio
import contextvars
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(uuid)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

request_id = contextvars.ContextVar("request_id")


class UUIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "uuid"):
            record.uuid = request_id.get()
        return True


log = logging.getLogger(__name__)
log.addFilter(UUIDFilter())


async def level2() -> None:
    request_id.set("level2")
    log.info("начало работы корутины level2")
    await asyncio.sleep(1)
    log.info("конец работы корутины level2")


async def level1() -> None:
    request_id.set("level1")
    log.info("начало работы корутины level1")
    await asyncio.sleep(1)
    ctx = asyncio.current_task().get_context()
    await asyncio.create_task(level2(), context=ctx)
    log.info("конец работы корутины level1")


async def main():
    request_id.set("main")
    log.info("начало работы корутины main")
    await asyncio.create_task(level1())
    log.info("конец работы корутины main")


if __name__ == "__main__":
    asyncio.run(main())
