import re
from abc import ABC, abstractmethod
from typing import Callable, ClassVar, TypeVar

T = TypeVar("T", bound="HandlerABC")

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


class HandlersRegistry:
    REGISTRY: ClassVar[list[type["HandlerABC"]]] = []

    @classmethod
    def add(cls) -> Callable[[type[T]], type[T]]:
        def wrapper(handler: type[T]) -> type[T]:
            if not handler.__name__.startswith("HandlerABC") and handler not in cls.REGISTRY:
                cls.REGISTRY.append(handler)
            return handler

        return wrapper


class HandlerABC(ABC):
    @classmethod
    @abstractmethod
    def format(cls, config: str) -> str: ...


@HandlersRegistry.add()
class IndentAligner(HandlerABC):
    @classmethod
    def format(cls, config: str) -> str:
        result = []
        section = False
        for line in config.splitlines():
            if len(line) == 0:
                continue
            if line == "#":
                section = False
                space_count = 0
            elif not line.startswith(" "):
                section = True
            if line.startswith(" ") and not section:
                if space_count == 0:
                    space_count = len(line) - len(line.lstrip())
                result.append(line.removeprefix(" " * space_count))
            else:
                result.append(line)
        return "\n".join(result)


@HandlersRegistry.add()
class CommunityStripper(HandlerABC):
    @classmethod
    def format(cls, config: str) -> str:
        config = re.sub(
            pattern=r"(snmp-agent community (?:read|write)) \S+",
            repl=r"\1 ****",
            string=config,
        )
        return config


@HandlersRegistry.add()
class CipherStripper(HandlerABC):
    @classmethod
    def format(cls, config: str) -> str:
        config = re.sub(
            pattern=r"(irreversible-cipher) \S+",
            repl=r"\1 ****",
            string=config,
        )
        return config


class HuaweiVRP:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_configuration(self) -> str:
        return HUAWEI_CONFIG

    def format_configuration(self, config: str) -> str:
        for handler in HandlersRegistry.REGISTRY:
            config = handler.format(config)
        return config

    def save_config_to_file(self, config: str, filename: str) -> None:
        with open(filename, "w") as f:
            f.write(config)


if __name__ == "__main__":
    device = HuaweiVRP("192.168.0.1")
    config = device.get_configuration()
    config = device.format_configuration(config)
    print(config)
