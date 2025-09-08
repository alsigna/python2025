# ruff: noqa: S105
from typing import Any
from unittest.mock import PropertyMock, patch

import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture


# оригинальный класс
class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "platform": "cisco_iosxe",
            "host": self.ip,
            "auth_username": "admin",
            "auth_password": "P@ssw0rd",
            "auth_strict_key": False,
            "ssh_config_file": True,
        }


# патч property через unittest
def test_patch_scrapli_password_unittest() -> None:
    def fake_scrapli(self) -> dict[str, Any]:
        data = original(self).copy()
        data["auth_password"] = "scrapli"
        return data

    original = Device.scrapli.fget
    device = Device("1.2.3.4")

    with patch.object(Device, "scrapli", property(fake_scrapli)):
        assert device.scrapli["auth_password"] == "scrapli"


# патч property через monkeypatch с выносом в отдельную фикстуру
@pytest.fixture()
def patched_device(monkeypatch: MonkeyPatch):
    def fake_scrapli(self):
        data = original(self).copy()
        data["auth_password"] = "scrapli"
        return data

    original = Device.scrapli.fget
    monkeypatch.setattr(Device, "scrapli", property(fake_scrapli))
    yield


def test_patch_scrapli_password_monkeypatch(patched_device: None) -> None:
    device = Device("1.2.3.4")
    assert device.scrapli["auth_password"] == "scrapli"


# патч property через python-mock с выносом в отдельную фикстуру
@pytest.fixture()
def patched_device_pytest_mock(mocker: MockerFixture):
    def fake_scrapli(self):
        data = original(self).copy()
        data["auth_password"] = "scrapli"
        return data

    original = Device.scrapli.fget
    mocker.patch.object(Device, "scrapli", property(fake_scrapli))
    yield


def test_patch_scrapli_password_pytest_mock(patched_device_pytest_mock: None) -> None:
    device = Device("1.2.3.4")
    assert device.scrapli["auth_password"] == "scrapli"
