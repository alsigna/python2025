from abc import ABC, abstractmethod
from datetime import datetime


class DeviceConfigBackup(ABC):
    # Шаблонный метод - определяет каркас алгоритма
    def backup_configuration(self, ip: str) -> str:
        self.connect(ip)
        config = self.get_configuration()
        config = self.format_configuration(config)
        backup_filename = self.generate_backup_filename(ip)
        self.save_to_file(backup_filename, config)
        return backup_filename

    def connect(self, ip: str) -> None:
        print(f"подключаемся к устройству {ip} по ssh...")

    @abstractmethod
    def get_configuration(self) -> str: ...

    def format_configuration(self, config: str) -> str:
        return f"=== Конфигурация ===\n{config}\n=== EOF ==="

    def generate_backup_filename(self, ip: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{self.__class__.__name__}_{ip}_{timestamp}.txt"

    def save_to_file(self, filename: str, config: str) -> None:
        print(f"сохранение конфигурации в файл {filename}...")
        with open(filename, "w") as f:
            f.write(config)


class CiscoConfigBackup(DeviceConfigBackup):
    def get_configuration(self) -> str:
        print("выполняем 'show running-config'")
        return (
            "! Cisco IOS Configuration\n"
            "hostname cisco_router\n"
            "interface Gig0/1\n"
            " ip address 192.168.1.1 255.255.255.0\n"
        )


class HuaweiConfigBackup(DeviceConfigBackup):
    def get_configuration(self) -> str:
        print("выполняем 'display current-configuration'")
        return (
            "# Huawei VRP Configuration\n"
            "sysname huawei_router\n"
            "interface GE0/0/1\n"
            " ip address 192.168.1.2 255.255.255.0\n"
        )

    def format_configuration(self, config: str) -> str:
        return f"### Huawei Configuration ###\n{config}\n### EOF ###"


def backup_configurations(devices: list[DeviceConfigBackup]) -> None:
    for platform, ip in devices:
        print(f"\nРезервное копирование '{platform}' устройства '{ip}':")
        if platform == "cisco_iosxe":
            backup = CiscoConfigBackup()
        elif platform == "huawei_vrp":
            backup = HuaweiConfigBackup()
        else:
            print(f"Неизвестная платформа устройства: '{platform}'")
            continue

        filename = backup.backup_configuration(ip)
        print(f"конфигурация сохранена в '{filename}'")


# Пример использования
if __name__ == "__main__":
    devices_to_backup = [
        ("cisco_iosxe", "10.0.0.1"),
        ("huawei_vrp", "10.0.0.2"),
        ("cisco_iosxe", "10.0.0.3"),
    ]

    backup_configurations(devices_to_backup)
