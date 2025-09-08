# python -m unittest discover -s ./c18_pytest/src/s03_subtest/
# python -m unittest discover -s ./c18_pytest/src/s03_subtest/ -v

from unittest import TestCase

from c18_pytest.src.s03_subtest.utils import concat


class ConcatLoopTestCase(TestCase):
    def test_concat_loop(self) -> None:
        for a, b, expected in [
            (1, 2, 3),
            (0, 3, 3),
            (-1, 1, 0),
            ("a", "b", "ab"),
            ("abc", "def", "abcdef"),
            ("", "", ""),
            (" ", " ", "  "),
            ("a", " ", "a "),
        ]:
            result = concat(a, b)
            self.assertEqual(expected, result)


class ConcatSubTestTestCase(TestCase):
    def test_concat_sub_test(self) -> None:
        for a, b, c in [
            (1, 2, 3),
            (0, 3, 3),
            (-1, 1, 0),
            ("a", "b", "ab"),
            ("abc", "def", "abcdef"),
            ("", "", ""),
            (" ", " ", "  "),
            ("a", " ", "a "),
        ]:
            with self.subTest("concat test", a=a, b=b, expected=c):
                result = concat(a, b)
                self.assertEqual(c, result)
