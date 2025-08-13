from concurrent.futures import ThreadPoolExecutor
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

    if host == "192.168.122.115":
        raise ValueError("неизвестный хост")

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    log(f"{host:>15}: завершено")
    return result


if __name__ == "__main__":
    ip_addresses = [
        "192.168.122.102",
        # "192.168.122.109",
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
    t0 = perf_counter()

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = pool.map(print_version, ip_addresses)
        log("задачи поставлены в пул")

    log("код за пределами контекстного менеджера ThreadPoolExecutor'a")

    # map дает итератор, и если какая-либо таска была завершена с ошибкой, то
    # цепочка ломается и все последующие таски (даже если они успешные), будут
    # отданы с ошибкой
    it = iter(results)
    for _ in ip_addresses:
        try:
            r = next(it)
        except Exception:
            log("error")
        else:
            log(r)
