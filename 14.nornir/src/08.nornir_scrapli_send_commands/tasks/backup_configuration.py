from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from nornir.core.task import Result, Task
from nornir_scrapli.tasks import send_commands
from nornir_utils.plugins.tasks.files import write_file


def backup_configuration(task: Task, backup_folder: Path) -> Result:
    now = datetime.now(tz=ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder.mkdir(parents=True, exist_ok=True)
    filename = Path(backup_folder, f"{task.host.name}_{now}.txt")

    result = task.run(
        task=send_commands,
        commands=task.host["backup_commands"],
        severity_level=10,
    )
    backup_result = result.result

    task.run(
        task=write_file,
        filename=str(filename),
        content=backup_result,
        severity_level=10,
    )

    result = "вывод команд:\n"
    for cmd in task.host["backup_commands"]:
        result += f"  - {cmd}\n"
    result += f"\nсохранен в файл '{filename.relative_to(backup_folder)}'"

    return Result(host=task.host, result=result)
