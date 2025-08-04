from collections import deque
from concurrent.futures import ThreadPoolExecutor

from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Result, Task


class FibonacciThreadedRunner:
    def __init__(self, **kwargs):
        self.max_workers = kwargs.get("num_workers", 20)
        self.fib_sequence = self._generate_fib_sequence_up_to(self.max_workers)

    def _generate_fib_sequence_up_to(self, max_value: int) -> list[int]:
        seq = [1, 2]
        while seq[-1] + seq[-2] <= max_value:
            seq.append(seq[-1] + seq[-2])
        return seq

    def run(self, task: Task, hosts: list[Host]) -> AggregatedResult:
        result = AggregatedResult(task.name)
        host_queue = deque(hosts)
        wave = 0
        failed = False

        while host_queue:
            wave_size = self.fib_sequence[wave] if wave < len(self.fib_sequence) else self.max_workers
            current_batch = [host_queue.popleft() for _ in range(min(wave_size, len(host_queue)))]

            futures = []
            with ThreadPoolExecutor(wave_size) as pool:
                for host in current_batch:
                    future = pool.submit(task.copy().start, host)
                    futures.append(future)

            for future in futures:
                worker_result = future.result()
                if worker_result.failed:
                    failed = True
                result[worker_result.host.name] = worker_result

            if failed:
                for host in host_queue:
                    host_result = MultiResult(name=task.name)
                    host_result.append(
                        Result(
                            host=host,
                            changed=False,
                            failed=False,
                            result="skipped",
                        ),
                    )
                    result[host.name] = host_result
                return result
            else:
                wave += 1

        return result
