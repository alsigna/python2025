import time
from concurrent.futures import Future, ThreadPoolExecutor
from time import perf_counter

from scrapli import Scrapli


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def print_version(host: str) -> str:
    log(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    log(f"{host:>15}: завершено")
    return result


def print_serial(host: str) -> str:
    if host == "192.168.122.101":
        time.sleep(5)
    log(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    serial = parsed_output.get("serial")[0]
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {serial}"
    log(f"{host:>15}: завершено")
    return result


if __name__ == "__main__":
    t0 = perf_counter()

    ip_addresses = [
        "192.168.122.102",
        "192.168.122.109",
        "192.168.122.110",
        "192.168.122.111",
        "192.168.122.112",
        "192.168.122.113",
        "192.168.122.114",
        "192.168.122.115",
        "192.168.122.116",
        "192.168.122.117",
        "192.168.122.101",
        "192.168.122.118",
    ]

    futures: list[Future] = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        for ip in ip_addresses:
            if int(ip.split(".")[-1]) % 2 == 0:
                futures.append(pool.submit(print_version, ip))
            else:
                futures.append(pool.submit(print_serial, ip))
        log("задачи поставлены в очередь")

    log("код за пределами контекстного менеджера")

    for r in futures:
        try:
            log(r.result())
        except Exception as exc:
            log(f"{exc.__class__.__name__}: {str(exc)}")
