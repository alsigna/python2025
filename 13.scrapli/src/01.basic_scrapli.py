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
    ssh = Scrapli(**device)  # type: ignore [arg-type]
    ssh.open()
    ssh.close()
