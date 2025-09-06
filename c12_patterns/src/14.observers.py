import json
from abc import ABC, abstractmethod

import requests
import urllib3

urllib3.disable_warnings()
NETBOX_URL = "https://demo.netbox.dev/api/dcim/devices/"
NETBOX_TOKEN = "b91ad8c15445553d0c7d1bdc726535b3b52c3a12"  # noqa: S105
NETBOX_HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# Абстрактный класс наблюдателя
class DeviceObserver(ABC):
    @abstractmethod
    def update(self, device: "Device", status: str) -> None: ...


# Конкретные реализации наблюдателей
class Logger(DeviceObserver):
    def update(self, device: "Device", status: str) -> None:
        print(f"[LOG] статус '{device.name}' поменялся на '{status}'")


class Alerting(DeviceObserver):
    def update(self, device: "Device", status: str) -> None:
        if status == "down":
            print(f"[ALERT] '{device.name}' выключено")


class Netbox(DeviceObserver):
    def _update(self, device_id: int, status: str) -> None:
        response = requests.patch(
            url=NETBOX_URL,
            data=json.dumps([{"id": device_id, "status": status}]),
            headers=NETBOX_HEADERS,
            timeout=30,
        )
        new_status = response.json()[0]["status"]["value"]
        hostname = response.json()[0]["name"]
        print(f"[NETBOX] статус '{hostname}' изменен на '{new_status}'")

    def update(self, device: "Device", status: str) -> None:
        response = requests.get(
            NETBOX_URL,
            {"name": device.name},
            headers=NETBOX_HEADERS,
            timeout=30,
            verify=False,
        )
        nb_status = response.json()["results"][0]["status"]["value"]
        device_id = response.json()["results"][0]["id"]
        if status == "up" and nb_status != "active":
            self._update(device_id, "active")
        elif status == "down" and nb_status != "offline":
            self._update(device_id, "offline")
        else:
            print(f"[NETBOX] изменение статуса '{device.name}' не требуется")


# Субъект (сетевое устройство)
class Device:
    def __init__(self, name: str) -> None:
        self.name = name
        self._status = "down"
        self._observers: list[DeviceObserver] = []

    def attach(self, observer: DeviceObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: DeviceObserver) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self, self._status)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value
        self.notify()


if __name__ == "__main__":
    router = Device("dmi01-utica-rtr01")

    logger = Logger()
    alert = Alerting()
    netbox = Netbox()

    router.attach(logger)
    router.attach(alert)
    router.attach(netbox)

    print("--- enable ---")
    router.status = "up"
    print("--- disable ---")
    router.status = "down"
    print("--- enable ---")
    router.status = "up"

    print("--- detach netbox ---")
    router.detach(netbox)
    print("--- enable ---")
    router.status = "up"
    print("--- disable ---")
    router.status = "down"
    print("--- enable ---")
    router.status = "up"
