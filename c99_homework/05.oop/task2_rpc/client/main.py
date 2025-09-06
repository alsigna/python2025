from python2025_alexigna.hw_05_oop.task2_rpc.rpc import RPC

with RPC() as rpc:
    # tasks = [
    #     rpc.hello(user="admin-1", count=3),
    #     rpc.hello(user="admin-2", count=3),
    #     # rpc.bad_hello(user="admin-3", count=3),
    #     rpc.hello(user="admin-4", count=3),
    # ]
    tasks = [
        rpc.send_command("cisco_iosxe", "192.168.122.101", "show clock"),
        rpc.send_command("cisco_iosxe", "192.168.122.102", "show clock"),
    ]
    rpc.gather(*tasks)

    for task in tasks:
        if task.result is None:
            continue
        response = task.result
        print("-" * 10)
        print(task.job_id)
        print(response.host)
        print(response.channel_input)
        print(response.result)
