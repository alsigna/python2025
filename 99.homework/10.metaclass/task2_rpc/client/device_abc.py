from abc import ABC, abstractmethod

from python2025_alexigna.hw_05_oop.task2_rpc.client.log import LoggerMixIn
from python2025_alexigna.hw_05_oop.task2_rpc.client.models import Platform


class Device(LoggerMixIn, ABC):
    def __init__(self, host: str) -> None:
        self.host = host

    @property
    @abstractmethod
    def command(self) -> str: ...

    @property
    @abstractmethod
    def platform(self) -> Platform: ...

    # @classmethod
    # def __init_subclass__(cls, platform: Platform):
    #     super().__init_subclass__()
    #     cls.platform = platform
    #     if getattr(cls, "platform", None) is None:
    #         raise TypeError(f"Класс {cls.__name__} должен определить 'platform'")


class CiscoIOSXE(Device):
    platform = Platform.CISCO_IOSXE
    command = "show inventory"


class HuaweiVRP(Device):
    platform = Platform.HUAWEI_VRP
    command = "display device"
