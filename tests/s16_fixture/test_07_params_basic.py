from typing import cast

import pytest
from pytest import FixtureRequest


@pytest.fixture(params=["prod", "stg"])
def netbox(request: FixtureRequest) -> str:
    if request.param == "prod":
        # идем в продовый сервис
        return "admin"
    elif request.param == "stg":
        # какой-то другой код для stg
        return "user"


@pytest.fixture(
    params=[
        "admin",
        "user",
        pytest.param("guest", id="guest-user"),
    ],
)
def role(request: FixtureRequest) -> str:
    return cast(str, request.param)


def test_role_access(role: str) -> None:
    if role == "admin":
        assert True
    elif role == "user":
        assert True
    else:
        assert role == "guest"
