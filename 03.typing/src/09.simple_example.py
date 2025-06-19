import re
from textwrap import dedent


def get_ip(config: str) -> tuple[str, str]:
    pattern = re.compile(
        pattern=r"ip address (?P<address>\S+) (?P<netmask>\S+)",
    )
    m = pattern.search(config)
    if m is None:
        return "", ""
    else:
        return (
            m.group("address"),
            m.group("netmask"),
        )


if __name__ == "__main__":
    config = dedent(
        """
        interface GigabitEthernet0/1
         description test
         ip address 192.168.0.1 255.255.255.0
         load-interval 30
        """,
    )

    print(get_ip(config))
