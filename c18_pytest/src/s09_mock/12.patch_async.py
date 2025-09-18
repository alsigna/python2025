import asyncio
from time import perf_counter
from unittest.mock import AsyncMock, patch


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    async def get_output(self, command: str) -> str:
        await asyncio.sleep(3)
        return f"output of '{command}'"


async def main() -> None:
    device = Device("1.2.3.4")
    log(await device.get_output("show version"))


if __name__ == "__main__":
    t0 = perf_counter()
    log("оригинальный объект:")
    asyncio.run(main())

    log("-----")
    log("mock-объект:")
    with patch.object(
        target=Device,
        attribute="get_output",
        new_callable=AsyncMock,
        return_value="mocked output",
    ) as mock_get_output:
        asyncio.run(main())

    log("-----")
    log("mock-sleep:")
    with patch(
        target="asyncio.sleep",
        new_callable=AsyncMock,
    ) as mock_sleep:
        mock_sleep.return_value = None
        asyncio.run(main())

    log("-----")
    log("пример с рекурсией:")
    real_sleep = asyncio.sleep

    async def fake_sleep(delay: float) -> None:
        # мы используем эту функцию как side_effect, но внутри нее идет обращение к
        # функции, которая была замокана. Поэтому возникает рекурсия. В этом случае
        # мы сохраняем оригинальную функцию в отдельный объект и используем его
        return await asyncio.sleep(1)
        # return await real_sleep(1)

    with patch(
        target="asyncio.sleep",
        side_effect=fake_sleep,
    ):
        asyncio.run(main())
