# поменять конфиг, что бы на reload in было два запроса, показать проблему
# и дать ДЗ на модификацию
from time import perf_counter
from typing import Any

from scrapli import Scrapli
from scrapli.response import MultiResponse, Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def send_command_v1(device: dict[str, Any], command: str) -> MultiResponse:
    with Scrapli(
        **device,
        channel_log="./debug.log",
    ) as ssh:
        output = ssh.send_commands(
            commands=[command],
            timeout_ops=5,
        )
    return output


def send_command_v2(device: dict[str, Any], command: str) -> MultiResponse:
    with Scrapli(
        **device,
        channel_log="./debug.log",
    ) as ssh:
        result = MultiResponse()
        output: Response = ssh.send_and_read(
            channel_input=command,
            expected_outputs=[
                ssh.comms_prompt_pattern,
                "[confirm]",
                "[yes/no]",
            ],
            timeout_ops=5,
        )
        result.append(output)
        if "[confirm]" in output.result:
            result.append(ssh.send_command("\n"))
        elif "[yes/no]" in output.result:
            result.append(ssh.send_command("yes"))
        return result


if __name__ == "__main__":
    t0 = perf_counter()
    try:
        result = send_command_v2(device, "reload in 30")
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
    finally:
        print(f"\nвремя работы: {perf_counter() - t0:.4f} сек")
