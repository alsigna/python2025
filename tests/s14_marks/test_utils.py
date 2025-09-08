import pytest

from c18_pytest.src.s14_marks.utils import unrange_huawei_vlans


@pytest.mark.parametrize(
    ("line", "expected_vlans"),
    [
        (
            "port trunk allow-pass vlan 10 to 15",
            [10, 11, 12, 13, 14, 15],
        ),
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
    ],
)
def test_unrange_huawei_vlans(line: str, expected_vlans: list[int]) -> None:
    result = list(unrange_huawei_vlans(line))
    assert result == expected_vlans
    assert result == expected_vlans
