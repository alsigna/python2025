import logging
import time

from rich.logging import RichHandler
from scrapli import Scrapli
from scrapli.driver.generic import GenericDriver

log = logging.getLogger("scrapli")
log.setLevel(logging.DEBUG)


rh = RichHandler(
    markup=True,
    show_path=False,
    omit_repeated_times=True,
    rich_tracebacks=True,
)
rh.setFormatter(
    logging.Formatter(
        fmt="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ),
)
log.addHandler(rh)

server = {
    "host": "192.168.122.1",
    "auth_username": "alexigna",
    "auth_private_key": "/Users/alexigna/.ssh/gcp_eve_rsa",
    "auth_strict_key": False,
    "transport": "paramiko",
}

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "port": 22,
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": False,
    "transport": "paramiko",
}

if __name__ == "__main__":
    # подключение к jump-host, как к обычному ssh серверу
    jump_host = GenericDriver(**server)
    jump_host.open()

    # на нем так же есть возможность выполнять какие-либо команды
    # output = jump_host.send_command("who")
    # print(output.result)

    # в зависимости от типа реализации jump-host делаем вручную подключение к устройству
    # для примера это ubuntu, поэтому с нее делаем ssh. Если это консольный сервер, то
    # можно делать очистку и подключение к нужной линии
    # что бы использовать известные логин/пароль от устройства, создаем его заранее, но без .open()
    ssh = Scrapli(**device)
    jump_host.channel.write(
        f"ssh {ssh.auth_username}@{ssh.host} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -F /dev/null",
    )
    jump_host.channel.send_return()
    time.sleep(1)
    jump_host.channel.write(ssh.auth_password, redacted=True)
    jump_host.channel.send_return()

    # после подключения к устройству передаем в него сессию, установленную к jump-host
    ssh.commandeer(conn=jump_host)
    # после этого шага с ssh объектом можно работать как обычно
    ssh.acquire_priv("configuration")
    print(ssh.get_prompt())

    jump_host.close()
