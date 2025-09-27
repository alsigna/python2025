from pytest import MonkeyPatch


def get_user_id():
    return 42


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    def show_version(self) -> str:
        raise NotImplementedError("еще не реализовано")

    def reload(self) -> None:
        raise NotImplementedError("еще не реализовано")


# у setattr два варианта передачи target (первый аргумент):
# - строка первым аргументом: monkeypatch.setattr("os.getcwd", lambda: "/")
# - объект первым аргументом: monkeypatch.setattr(os, "getcwd", lambda: "/")
def test_patch_function(monkeypatch: MonkeyPatch) -> None:
    def fake_get_user_id():
        return 99

    assert isinstance(monkeypatch, MonkeyPatch)
    print(type(monkeypatch))
    monkeypatch.setattr(
        target=__name__ + ".get_user_id",
        name=fake_get_user_id,
    )
    # monkeypatch.setattr(
    #     target=sys.modules[__name__],
    #     name="get_user_id",
    #     value=fake_get_user_id,
    # )

    assert get_user_id() == 99


def test_device_show_version(monkeypatch: MonkeyPatch) -> None:
    def fake_show_version(self):
        return "1.2.3"

    monkeypatch.setattr(Device, "show_version", property(fake_show_version))

    device = Device("192.168.1.1")
    assert device.show_version == "1.2.3"


def test_device_reload(monkeypatch: MonkeyPatch) -> None:
    def fake_reload(self):
        self._reloaded = True

    monkeypatch.setattr(Device, "reload", fake_reload)

    device = Device("192.168.1.1")
    device.reload()
    assert device._reloaded is True  # noqa: SLF001
