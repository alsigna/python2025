# python -m unittest discover -s ./c18_pytest/src/s02_formatter_unittest/ -v

from textwrap import dedent
from unittest import TestCase

from c18_pytest.src.s02_formatter_unittest.formatters import JunkLineStripper


class JunkLineStripperTestCase(TestCase):
    def _get_raw_and_expected_strings(self) -> tuple[str, str]:
        raw_str = dedent(
            """
            Software Version V200VERSION
            #
            Software Version V200VERSION
            sysname router1
            #
            Software Version V200VERSION
            """,
        )
        expected_str = dedent(
            """
            #
            sysname router1
            #
            """,
        )
        return raw_str, expected_str

    def test_junk_line_strip(self) -> None:
        input_str, expected_str = self._get_raw_and_expected_strings()
        result_str = JunkLineStripper.format(input_str)
        self.assertEqual(expected_str, result_str)
