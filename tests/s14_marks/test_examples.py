import pytest


@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_mul(x, y) -> None:
    assert x * y > 0


@pytest.mark.parametrize(
    argnames=("x", "expected"),
    argvalues=[(1, 2), (3, 4)],
    ids=["one", "two"],
)
def test_inc_v1(x: int, expected: int) -> None:
    assert x + 1 == expected


@pytest.mark.parametrize(
    argnames=("x", "expected"),
    argvalues=[
        pytest.param(1, 2, id="one"),
        pytest.param(3, 4, id="two"),
    ],
)
def test_inc_v2(x: int, expected: int) -> None:
    assert x + 1 == expected
