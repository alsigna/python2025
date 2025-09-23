import pytest

from c18_pytest.src.s15_raises.models import Vendor
from c18_pytest.src.s15_raises.utils import get_svi_name


class TestGetSVIName:
    TEST_VLAN_ID = 100

    @pytest.mark.parametrize("vendor", list(Vendor._value2member_map_.values()))
    def test_known_vendor(self, vendor: str) -> None:
        result = get_svi_name(vendor, 100)
        assert isinstance(result, str)

    @pytest.mark.parametrize(
        ("vendor", "expected"),
        [
            ("cisco", f"Vlan{TEST_VLAN_ID}"),
            ("huawei", f"Vlanif{TEST_VLAN_ID}"),
        ],
    )
    def test_known_vendor_with_value(self, vendor: str, expected: str) -> None:
        result = get_svi_name(vendor, self.TEST_VLAN_ID)
        assert result == expected

    def test_unknown_vendor(self):
        with pytest.raises(AssertionError):
            # тест падает, если исключение не возбуждено
            # get_svi_name("cisco", 100)
            get_svi_name("UNKNOWN_VENDOR_NAME", 100)
