import asyncio
import json
import re
from time import perf_counter

import aiohttp
from scrapli import AsyncScrapli
from scrapli.response import Response

NETBOX_TOKEN = "a042e0c9ef120737001a5d4b79925a690b4254f3"
NETBOX_URL = "https://demo.netbox.dev"
DEVICES = [
    "192.168.122.101",
    "192.168.122.102",
    "192.168.122.103",
]
COMMAND = "show interfaces description"


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
    log(f"get_output_scrapli - {ip:>15}: сбор вывода с устройства")
    device = device_scrapli | {"host": ip}
    async with AsyncScrapli(**device) as ssh:
        response = await ssh.send_command(cmd)
    log(f"get_output_scrapli - {ip:>15}: сбор завершен")
    return response


async def collect_output(queue: asyncio.Queue) -> None:
    tasks = [asyncio.create_task(get_output_scrapli(ip, COMMAND)) for ip in DEVICES]
    async for task in asyncio.as_completed(tasks):
        try:
            await queue.put(task.result())
        except Exception as exc:
            log(f"collect_output - ошибка {exc.__class__.__name__}: {exc}")
    await queue.put(None)


async def _update_netbox(session: aiohttp.ClientSession, response: Response) -> None:
    log(f"update_netbox - получены данные для '{response.host}'")
    await asyncio.sleep(5)
    m = re.search(r"Lo0\s+up\s+up\s+(?P<description>.*)", response.result)
    if m is None:
        log(f"update_netbox - нет информации по Loopback0 на устройстве '{response.host}'")
        return

    description = m.group("description")
    log(f"update_netbox - описание '{response.host}' - '{description}'")

    async with session.get(
        url="/api/ipam/ip-addresses/",
        params=[("address", response.host)],
    ) as reply:
        reply.raise_for_status()
        reply_json = await reply.json()
    reply_json = reply_json["results"][0]
    assigned_object_id = reply_json["assigned_object"]["id"]
    existed_description = reply_json["assigned_object"]["description"]
    if existed_description == description:
        log(f"update_netbox - для '{response.host}' description уже установлен равным '{description}'")
        return

    async with session.patch(
        url=f"/api/dcim/interfaces/{assigned_object_id}",
        data=json.dumps({"description": description}),
    ) as reply:
        reply.raise_for_status()
        log(f"update_netbox - для '{response.host}' description обновлен на '{description}'")


async def update_netbox(queue: asyncio.Queue) -> None:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=10, ssl=False),
        base_url=NETBOX_URL,
        headers={
            "Authorization": f"Token {NETBOX_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "demo-python2025",
        },
    ) as session:
        tasks: list[asyncio.Task] = []
        response: Response | None = await queue.get()
        while response is not None:
            tasks.append(asyncio.create_task(_update_netbox(session, response)))
            response: Response | None = await queue.get()
        await asyncio.gather(*tasks)
        log("update_netbox - обработка всех ответов завершена")
        log(f"!!!! {queue.full()=}")
        log(f"!!!! {queue.empty()=}")
        log(f"!!!! {queue.maxsize=}")
        log(f"!!!! {queue.qsize()=}")
        log(f"!!!! {queue._unfinished_tasks=}")


async def main() -> None:
    queue = asyncio.Queue(maxsize=0)
    await asyncio.gather(
        asyncio.create_task(collect_output(queue)),
        asyncio.create_task(update_netbox(queue)),
    )


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
