from scrapli import Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}

if __name__ == "__main__":
    ssh = Scrapli(**device)  # type: ignore [arg-type]
    ssh.open()
    output: Response = ssh.send_command("show clock")
    ssh.close()

    print(output.result)
