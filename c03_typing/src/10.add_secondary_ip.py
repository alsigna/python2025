import re
from textwrap import dedent


def get_ip(config: str) -> tuple[str, str, bool]:
    pattern = re.compile(
        pattern=r"ip address (?P<address>\S+) (?P<netmask>\S+)(?P<secondary> secondary)?",
    )
    m = pattern.search(config)
    if m is None:
        return (
            "",
            "",
            False,
        )
    else:
        return (
            m.group("address"),
            m.group("netmask"),
            bool(m.group("secondary")),
        )


if __name__ == "__main__":
    config = dedent(
        """
        interface GigabitEthernet0/1
         description test
         ip address 192.168.1.1 255.255.255.0 secondary
         load-interval 30
        """,
    )

    print(get_ip(config))
