# Есть три вендора: cisco, huawei, arista. Нужно написать функцию "svi_name(vendor_name, svi_id)"
# которая по переданному вендору и номеру интерфейса возвращает имя SVI интерфейса:
#  - cisco - Vlan<id>
#  - huawei - Vlanif<id>
#  - arista - Vlan<id>
# сделать аннотацию кода + сделать так, что бы при добавлении нового вендора тайп-чекер (mypy)
# говорил о том, что функцию svi_name нужно дополнить для учета добавленного вендора.
# в примере вызовов вендора перечислены в StrEnum, но можно сделать другим подходом, если есть желание

if __name__ == "__main__":
    assert svi_name(Vendor.CISCO, 10) == "Vlan10"
    assert svi_name(Vendor.HUAWEI, 10) == "Vlanif10"
    assert svi_name(Vendor.ARISTA, 10) == "Vlan10"
