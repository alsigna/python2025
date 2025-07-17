from abc import ABC, abstractmethod


#
# устройства
#
class Device(ABC):
    def __init__(self, ip: str):
        self.ip = ip

    @property
    @abstractmethod
    def platform(self) -> str: ...

    @property
    @abstractmethod
    def show_version_command(self) -> str: ...

    def send_command(self, command: str) -> str:
        return ""


class CiscoIOSXE(Device):
    platform = "cisco_iosxe"
    show_version_command = "show version"


class HuaweiVRP(Device):
    platform = "huawei_vrp"
    show_version_command = "display version"


#
# парсер вывода
#


class Parser(ABC):
    @classmethod
    @abstractmethod
    def parse_version(cls, output: str) -> str: ...


class CiscoIOSXEParser(Parser):
    @classmethod
    def parse_version(cls, output: str) -> str:
        return "15.1(4)M5"


class HuaweiVRPParser(Parser):
    @classmethod
    def parse_version(cls, output: str) -> str:
        return "V100R005C60"


#
# фабрика
#


class Factory(ABC):
    @classmethod
    @abstractmethod
    def create_device(cls, ip: str) -> Device: ...

    @classmethod
    @abstractmethod
    def create_parser(cls) -> Parser: ...


class CiscoIOSXEFactory(Factory):
    _parser: Parser | None = None

    @classmethod
    def create_device(cls, ip: str) -> Device:
        return CiscoIOSXE(ip)

    @classmethod
    def create_parser(cls) -> Parser:
        if cls._parser is None:
            cls._parser = CiscoIOSXEParser()
        return cls._parser


class HuaweiVRPFactory(Factory):
    _parser: Parser | None = None

    @classmethod
    def create_device(cls, ip: str) -> Device:
        return HuaweiVRP(ip)

    @classmethod
    def create_parser(cls) -> Parser:
        if cls._parser is None:
            cls._parser = HuaweiVRPParser()
        return cls._parser


def some_client_code(ip: str, factory: Factory):
    device = factory.create_device(ip)
    parser = factory.create_parser()

    output = device.send_command(device.show_version_command)
    version = parser.parse_version(output)
    print(version)


if __name__ == "__main__":
    PLATFORM_TO_FACTORY = {
        "cisco_iosxe": CiscoIOSXEFactory(),
        "huawei_vrp": HuaweiVRPFactory(),
    }
    for ip, platform in (
        ("192.168.1.1", "cisco_iosxe"),
        ("192.168.1.2", "huawei_vrp"),
    ):
        some_client_code(ip, PLATFORM_TO_FACTORY[platform])
