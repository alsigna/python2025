# python -m unittest discover -s ./c18_pytest/src/s10_cov/ -v
# coverage run -m unittest discover -s ./c18_pytest/src/s10_cov/ -v
from unittest import TestCase

from c18_pytest.src.s10_cov.is_even import is_even


class IsEvenTestCase(TestCase):
    def test_divide(self) -> None:
        even = is_even(10)
        self.assertTrue(even)
        # branch = true
        # odd = is_even(5)
        # self.assertFalse(odd)
