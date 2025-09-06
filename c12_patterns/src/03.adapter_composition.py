from ipaddress import IPv4Interface


# целевой класс - предоставляет интерфейс, с которым работает клиентский код
class Target:
    def request(self) -> tuple[str, str]:
        return "192.168.0.1", "255.255.255.0"


# адаптируемый класс - содержит что-то полезное, но не совместим с клиентским кодом
class External:
    def unsupported_request(self) -> IPv4Interface:
        return IPv4Interface("192.168.255.1/24")


# адаптер - делает интерфейс адаптируемого класса, совместимым с целевым
class Adapter(Target):
    def __init__(self, external: External):
        self.external = external

    def request(self) -> tuple[str, str]:
        ip = self.external.unsupported_request()
        return str(ip.ip), str(ip.netmask)


if __name__ == "__main__":
    a = Adapter(External())
    ip, mask = a.request()
    print(f"{ip=}")
    print(f"{mask=}")
