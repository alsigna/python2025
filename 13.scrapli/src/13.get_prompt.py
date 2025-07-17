from typing import Any

from scrapli import Scrapli

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "default_desired_privilege_level": "exec",
    "ssh_config_file": True,
}


def change_prompt(device: dict[str, Any]) -> None:
    with Scrapli(**device) as ssh:
        print(ssh.get_prompt())

        ssh.acquire_priv("privilege_exec")
        print(ssh.get_prompt())

        ssh.acquire_priv("configuration")
        print(ssh.get_prompt())

        ssh.acquire_priv("tclsh")
        print(ssh.get_prompt())

        ssh.acquire_priv("exec")
        print(ssh.get_prompt())


if __name__ == "__main__":
    try:
        change_prompt(device)
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
