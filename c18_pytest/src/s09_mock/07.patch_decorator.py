from typing import Any
from unittest.mock import MagicMock, patch


def netbox_request() -> dict[str, Any]:
    raise RuntimeError("API недоступно")


@patch(
    # подменяем netbox_request функцию
    target="__main__.netbox_request",
    # прокидывается как return_value
    return_value={"id": 1, "name": "test"},
)
def test_api(
    key: str,
    value: int,
    # patch самостоятельно создает mock-объект и прокидывает его в функцию
    # внутри test_api netbox_request это mock, за её пределами - оригинальная функция
    mock_request: MagicMock,
) -> None:
    assert isinstance(mock_request, MagicMock)
    data = netbox_request()
    assert data[key] == value
    mock_request.assert_called_once()


if __name__ == "__main__":
    test_api("id", 1)
