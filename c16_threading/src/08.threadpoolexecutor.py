import threading
import time
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


def foo(count: int, flag: bool) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        log(f"[{thr_name}]: {i}, flag: {flag}")
        time.sleep(1)


if __name__ == "__main__":
    t0 = perf_counter()
    params = (
        (7, True),
        (5, False),
        (2, True),
    )

    # with ThreadPoolExecutor() as pool:
    #     pool.map(foo, (7, 5, 2), (False, True, False))

    with ThreadPoolExecutor() as pool:
        pool_map = pool.map(foo, *zip(*params, strict=True))
