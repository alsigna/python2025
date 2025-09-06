# написать функцию генератор, которая принимает строку вида 'port trunk allow-pass vlan <vlans>'
# и на каждой итерации возвращает очередной vlan из разрешенных на порту, при этом vlan внутри
# диапазонов ' to ' не теряются, а так же возвращаются. Т.е.
#  - port trunk allow-pass vlan 10          -> результат 10
#  - port trunk allow-pass vlan 10 13       -> результат 10, 13
#  - port trunk allow-pass vlan 10 to 13    -> результат 10, 11, 12, 13
#  - port trunk allow-pass vlan 10 to 13 15 -> результат 10, 11, 12, 13, 15


def unrange_huawei_vlans(allow_pass_vlan_line):
    # yield vlan


if __name__ == "__main__":
    for config_line, expected_vlan_list in (
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
    ):
        received_vlan_list = list(unrange_huawei_vlans(config_line))
        print(f"{received_vlan_list=}")
        print(f"{expected_vlan_list=}")
        assert expected_vlan_list == received_vlan_list
