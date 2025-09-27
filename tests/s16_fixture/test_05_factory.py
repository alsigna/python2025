from collections.abc import Callable
from dataclasses import dataclass

import pytest


@dataclass
class User:
    name: str
    role: str


@pytest.fixture()
def user_factory() -> Callable[..., User]:
    def create_user(**kwargs: str) -> User:
        data = {"name": "John", "role": "user", **kwargs}
        return User(**data)

    return create_user


def test_custom_user_admin(
    user_factory: Callable[..., User],
) -> None:
    admin = user_factory(name="mike", role="admin")
    assert admin.name == "mike"
    assert admin.role == "admin"


def test_custom_user_staff(
    user_factory: Callable[..., User],
) -> None:
    admin = user_factory(role="staff")
    assert admin.name == "John"
    assert admin.role == "staff"


@pytest.mark.parametrize(
    ("name", "role"),
    [
        ("John", "admin"),
        ("John", "staff"),
        ("mike", "admin"),
        pytest.param("mike", "staff", id="m-staff"),
    ],
)
def test_custom_user(
    name: str,
    role: str,
    user_factory: Callable[..., User],
) -> None:
    user = user_factory(name=name, role=role)
    assert user.name == name
    assert user.role == role
