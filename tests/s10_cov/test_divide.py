# python -m unittest discover -s ./c18_pytest/src/s10_cov/ -v
# coverage run -m unittest discover -s ./c18_pytest/src/s10_cov/ -v
from unittest import TestCase

from c18_pytest.src.s10_cov.divide import divide


class DivideTestCase(TestCase):
    def test_divide(self) -> None:
        result = divide(10, 5)
        expected_result = 2.0
        self.assertEqual(expected_result, result)
