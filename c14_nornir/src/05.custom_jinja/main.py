from pathlib import Path

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from tasks import custom_jinja

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    result = nr.run(
        name="генерация конфигурации ospf",
        task=custom_jinja,
        template=Path(cwd, "templates", "ospf.j2"),
    )
    print_result(result)
