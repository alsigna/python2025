from unittest.mock import patch

from pytest import MonkeyPatch
from pytest_mock import MockerFixture

device = {
    "platform": "cisco_iosxe",
    "host": "127.0.0.1",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


# патч через unittest с контекстным менеджеров
def test_unittest_patch_dict() -> None:
    with patch.dict(
        device,
        {"auth_username": "scrapli", "auth_password": "scrapli"},
    ):
        assert device["auth_username"] == "scrapli"
        assert device["auth_password"] == "scrapli"  # noqa: S105


# патч через unittest с декоратором
@patch.dict(device, {"auth_username": "scrapli", "auth_password": "scrapli"})
def test_unittest_patch_dict_decorator() -> None:
    assert device["auth_username"] == "scrapli"
    assert device["auth_password"] == "scrapli"  # noqa: S105


# патч через monkeypatch
def test_monkeypatch_patch_dict(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setitem(device, "auth_username", "scrapli")
    monkeypatch.setitem(device, "auth_password", "scrapli")
    assert device["auth_username"] == "scrapli"
    assert device["auth_password"] == "scrapli"  # noqa: S105


# патч через pytest-mock
def test_mock_patch_dict(mocker: MockerFixture) -> None:
    mocker.patch.dict(
        device,
        {"auth_username": "scrapli", "auth_password": "scrapli"},
    )
    assert device["auth_username"] == "scrapli"
    assert device["auth_password"] == "scrapli"  # noqa: S105
