from typing import cast

import pytest
from pytest import FixtureRequest


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
