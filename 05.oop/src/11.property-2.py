from netaddr import IPAddress


class Switch:
    def __init__(self, ip: str, hostname: str) -> None:
        self._ip: str
        self.ip = ip
        self._hostname = hostname

    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self._ip = ip

    def _set_hostname(self, hostname: str) -> None:
        self._hostname = hostname

    def _get_hostname(self) -> str:
        return self._hostname

    hostname = property(fget=_get_hostname, fset=_set_hostname, doc="device hostname")


# sw = Switch("500.168.1.1")
# print(sw.ip)
# sw.ip = "192.168.1.2"
# print(sw.ip)
# sw.ip = "500.1.1.1"

sw = Switch("100.168.1.1", "sw1")
print(sw.ip)

# sw = Switch("100.168.1.1000", "sw1")
# print(sw.ip)
