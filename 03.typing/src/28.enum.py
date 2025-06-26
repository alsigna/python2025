from enum import StrEnum, auto


class Transport(StrEnum):
    SSH = auto()
    TELNET = auto()


def get_command_output(
    hostname: str,
    command: str,
    transport: Transport,
) -> str:
    return f"output of '{command}' from '{hostname}' via '{transport}': some text"


print(list(Transport))

print(
    get_command_output(
        hostname="r1",
        command="show version",
        transport=Transport.SSH,
        # transport="netconf",
    ),
)
