import asyncio
from itertools import product
from random import shuffle
from time import perf_counter

from scrapli import AsyncScrapli
from scrapli.response import Response

DEVICES = [
    "192.168.122.101",
    "192.168.122.102",
    "192.168.122.103",
]
COMMANDS = [
    "show interfaces description",
    "show version",
    "show ip interface brief",
]
MAX_CONNECTIONS = 2


pairs = list(product(DEVICES, COMMANDS))
shuffle(pairs)
semaphore = asyncio.Semaphore(MAX_CONNECTIONS)


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


async def get_output_scrapli(ip: str, cmd: str) -> Response:
    log(f"get_output_scrapli - {ip:>15}: \u23f2 корутина для сбора '{cmd}' создана")
    device = device_scrapli | {"host": ip}
    async with semaphore:
        log(f"get_output_scrapli - {ip:>15}: \u23e9 сбор '{cmd}'")
        async with AsyncScrapli(**device) as ssh:
            response = await ssh.send_command(cmd)
    log(f"get_output_scrapli - {ip:>15}: \u2705 завершено '{cmd}'")
    return response


async def main() -> None:
    await asyncio.gather(
        *[asyncio.create_task(get_output_scrapli(ip=pair[0], cmd=pair[1])) for pair in pairs],
    )


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
