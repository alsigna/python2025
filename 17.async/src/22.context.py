import asyncio
import contextvars
from time import perf_counter
from uuid import uuid4

request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def middleware() -> None:
    request_id.set(str(uuid4()))


async def coro(num: int) -> str:
    ctx_request_id = request_id.get()
    task_name = asyncio.current_task().get_name()
    log(f"[{ctx_request_id}] начало работы корутины '{num}' с именем {task_name}")
    await asyncio.sleep(num)
    log(f"[{ctx_request_id}] конец работы корутины '{num}' с именем {task_name}")
    return f"корутина '{num}' выполнена"


async def main(coro_count: int) -> None:
    contexts = [contextvars.copy_context() for _ in range(1, coro_count + 1)]
    tasks = [asyncio.create_task(middleware(), context=ctx) for ctx in contexts]
    await asyncio.gather(*tasks)

    tasks = [
        asyncio.create_task(
            coro=coro(i + 1),
            name=f"my-task-{i+1}",
            context=contexts[i],
        )
        for i in range(len(contexts))
    ]
    await asyncio.gather(*tasks)

    # tasks = [asyncio.create_task(coro(i + 1), context=contexts[i]) for i in range(len(contexts))]
    # await asyncio.gather(*tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(coro_count=4))
    log("асинхронный код закончен")
