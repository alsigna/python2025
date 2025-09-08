from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest
from pytest_mock import MockerFixture

from c18_pytest.src.s09_mock.src.netbox_api_handler import NetboxAPIHandler


def test_get_cm_raise() -> None:
    exc_string = "метод используется в контекстном менеджере"
    with pytest.raises(
        expected_exception=RuntimeError,
        match=exc_string,
    ) as exc_info:
        api = NetboxAPIHandler("http://netbox.fake.com", "token")
        _ = api.get("/api/status/")
    assert isinstance(exc_info.value, RuntimeError)
    assert str(exc_info.value) == exc_string


def test_get_single_object_response(mocker: MockerFixture) -> None:
    fake_response = SimpleNamespace(
        json=lambda: {
            "hostname": "demo-netbox-stable",
            "installed_apps": {
                "django_filters": "25.1",
            },
            "netbox-version": "4.4.0",
        },
        raise_for_status=lambda: None,
    )
    mocker.patch.object(
        target=httpx.Client,
        attribute="get",
        return_value=fake_response,
    )

    with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        response = api.get("/api/status/")

    assert response[0]["netbox-version"] == "4.4.0"


def test_get_multiply_objects_response(mocker: MockerFixture) -> None:
    # пример части реального ответа
    real_response = {
        "next": None,
        "results": [
            {"name": "default"},
            {"name": "high"},
            {"name": "low"},
        ],
    }
    fake_response = SimpleNamespace(
        json=lambda: real_response,
        raise_for_status=lambda: None,
    )
    mocker.patch.object(httpx.Client, "get", return_value=fake_response)

    with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        response = api.get("/api/core/background-queues/")

    assert len(response) == 3
    assert response == real_response.get("results")


def test_get_multiply_objects_response_with_pages(mocker: MockerFixture) -> None:
    # пример части реального ответа
    first_real_response = {
        "next": "http://netbox.fake.com/api/core/background-queues/?limit=2&offset=2",
        "results": [
            {
                "name": "default",
            },
            {
                "name": "high",
            },
        ],
    }
    # но тут стоит учесть, что если пример ответа делать отдельным объектом, то он будет возвращаться
    # при get, и так как он мутабельный, то будет меняться исходный объект (first_real_response)
    # в .get мы получаем список results и его потом экспендим,
    # поэтому при создании SimpleNamespace нужно deepcopy делать
    first_response = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: deepcopy(first_real_response),
    )
    # либо определять сам словарь в SimpleNamespace, без создания отдельного объекта
    second_response = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {
            "next": None,
            "results": [
                {
                    "name": "low",
                },
            ],
        },
    )
    mocker.patch.object(httpx.Client, "get", side_effect=[first_response, second_response])

    with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        response = api.get("/api/core/background-queues/")

    assert len(response) == 3
    assert response == [
        {"name": "default"},
        {"name": "high"},
        {"name": "low"},
    ]


def test_sync_cm_manual_close() -> None:
    with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        api.__exit__(None, None, None)
        assert api.session is None
    assert api.session is None


async def test_aget_cm_raise(mocker: MockerFixture) -> None:
    exc_string = "метод используется в контекстном менеджере"
    with pytest.raises(
        expected_exception=RuntimeError,
        match=exc_string,
    ) as exc_info:
        api = NetboxAPIHandler("http://netbox.fake.com", "token")
        _ = await api.aget("/api/status/")
    assert isinstance(exc_info.value, RuntimeError)
    assert str(exc_info.value) == exc_string


async def test_aget_single_object_response(mocker: MockerFixture) -> None:
    # пример части реального ответа
    fake_response = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {
            "hostname": "demo-netbox-stable",
            "installed_apps": {
                "django_filters": "25.1",
            },
            "netbox-version": "4.4.0",
        },
    )
    mocker.patch.object(
        httpx.AsyncClient,
        "get",
        new_callable=AsyncMock,
        return_value=fake_response,
    )

    async with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        response = await api.aget("/api/status/")

    # либо mock-объект в отдельную переменную сохранить и её проверять, а не httpx.AsyncClient.get
    httpx.AsyncClient.get.assert_awaited_once_with(url="/api/status/", params=None)
    assert response[0]["netbox-version"] == "4.4.0"


async def test_aget_multiply_objects_response(mocker: MockerFixture) -> None:
    fake_response = SimpleNamespace(
        json=lambda: {
            "next": None,
            "results": [
                {"name": "default"},
                {"name": "high"},
                {"name": "low"},
            ],
        },
        raise_for_status=lambda: None,
    )
    mocker.patch.object(
        httpx.AsyncClient,
        "get",
        new_callable=AsyncMock,
        return_value=fake_response,
    )

    async with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        response = await api.aget("/api/core/background-queues/")

    assert len(response) == 3
    assert response == [
        {"name": "default"},
        {"name": "high"},
        {"name": "low"},
    ]


async def test_aget_multiply_objects_response_with_pages(mocker: MockerFixture) -> None:
    first_response = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {
            "next": "http://netbox.fake.com/api/core/background-queues/?limit=2&offset=2",
            "results": [
                {
                    "name": "default",
                },
                {
                    "name": "high",
                },
            ],
        },
    )
    second_response = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {
            "next": None,
            "results": [
                {
                    "name": "low",
                },
            ],
        },
    )
    mocker.patch.object(
        httpx.AsyncClient,
        "get",
        new_callable=AsyncMock,
        side_effect=[first_response, second_response],
    )

    async with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        response = await api.aget("/api/core/background-queues/")

    assert len(response) == 3
    assert response == [
        {"name": "default"},
        {"name": "high"},
        {"name": "low"},
    ]


async def test_async_cm_manual_close() -> None:
    async with NetboxAPIHandler("http://netbox.fake.com", "token") as api:
        await api.__aexit__(None, None, None)
        assert api.session is None
    assert api.session is None
    assert api.session is None
