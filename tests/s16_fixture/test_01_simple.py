import pytest


@pytest.fixture()
def sample() -> list[int]:
    return [1, 2, 3]


def test_sum(sample: list[int]) -> None:
    assert sum(sample) == 6


def test_max(sample: list[int]) -> None:
    assert max(sample) == 3


def test_min(sample: list[int]) -> None:
    assert min(sample) == 1
