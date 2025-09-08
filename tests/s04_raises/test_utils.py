# python -m unittest discover -s ./c18_pytest/src/s04_raises/
# python -m unittest discover -s ./c18_pytest/src/s04_raises/ -v

from unittest import TestCase

from c18_pytest.src.s04_raises.models import Vendor
from c18_pytest.src.s04_raises.utils import get_svi_name


class DivisionTestCase(TestCase):
    def test_division_by_zero(self):
        with self.assertRaisesRegex(
            expected_exception=(ZeroDivisionError,),
            expected_regex=r"division by \w+",
        ) as cm:
            42 / 0  # noqa: B018
        self.assertIsInstance(cm.exception, ZeroDivisionError)
        self.assertIsInstance(str(cm.exception), str)
        self.assertEqual(str(cm.exception), "division by zero")


class KnownVendorTestCase(TestCase):
    def test_known_vendor(self):
        for vendor in Vendor._value2member_map_.values():
            with self.subTest(msg="known vendor", vendor=str(vendor)):
                result = get_svi_name(vendor, 100)
            self.assertIsInstance(result, str)


class UnknownVendorTestCase(TestCase):
    def test_unknown_vendor_raises(self):
        with self.assertRaises(AssertionError):
            # get_svi_name("cisco", 100)
            get_svi_name("UNKNOWN_VENDOR_NAME", 100)

    def test_unknown_vendor_raises_regex(self):
        vendor = "UNKNOWN_VENDOR_NAME"
        with self.assertRaisesRegex(
            expected_exception=AssertionError,
            expected_regex=f"Expected code to be unreachable, but got: '{vendor}'",
        ):
            get_svi_name(vendor, 100)

    def test_unknown_vendor_raises_cm(self):
        vendor = "UNKNOWN_VENDOR_NAME"
        with self.assertRaisesRegex(
            expected_exception=AssertionError,
            expected_regex=f"Expected code to be unreachable, but got: '{vendor}'",
        ):
            get_svi_name(vendor, 100)
