from typing import Any

from scrapli import Scrapli

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def check_alive(device: dict[str, Any]) -> None:
    with Scrapli(**device) as ssh:
        print(ssh.get_prompt())
        print(f"после подключения: {ssh.isalive()=}")

        ssh.close()
        try:
            _ = ssh.get_prompt()
        except Exception:
            print(f"ошибка после выхода {ssh.isalive()=}")
            ssh.open()
            print(f"после повторного подключения:  {ssh.isalive()=}")

        print(ssh.get_prompt())


if __name__ == "__main__":
    try:
        check_alive(device)
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
