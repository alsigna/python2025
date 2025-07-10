from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from random import randint

import yaml
from utils.log import LoggerMixIn

PLATFORMS_FILE = "./platforms.yaml"
DEVICES_FILE = "./devices.yaml"
type Platform = str
type IP = str


class Device(ABC, LoggerMixIn):
    def __init__(self, ip: IP):
        self.hostname = ip
        self.ip = ip

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.ip}"

    def __repr__(self) -> str:
        return f"<{self.__str__()}>"

    @property
    @abstractmethod
    def platform(self) -> Platform: ...

    @property
    @abstractmethod
    def commands(self) -> list[str]: ...

    @property
    @abstractmethod
    def secrets(self) -> list[str]: ...

    def collect_outputs(self) -> None:
        self.log_debug("подключение к устройству")
        for command in self.commands:
            self.log_debug(f"сбор вывода '{command}'")
            dice = randint(1, 6)
            match dice:
                case 6:
                    self.log_warning(f"команда '{command}' собрана не полностью")
                case 5:
                    self.log_error(f"ошибка сбора команды '{command}'")
                case _:
                    self.log_succeeded(f"команда '{command}' собрана успешно")


@dataclass
class YamlPlatform:
    platform: Platform
    vendor: str
    commands: list[str]
    secrets: list[str] = field(default_factory=list)


@dataclass
class YamlDevice:
    ip: IP
    platform: Platform


class DeviceFactory:
    _PLATFORM_MAP: dict[Platform, type[Device]] = {}

    @classmethod
    def load_platforms(cls) -> None:
        with open(PLATFORMS_FILE) as f:
            data = yaml.safe_load(f)
        for platform, platform_data in data.items():
            platform_yaml = YamlPlatform(platform=platform, **platform_data)
            if platform in cls._PLATFORM_MAP:
                raise ValueError(f"платформа '{platform}' уже загружена")
            cls._PLATFORM_MAP[platform] = type(
                platform.upper(),
                (Device,),
                asdict(platform_yaml),
            )

    @classmethod
    def create(cls, ip: IP, platform: Platform) -> Device:
        if platform not in cls._PLATFORM_MAP:
            raise ValueError(f"Unknown platform '{platform}'")
        return cls._PLATFORM_MAP[platform](ip)


def load_devices(filename: str) -> list[YamlDevice]:
    result = []
    with open(filename) as f:
        data = yaml.safe_load(f)
    for device_raw in data["devices"]:
        result.append(YamlDevice(**device_raw))
    return result


if __name__ == "__main__":
    DeviceFactory.load_platforms()
    yaml_devices = load_devices(DEVICES_FILE)
    devices = [DeviceFactory.create(device.ip, device.platform) for device in yaml_devices]
    for device in devices:
        device.log_debug("-" * 10)
        device.collect_outputs()
