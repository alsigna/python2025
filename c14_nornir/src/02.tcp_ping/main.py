from pathlib import Path

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.networking import tcp_ping

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    result = nr.run(
        task=tcp_ping,
        ports=[22, 23, 24],
        timeout=3,
    )
    print_result(result)
