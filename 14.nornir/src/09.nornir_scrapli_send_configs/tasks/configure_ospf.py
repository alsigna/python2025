from nornir.core.task import Result, Task
from nornir_scrapli.tasks.core.send_configs import send_configs
from scrapli.response import MultiResponse

from .generate_ospf_config import generate_ospf_config
from .save_config import save_config


def configure_ospf(task: Task, undo: bool = False) -> Result:
    task_result = task.run(
        task=generate_ospf_config,
        undo=undo,
        severity_level=10,
    )
    target_config: str = task_result.result
    if task.is_dry_run():
        task.name += " (DRY-RUN)"
        target_config = f"Запуск в DRY-RUN режиме, целевая конфигурация не применена:\n\n{target_config}"
        return Result(
            host=task.host,
            result=target_config,
        )
    else:
        if task.host.platform == "huawei_vrp":
            configs = ["mmi-mode enable"] + target_config.splitlines()
        else:
            configs = target_config.splitlines()

        task_result = MultiResponse()

        configure_result = task.run(
            task=send_configs,
            configs=configs,
            stop_on_failed=True,
            severity_level=10,
        )
        task_result.extend(configure_result.scrapli_response)

        save_result = task.run(
            task=save_config,
            severity_level=10,
        )
        task_result.append(save_result.scrapli_response)

        return Result(
            host=task.host,
            result=task_result.result,
            failed=task_result.failed,
            changed=True,
        )
