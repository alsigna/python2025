import asyncio
from time import perf_counter

import httpx
from tqdm.asyncio import tqdm_asyncio


def log(msg: str) -> None:
    tqdm_asyncio.write(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def fetch(client: httpx.AsyncClient) -> None:
    task_name = asyncio.current_task().get_name()
    try:
        response = await client.get("/get")
    except Exception as exc:
        log(f"{task_name}: GET - exception {exc.__class__.__name__}: {str(exc)}")
    else:
        status_code = response.status_code
        if status_code == 200:
            request_id = response.json()["headers"]["X-Amzn-Trace-Id"]
            log(f"{task_name}: GET - status-code={status_code} - request-id={request_id}")
        else:
            log(f"{task_name}: GET - status-code={status_code}")

    try:
        response = await client.post("/post", json={"key": "value"})
    except Exception as exc:
        log(f"{task_name}: POST - exception {exc.__class__.__name__}: {str(exc)}")
    else:
        status_code = response.status_code
        if status_code == 200:
            request_id = response.json()["headers"]["X-Amzn-Trace-Id"]
            log(f"{task_name}: POST - status-code={status_code} - request-id={request_id}")
        else:
            log(f"{task_name}: POST - status-code={status_code}")


async def main() -> None:
    async with httpx.AsyncClient(
        limits=httpx.Limits(max_connections=20),
        verify=False,
        base_url="https://httpbin.org/",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    ) as client:
        tasks = [asyncio.create_task(fetch(client), name=f"task-{i:>02}") for i in range(100)]
        await tqdm_asyncio.gather(*tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
