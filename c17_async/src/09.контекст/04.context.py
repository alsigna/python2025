import asyncio
import contextvars
import logging
import uuid
from datetime import datetime
from random import randint
from zoneinfo import ZoneInfo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(uuid)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

request_id = contextvars.ContextVar("request_id", default="n/a")


class UUIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "uuid"):
            record.uuid = request_id.get()
        return True


log = logging.getLogger(__name__)
log.addFilter(UUIDFilter())


async def fetch_router_config(ip: str) -> str:
    log.info(f"сбор конфигурации с '{ip}'")
    await asyncio.sleep(randint(1, 5))
    config = f"конфигурация '{ip}' на {datetime.now(tz=ZoneInfo("Europe/Moscow"))}"
    if ip.endswith("2"):
        raise RuntimeError("какая-то ошибка сбора")
    log.info(f"конфигурация с '{ip}' успешно собрана")
    return config


async def upload_to_s3(config: str, ip: str) -> str:
    log.info(f"загрузка конфигурации '{ip}' в s3")
    await asyncio.sleep(randint(1, 5))
    s3_path = f"s3://configs/{ip}.txt"
    log.info(f"конфигурация '{ip}' сохранена в s3: {s3_path}")
    return s3_path


async def process_router(ip: str) -> str:
    request_id.set(str(uuid.uuid4()).split("-")[-1])

    log.info(f"обработка маршрутизатора '{ip}'")
    try:
        config = await fetch_router_config(ip)
        s3_path = await upload_to_s3(config, ip)
    except Exception as exp:
        log.error(f"ошибка при обработке '{ip}': {str(exp)}")
        raise
    else:
        log.info(f"маршрутизатор '{ip}' успешно обработан. S3 путь: '{s3_path}'")
        return s3_path


async def main(ips: list[str]):
    tasks = [asyncio.create_task(process_router(ip)) for ip in ips]
    await asyncio.gather(*tasks, return_exceptions=True)

    new_tasks = []
    for ip, task in zip(ips, tasks, strict=True):
        new_tasks.append(
            asyncio.create_task(
                coro=fetch_router_config(ip),
                context=task.get_context(),
            ),
        )

    await asyncio.gather(*new_tasks, return_exceptions=True)

    # _request_id = ctx.get(request_id)

    # exc = task.exception()
    # if exc is not None:
    #     log.error(f"статус '{ip}': ошибка: {str(exc)}", extra={"uuid": _request_id})
    # else:
    #     result = task.result()
    #     log.info(f"статус '{ip}': успешно: {result}", extra={"uuid": _request_id})


if __name__ == "__main__":
    routers = [
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.3",
        "192.168.1.4",
    ]
    asyncio.run(main(routers))
