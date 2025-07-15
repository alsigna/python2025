# from python2025_alexigna.hw_05_oop.task2_rpc.client.device_abc import CiscoIOSXE, DeviceABC, HuaweiVRP
from scrapli.response import Response

from python2025_alexigna.hw_05_oop.task2_rpc.client.device_protocol import CiscoIOSXE, Device, HuaweiVRP
from python2025_alexigna.hw_05_oop.task2_rpc.rpc import RPC, RPCResult
from python2025_alexigna.hw_05_oop.task2_rpc.rpc.exceptions import RPCError


def main_gather() -> None:
    with RPC() as rpc:
        devices: list[Device] = [
            CiscoIOSXE("192.168.122.101"),
            CiscoIOSXE("192.168.122.102"),
            HuaweiVRP("192.168.122.103"),
            CiscoIOSXE("192.168.122.101"),
            CiscoIOSXE("192.168.122.102"),
            HuaweiVRP("192.168.122.103"),
        ]
        tasks: dict[RPCResult[Response], Device] = {}
        for device in devices:
            job = rpc.send_command(str(device.platform), device.host, device.command)
            tasks[job] = device
            device.log_debug("задача %s запланирована", job.job_id)

        rpc.gather(*tasks.keys())

        for task, device in tasks.items():
            if task.result is None:
                device.log_error("не удалось получить результат выполнения задачи")
                continue
            else:
                device.log_succeeded("задача успешно выполнена")
            response = task.result
            device.log_info(response.channel_input)
            device.log_info(response.result)


def main_as_completed() -> None:
    with RPC() as rpc:
        devices: list[Device] = [
            CiscoIOSXE("192.168.122.101"),
            CiscoIOSXE("192.168.122.102"),
            HuaweiVRP("192.168.122.103"),
            CiscoIOSXE("192.168.122.101"),
            CiscoIOSXE("192.168.122.102"),
            HuaweiVRP("192.168.122.103"),
        ]
        tasks: dict[RPCResult[Response], Device] = {}

        for device in devices:
            job = rpc.send_command(str(device.platform), device.host, device.command)
            tasks[job] = device
            device.log_debug("задача %s запланирована", job.job_id)

        for task in rpc.as_completed(*tasks.keys(), timeout=2):
            if task.result is None:
                device.log_error("не удалось получить результат выполнения задачи")
                continue
            else:
                device.log_succeeded("задача успешно выполнена")
            response = task.result
            device.log_info(response.channel_input)
            device.log_info(response.result)


if __name__ == "__main__":
    # main_gather()
    main_as_completed()
