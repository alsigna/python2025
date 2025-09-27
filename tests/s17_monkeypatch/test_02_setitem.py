from collections.abc import Generator
from typing import Any

import pytest
from pytest import MonkeyPatch

scrapli = {
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def test_dict_scrapli_password(monkeypatch: MonkeyPatch) -> None:
    password = "fake"  # noqa: S105
    monkeypatch.setitem(dic=scrapli, name="auth_password", value=password)
    assert scrapli["auth_password"] == password


# но если наш словарь идет через property, например как в class Device,
# то он меняется через setattr, а не setitem


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "host": self.ip,
            "auth_username": "admin",
            "auth_password": "P@ssw0rd",
            "auth_strict_key": False,
            "ssh_config_file": True,
        }


def test_class_scrapli_password(monkeypatch: MonkeyPatch) -> None:
    def fake_scrapli(self):
        data = original_scrapli(self).copy()
        data["auth_password"] = password
        return data

    original_scrapli = Device.scrapli.fget
    password = "fake"  # noqa: S105

    monkeypatch.setattr(Device, "scrapli", property(fake_scrapli))

    ip = "10.0.0.1"
    device = Device(ip)

    assert device.scrapli["auth_password"] == password
    assert device.ip == ip


# Если патчинг нужен в нескольких тестах, то мы можем вынести это в фикстуру:
# что стоит помнить: у monkeypatch scope всегда function, поэтому мы не можем
# делать свои фикстуры с более широким scope. scope="function" - по умолчанию
# можно не писать, но явно отметим это, что бы не забыть
@pytest.fixture(scope="function")
def patched_device(monkeypatch: MonkeyPatch) -> Generator[None]:
    def fake_scrapli(self):
        data = original_scrapli(self).copy()
        data["auth_password"] = "fake"  # noqa: S105
        return data

    original_scrapli = Device.scrapli.fget

    monkeypatch.setattr(Device, "scrapli", property(fake_scrapli))

    # используем yield а не return, так как если фикстура закончится, изменения будут откачены
    yield


def test_class_scrapli_password_with_fixture(patched_device: None) -> None:
    ip = "10.0.0.1"
    device = Device(ip)

    assert device.scrapli["auth_password"] == "fake"  # noqa: S105
    assert device.ip == ip
