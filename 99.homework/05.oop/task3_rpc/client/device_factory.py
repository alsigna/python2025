from python2025_alexigna.hw_05_oop.task2_rpc.client.device_abc import CiscoIOSXE, Device, HuaweiVRP
from python2025_alexigna.hw_05_oop.task2_rpc.client.models import Platform


class DeviceFactory:
    platform_map: dict[Platform, type[Device]] = {
        Platform.CISCO_IOSXE: CiscoIOSXE,
        Platform.HUAWEI_VRP: HuaweiVRP,
    }

    @classmethod
    def create(cls, platform: Platform, host: str) -> Device:
        _class = cls.platform_map[platform]
        return _class(host)
