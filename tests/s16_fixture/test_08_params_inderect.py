import pytest
from pytest import FixtureRequest

from c18_pytest.src.s16_fixture.utils import Vendor, unrange_vlans

# switchport trunk allowed vlan 34,35,37-40,45-50
# port trunk allow-pass vlan 34 to 35 37 to 40 45 to 50


# вариант 1: что бы сохранить vendor, отдаем его и строку в tuple
@pytest.fixture()
def vendor_line(request: FixtureRequest) -> tuple[Vendor, str]:
    if request.param == Vendor.CISCO:
        return (
            request.param,
            "switchport trunk allowed vlan 34,35,37-40,45-50",
        )
    elif request.param == Vendor.HUAWEI:
        return (
            request.param,
            "port trunk allow-pass vlan 34 to 35 37 to 40 45 to 50",
        )


@pytest.mark.parametrize(
    "vendor_line",
    [Vendor.CISCO, Vendor.HUAWEI],
    indirect=True,
)
def test_unrange_vlan_v1(vendor_line: tuple[Vendor, str]) -> None:
    expected = [34, 35, 37, 38, 39, 40, 45, 46, 47, 48, 49, 50]
    # print(f"{vlan_line=}")
    result = list(unrange_vlans(*vendor_line))
    assert result == expected


# вариант 2: что бы вытащить vendor, используем request в тесте
@pytest.fixture()
def config_line(request: FixtureRequest) -> str:
    if request.param == Vendor.CISCO:
        return "switchport trunk allowed vlan 34,35,37-40,45-50"
    elif request.param == Vendor.HUAWEI:
        return "port trunk allow-pass vlan 34 to 35 37 to 40 45 to 50"


@pytest.mark.parametrize(
    ("config_line", "vendor"),
    [
        (Vendor.CISCO, Vendor.CISCO),
        (Vendor.HUAWEI, Vendor.HUAWEI),
    ],
    indirect=["config_line"],
)
def test_unrange_vlan_v2(config_line: str, vendor: Vendor) -> None:
    expected = [34, 35, 37, 38, 39, 40, 45, 46, 47, 48, 49, 50]
    # print(f"{vlan_line=}")
    result = list(unrange_vlans(vendor, config_line))
    assert result == expected


# factory + parametrize
# @pytest.mark.parametrize(
#     argnames=("name", "role", "user_factory"),
#     argvalues=["john", "admin"],
# )
# def test_custom_user_admin(
#     name: str,
#     role: str,
#     user_factory: Callable[..., User],
# ) -> None:
#     admin = user_factory(name=name, role=role)
#     assert admin.name == "John"
#     assert admin.role == "admin"
