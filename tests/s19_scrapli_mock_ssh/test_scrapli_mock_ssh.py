import asyncio

import pytest
from scrapli import AsyncScrapli, Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "127.0.0.1",
    "port": 20101,
    "auth_username": "scrapli",
    "auth_password": "scrapli",
    "auth_strict_key": False,
}


# def send_command(device: dict[str, str], command: str) -> Response:
#     try:
#         with Scrapli(**device) as ssh:
#             return ssh.send_command(command)
#     except Exception as exc:
#         print(f"Error {exc.__class__.__name__}: {str(exc)}")
#         raise exc


# @pytest.mark.skip("фейлится при запуске через IDE")
@pytest.mark.mock_ssh()
def test_sync_scrapli_mock_ssh() -> None:
    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")
    assert output.result.splitlines()[0] == "Cisco IOS XE Software, Version 17.03.03"


@pytest.mark.mock_ssh()
async def test_async_scrapli_mock_ssh() -> None:
    async with AsyncScrapli(
        **device,
        transport="asyncssh",
    ) as ssh:
        output = await ssh.send_command("show version")
    assert output.result.splitlines()[0] == "Cisco IOS XE Software, Version 17.03.03"
