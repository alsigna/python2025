import threading
import time
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


def foo(count: int) -> None:
    log("поток начал выполнение")
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)


if __name__ == "__main__":
    thr1 = threading.Timer(
        interval=5,
        function=foo,
        args=(5,),
    )
    t0 = perf_counter()
    thr1.start()
    log("поток запущен")
