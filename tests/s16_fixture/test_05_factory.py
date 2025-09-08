from collections.abc import Callable
from dataclasses import dataclass

import pytest


@dataclass
class User:
    name: str
    role: str


@pytest.fixture
def user_factory() -> Callable[..., User]:
    def create_user(**kwargs: str) -> User:
        data = {"name": "John", "role": "user", **kwargs}
        return User(**data)

    return create_user


def test_custom_user(user_factory: Callable[..., User]) -> None:
    admin = user_factory(role="admin")
    assert admin.name == "John"
    assert admin.role == "admin"
