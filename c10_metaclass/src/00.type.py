class Device:
    platform = "cisco_iosxe"

    def __init__(self, ip: str) -> None:
        self.ip = ip
        self.hostname = self._resolve_hostname(ip)

    def _resolve_hostname(self, ip: str) -> str:
        return "rt1"


d = Device("1.2.3.4")
print(d.ip)
print(d.hostname)


def _resolve_hostname(self, ip: str) -> str:
    return "rt1"


def __init__(self, ip: str) -> None:
    self.ip = ip
    self.hostname = self._resolve_hostname(ip)


DeviceNew = type(
    "DeviceNew",
    (),
    {
        "platform": "cisco_iosxe",
        "__init__": __init__,
        "_resolve_hostname": _resolve_hostname,
    },
)

d = DeviceNew("1.2.3.4")
print(d.ip)
print(d.platform)
print(d.hostname)
