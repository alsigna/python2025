import time
from typing import cast
from unittest.mock import MagicMock, create_autospec


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_version(self) -> str:
        # долгие вычисления
        time.sleep(2)
        return f"{self.ip}: original version"

    def parse_output(self, output: str) -> str:
        return f"{self.ip}: {output[::-1]}"


if __name__ == "__main__":
    # без spec
    print("без spec")
    mock = MagicMock(
        get_version=MagicMock(return_value=42),
    )
    print(mock.get_version())
    print(mock.anything())
    print(mock.not_existing_attr.foo.bar("a", "b", 1, 2))

    # с использованием spec
    print("spec")
    mock = MagicMock(
        spec=Device,
        get_version=MagicMock(return_value=42),
    )
    print(mock.get_version())
    print(mock.get_version(1, 2, 3))
    try:
        print(mock.anything())
    except AttributeError as exc:
        print(f"работа spec. {exc.__class__.__name__}: {str(exc)}")

    # с использованием autospec
    print("autospec")
    mock = create_autospec(spec=Device)
    mock.get_version.return_value = 42
    print(mock.get_version())
    try:
        print(mock.get_version(1, 2, 3))
    except TypeError as exc:
        print(f"работа autospec. {exc.__class__.__name__}: {str(exc)}")

    # spec через список ограничивает имена
    print("spec list")
    mock = MagicMock(
        spec=["foo", "zoo"],
        foo=MagicMock(return_value=42),
        zoo=MagicMock(return_value=None),
    )
    try:
        print(mock.boo())
    except AttributeError as exc:
        print(f"работа spec list. {exc.__class__.__name__}: {str(exc)}")
