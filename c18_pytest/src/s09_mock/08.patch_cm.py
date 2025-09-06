from typing import Any
from unittest.mock import MagicMock, patch


def netbox_request() -> dict[str, Any]:
    raise RuntimeError("API недоступно")


# def test_api(
#     key: str,
#     value: int,
# ) -> None:
#     assert isinstance(mock_request, MagicMock)
#     data = netbox_request()
#     assert data[key] == value
#     mock_request.assert_called_once()


def test_api(
    key: str,
    value: int,
) -> None:
    assert isinstance(netbox_request, MagicMock)
    data = netbox_request()
    assert data[key] == value
    netbox_request.assert_called_once()


if __name__ == "__main__":
    with patch(
        target="__main__.netbox_request",
        return_value={"id": 1, "name": "test"},
    ):
        test_api("id", 1)
