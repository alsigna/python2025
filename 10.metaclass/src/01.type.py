from abc import ABC, abstractmethod
from enum import StrEnum, auto
from typing import Self

from utils.log import LoggerMixIn


class Platform(StrEnum):
    ARISTA_EOS = "arista_eos"
    CISCO_IOSXE = auto()
    HUAWEI_VRP = auto()


class Device(ABC):
    def __init__(self, hostname: str):
        self.hostname = hostname

    @abstractmethod
    def get_running_config(self) -> str: ...

    @property
    @abstractmethod
    def platform(self) -> Platform: ...


class CiscoIOSXE(Device, LoggerMixIn):
    platform = Platform.CISCO_IOSXE

    def get_running_config(self) -> str:
        self.log_debug("подключаемся к устройству")
        self.log_succeeded("'show run' успешно выполнена")
        self.log_debug("отключаемся от устройства")
        return f"{self.platform}: {self.hostname}: OK"


if __name__ == "__main__":
    rt1 = CiscoIOSXE("rt1")
    print(rt1.get_running_config())

    def arista_eos_get_running_config(self) -> str:  # type: ignore[no-untyped-def]
        self.log_debug("подключаемся к устройству")
        self.log_succeeded("'show run' успешно выполнена")
        self.log_debug("отключаемся от устройства")
        return f"{self.platform}: {self.hostname}: OK"

    AristaEOS = type(
        "AristaEOS",
        (Device, LoggerMixIn),
        {
            "platform": Platform.ARISTA_EOS,
            "get_running_config": arista_eos_get_running_config,
        },
    )

    rt2 = AristaEOS("rt2")
    print(rt2.get_running_config())
