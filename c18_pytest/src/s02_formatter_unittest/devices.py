from formatters import FormattersRegistry

HUAWEI_CONFIG = """
Software Version V200VERSION
#
 sysname router1
#
 clock timezone MSK add 03:00:00
#
 snmp-agent community write some-secret-hash
 snmp-agent community read some-secret-hash
 snmp-agent community read some-secret-hash view lala
 snmp-agent sys-info contact admin@lab.me
#
bgp 64512
 ipv4-family unicast
  import-route direct route-policy RP_CONNECTED
#
user-interface con 0
 authentication-mode password
 set authentication password irreversible-cipher secret-password-hash
#
"""


class HuaweiVRP:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_configuration(self) -> str:
        return HUAWEI_CONFIG

    def format_configuration(self, config: str) -> str:
        for handler in FormattersRegistry.REGISTRY:
            config = handler.format(config)
        return config

    def save_config_to_file(self, config: str, filename: str) -> None:
        with open(filename, "w") as f:
            f.write(config)
