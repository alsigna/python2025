import asyncio
from itertools import product
from random import shuffle
from time import perf_counter

from scrapli import AsyncScrapli
from scrapli.response import Response

DEVICES = [
    "192.168.122.101",
    "192.168.122.102",
    "192.168.122.110",
    "192.168.122.111",
    "192.168.122.112",
    "192.168.122.113",
]
COMMANDS = [
    "show interfaces description",
    "show version",
    "show ip interface brief",
]
MAX_CONNECTIONS = 3

semaphore = asyncio.Semaphore(MAX_CONNECTIONS)

pairs = list(product(DEVICES, COMMANDS))
shuffle(pairs)


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


device_scrapli = {
    "transport": "asyncssh",
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "transport_options": {
        "open_cmd": [
            "-o",
            "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
            "-o",
            "HostKeyAlgorithms=+ssh-rsa",
        ],
    },
}


async def _get_output_scrapli(ip: str, cmd: str) -> Response:
    log(f"get_output_scrapli - {ip:>15}: \u23f2 корутина для сбора '{cmd}' создана")
    device = device_scrapli | {"host": ip}
    log(f"get_output_scrapli - {ip:>15}: \u23e9 сбор '{cmd}'")
    # async with semaphore:
    async with AsyncScrapli(**device) as ssh:
        response = await ssh.send_command(cmd)
    log(f"get_output_scrapli - {ip:>15}: \u2705 завершено '{cmd}'")
    return response


async def get_output_scrapli(ip: str, cmd: str) -> Response:
    async with semaphore:
        return await _get_output_scrapli(ip, cmd)


async def main() -> None:
    await asyncio.gather(
        *[asyncio.create_task(get_output_scrapli(ip=pair[0], cmd=pair[1])) for pair in pairs],
    )


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
