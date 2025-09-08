# python -m unittest discover -s ./c18_pytest/src/s01_simple_unittest/
# python -m unittest discover -s ./c18_pytest/src/s01_simple_unittest/ -v

import string
from random import choices, randint
from unittest import TestCase

from c18_pytest.src.s01_simple_unittest.utils import concat


class ConcatTestCase(TestCase):
    def test_concat_int(self) -> None:
        num_a = randint(1, 10)
        num_b = randint(1, 10)
        expected = num_a + num_b
        result = concat(num_a, num_b)
        self.assertEqual(expected, result)

    def _get_random_string(self, length: int = 4) -> str:
        return "".join(choices(string.ascii_letters + string.digits, k=length))

    def test_concat_str(self) -> None:
        str_a = self._get_random_string()
        str_b = self._get_random_string()
        expected = str_a + str_b
        result = concat(str_a, str_b)
        self.assertEqual(expected, result)
