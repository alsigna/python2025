import asyncio
import threading
import time
from pathlib import Path

import pytest
from scrapli_replay.server.server import start


def run_mock_ssh_in_thread(port: int, collect_data: str):
    async def main():
        await start(port=port, collect_data=collect_data)

    def in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main())
            loop.run_forever()
        finally:
            loop.close()

    thread = threading.Thread(target=in_thread, daemon=True)
    thread.start()
    return thread


@pytest.fixture(scope="module", autouse=True)
def mock_ssh_servers():
    dumps = Path(Path(__file__).parent, "dumps")
    run_mock_ssh_in_thread(20101, Path(dumps, "collector_session_dump_192.168.122.101.yaml"))
    run_mock_ssh_in_thread(20102, Path(dumps, "collector_session_dump_192.168.122.102.yaml"))
    time.sleep(0.2)
    yield


# @pytest.fixture(scope="module", autouse=True)
# async def mock_ssh():
#     await start(port=20101, collect_data="collector_session_dump_192.168.122.101.yaml")
#     await start(port=20102, collect_data="collector_session_dump_192.168.122.102.yaml")

#     await asyncio.sleep(10)

#     print("СЕРВЕРА ЗАПУЩЕНЫ")
#     yield
#     print("ТЕСТЫ ЗАКОНЧЕНЫ")

#     # сервера живут внутри asyncio и сами завершатся вместе с event loop
#     # можно не делать, на всякий случа подождем
#     await asyncio.sleep(10)
#     print("СЕРВЕРА ОСТАНОВЛЕНЫ")
