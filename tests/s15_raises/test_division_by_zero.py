import pytest


def test_division_by_zero() -> None:
    with pytest.raises(
        expected_exception=(ZeroDivisionError,),
        match=r"division by \w+",
    ) as cm:
        42 / 0  # noqa: B018
    assert isinstance(cm.value, ZeroDivisionError)
    assert isinstance(str(cm.value), str)
    assert str(cm.value) == "division by zero"
