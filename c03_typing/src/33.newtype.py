from ipaddress import IPv4Address
from typing import NewType

IP = NewType("IP", str)


def ip(value: str) -> IP:
    try:
        IPv4Address(value)
    except Exception as exc:
        raise ValueError(f"incorrect ip: {str(exc)}") from exc
    else:
        return IP(value)


def connect_to_device(ip: IP) -> str:
    print(f"{isinstance(ip, str)=}")
    result = "Ok"
    return f"{ip=}, {result=}"


if __name__ == "__main__":
    print(connect_to_device(ip("1.2.3.4")))
    print("-" * 10)
    print(connect_to_device(ip("1.2.3.400")))
