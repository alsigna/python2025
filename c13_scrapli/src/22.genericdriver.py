from scrapli.driver import GenericDriver

device = {
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}

with GenericDriver(**device) as ssh:  # type: ignore [arg-type]
    ssh.send_command("terminal length 0")
    ssh.send_command("terminal width 512")
    output = ssh.send_command("show ip arp")
    ssh.send_command("conf t")
    ssh.send_command("int loo123")
    ssh.send_command("ip add 1.2.3.4 255.255.255.0")
    ssh.send_command("end")
    prompt = ssh.get_prompt()

print(prompt)
print(output.result)
