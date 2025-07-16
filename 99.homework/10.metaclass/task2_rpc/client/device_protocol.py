from typing import ClassVar, Protocol, runtime_checkable

from python2025_alexigna.hw_05_oop.task2_rpc.client.log import LoggerMixIn
from python2025_alexigna.hw_05_oop.task2_rpc.client.models import Platform


@runtime_checkable
class Device(Protocol):
    platform: ClassVar[Platform]
    command: ClassVar[str]
    host: str

    def __init__(self, host: str) -> None: ...
    def log_debug(self, msg: str, *args: str) -> None: ...
    def log_info(self, msg: str, *args: str) -> None: ...
    def log_error(self, msg: str, *args: str) -> None: ...
    def log_succeeded(self, msg: str, *args: str) -> None: ...


class CiscoIOSXE(LoggerMixIn):
    platform: ClassVar[Platform] = Platform.CISCO_IOSXE
    command: ClassVar[str] = "show inventory"

    def __init__(self, host: str) -> None:
        self.host = host


class HuaweiVRP(LoggerMixIn):
    platform: ClassVar[Platform] = Platform.HUAWEI_VRP
    command: ClassVar[str] = "display device"

    def __init__(self, host: str) -> None:
        self.host = host
