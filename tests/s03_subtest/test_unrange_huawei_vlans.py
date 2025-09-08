# python -m unittest discover -s ./c18_pytest/src/s03_subtest/
# python -m unittest discover -s ./c18_pytest/src/s03_subtest/ -v

from collections.abc import Iterator
from unittest import TestCase

from c18_pytest.src.s03_subtest.utils import unrange_huawei_vlans


class UnrangeHuaweiVlansTestCase(TestCase):
    @property
    def _test_params(self) -> Iterator[tuple[str, list[int]]]:
        for params in [
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
        ]:
            yield params

    def test_unrange_huawei_vlans(self) -> None:
        for line, vlans in self._test_params:
            with self.subTest("unrange huawei vlans", line=line):
                result = list(unrange_huawei_vlans(line))
                self.assertEqual(vlans, result)
