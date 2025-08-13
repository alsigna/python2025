import threading
import time

lock = threading.Lock()

count = 0
threads = []


def foo() -> None:
    global count
    for _ in range(10):
        count += 1
        time.sleep(0.1)
        print(count)


for _ in range(5):
    threads.append(threading.Thread(target=foo))

for thr in threads:
    thr.start()

for thr in threads:
    thr.join()


print("=======")

count = 0
threads = []


def boo() -> None:
    global count
    for _ in range(10):
        lock.acquire()
        count += 1
        time.sleep(0.1)
        print(count)
        lock.release()


def zoo() -> None:
    # тоже самое, что и boo(), только через with
    global count
    for _ in range(10):
        with lock:
            count += 1
            time.sleep(0.1)
            print(count)


for _ in range(5):
    threads.append(threading.Thread(target=zoo))
    # threads.append(threading.Thread(target=boo))

for thr in threads:
    thr.start()

for thr in threads:
    thr.join()
