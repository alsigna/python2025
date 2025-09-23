import pytest

from c18_pytest.src.s14_marks.utils import unrange_huawei_vlans


@pytest.mark.parametrize(
    argnames=("line", "expected_vlans"),
    argvalues=[
        # simple rage
        (
            "port trunk allow-pass vlan 10 to 15",
            [10, 11, 12, 13, 14, 15],
        ),
        # mixed range
        (
            "port trunk allow-pass vlan 34 to 35 37 to 40 45 to 50",
            [34, 35, 37, 38, 39, 40, 45, 46, 47, 48, 49, 50],
        ),
        (
            "port trunk allow-pass vlan 100",
            [100],
        ),
        (
            "port trunk allow-pass vlan 100 110",
            [100, 110],
        ),
        pytest.param(
            "port trunk allow-pass vlan 101",
            [100],
            marks=pytest.mark.xfail(reason="баг 123"),
            id="101 vlan",
        ),
    ],
)
def test_unrange_huawei_vlans(
    line: str,
    expected_vlans: list[int],
) -> None:
    result = list(unrange_huawei_vlans(line))
    assert result == expected_vlans
