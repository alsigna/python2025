from typing import Literal


def get_command_output(
    hostname: str,
    command: str,
    transport: Literal["ssh", "telnet"],
) -> str:
    return f"output of '{command}' from '{hostname}' via '{transport}': some text"


print(
    get_command_output(
        hostname="r1",
        command="show version",
        # transport="ssh",
        transport="netconf",
    ),
)
