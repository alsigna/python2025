from scrapli import Scrapli

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


if __name__ == "__main__":
    with Scrapli(**device) as ssh:  # type: ignore [arg-type]
        output = ssh.send_command("show clock")

    print(output.result)
