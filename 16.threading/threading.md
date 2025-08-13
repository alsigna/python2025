# Threading

- [Threading](#threading)
  - [Описание](#описание)
  - [Использование](#использование)
    - [Создание и запуск потока](#создание-и-запуск-потока)
    - [Ожидание завершения потоков](#ожидание-завершения-потоков)
    - [Daemons](#daemons)
    - [Синхронизация потоков](#синхронизация-потоков)
    - [Отложенный запуск](#отложенный-запуск)
    - [Семафоры](#семафоры)
    - [Возвращаемое значение](#возвращаемое-значение)
    - [Исключения](#исключения)
  - [`ThreadPoolExecutor`](#threadpoolexecutor)
    - [Описание](#описание-1)
    - [Создание](#создание)
    - [`map`](#map)
    - [`submit`](#submit)
    - [`as_completed`](#as_completed)

## Описание

`threading` - встроенная библиотека python для работы с потоками. Позволяет создавать/запускать/контролировать/удалять потоки и выносить в них выполнение отдельных функций.

## Использование

Для управления потоками библиотека `threading` предоставляет ряд функций, например:

- `threading.active_count()`:  количество активных потоков
- `threading.current_thread()`: текущий поток

и другие, которые будут рассмотрены по мере знакомства в библиотекой.

Сам же поток описывается классом `Thread` и так же имеет свои методы и атрибуты, например:

- `Thread.name`: имя потока
- `Thread.start()`: запустить поток

### Создание и запуск потока

Поток создается как экземпляр класса `Thread`. Аргументами являются:

- `target` - ссылка на вызываемый объект (функцию)
- `args` - кортеж позиционных аргументов целевой функции
- `kwargs` - словарь ключевых аргументов целевой функции
- `name` - имя потока

запуск производится методом `start`

```python
import threading
import time

def foo(count: int) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)

thr1 = threading.Thread(
    target=foo,
    args=(5,),
    name="thr-1",
)

thr2 = threading.Thread(
    target=foo,
    kwargs={"count": 3},
    name="thr-2",
)

thr1.start()
thr2.start()

print("потоки запущены")
```

Число активных потоков можно получить функцией `threading.active_count()`, а сами потоки: `threading.enumerate()`.

```python
print(f"число активных потоков: {threading.active_count()}")
# >>> 3
print(f"список всех потоков: {threading.enumerate()}")
# >>> [<_MainThread(MainThread, started 8386513920)>, <Thread(thr-1, started 6110867456)>, <Thread(thr-2, started 6127693824)>]
```

MainThread присутствует всегда, это работа основного скрипта. Это такой же объект Thread, который можно получить как элемент списка через обращение по индексу, так и через специальную функцию

```python
main_thr = threading.main_thread()
print(f"имя потока: {main_thr.name}")
# >>> имя потока: MainThread
print(f"id потока: {main_thr.ident}")
# >>> id потока: 8386513920
```

### Ожидание завершения потоков

Для ожидания завершения используется метод `join`. При вызове этого метода работа скрипта останавливается до завершения работы потока.

```python
import threading
import time

def foo(count: int) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)
    return count * 10

thr1 = threading.Thread(
    target=foo,
    args=(5,),
    name="thr-1",
)

thr2 = threading.Thread(
    target=foo,
    kwargs={"count": 3},
    name="thr-2",
)

thr1.start()
thr2.start()

print("потоки запущены")

for t in (thr1, thr2):
    t.join()
    print(f"поток {t.name} завершился")

print("скрипт завершен")
```

### Daemons

Отличие потоков-демонов от обычных в том, что демоны принудительно завершаются при завершении основного потока. Обычные потоки продолжают работать до полного исполнения инструкций, и основной поток (программа) будет завершена только после завершения всех обычных потоков.

```python
import threading
import time


def foo(count: int) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)
    return count * 10


thr1 = threading.Thread(
    target=foo,
    args=(5,),
    name="thr-1",
    daemon=True,
)

thr2 = threading.Thread(
    target=foo,
    kwargs={"count": 3},
    name="thr-2",
)

thr1.start()
thr2.start()
```

### Синхронизация потоков

Для синхронизации потоков существуют механизмы блокировок Lock и RLock. Например, если нужно получить эксклюзивный доступ к ресурсу (переменной), тогда используется механизм Lock/RLock, и остальные потоки будут вынуждены ждать, пока блокировка не будет снята. Разница между Lock и RLock в том, что Lock может снять любой поток, даже если не он устанавливал блокировку, а блокировку RLock может снять только поток, которые её поставил.

Работать с блокировкой можно вызывая методы `acquire`/`release` для установки/снятия, или через контекстный менеджер.

```python
def boo() -> None:
    lock.acquire()
    # some work
    lock.release()


def zoo() -> None:
    with lock:
        # some work
```

### Отложенный запуск

При необходимости отложенного запуска потока для создания объекта вместо класса `Thread` используется класс `Timer`. Параметры те же самые + дополнительно указывается количество секунд, через которое нужно запустить поток.

```python
import threading
import time


def foo(count: int) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)


thr1 = threading.Timer(
    interval=10,
    function=foo,
    args=(5,),
)


thr1.start()
```

### Семафоры

Семафор счетчик, позволяющий ограничить максимальное число одновременно работающих потоков. Например если значение семафора установлено на 2, а запускается 10 потоков, то одновременно в работе будут находится только 2 потока, остальные будут ожидать в очереди, пока не какой-нибудь из уже работающих потоков не завершится.

```python
from threading import BoundedSemaphore, Thread

max_connections = 2
pool = BoundedSemaphore(max_connections)

def foo() -> None:
    with pool:
        # some work

threads: list[Thread] = []
for _ in range(10):
    threads.append(Thread(target=foo))

for t in threads:
    t.start()

for t in threads:
    t.join()
```

### Возвращаемое значение

По умолчанию потоки не возвращают значения, что бы получать результаты работы потоков для дальнейшего анализа, нужно использовать кастомные классы, например такого вида:

```python
class ThreadWithResult(Thread):
    def __init__(
        self,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(group, target, name, *args, **kwargs)
        self._result = None

    def run(self) -> None:
        if self._target is not None:
            self._result = self._target(*self._args, **self._kwargs)

    def join(self, *args: Any) -> Any:
        super().join(*args)
        return self._result
```

Теперь метод `join` будет возвращать результат выполнения target функции.

### Исключения

Перехват исключений, возникших внутри потока можно выполнять через специальную функцию `threading.excepthook`. В эту функцию передается информация по возникшему исключению. По умолчанию она просто выводит трейсбек в терминал, поток при этом завершается. Но можно переопределить эту функцию и обрабатывать исключения требуемым способом.

```python
def custom_hook(args: Any) -> None:
    exc_type, exc_value, exc_traceback, exc_thread = args
    print(f"Тип исключения: {exc_type.__name__}")
    print(f"Сообщение исключения: {exc_value}")
    print(f"Номер потока: {exc_thread.ident}")
    print(f"Имя потока: {exc_thread.name}")
    print(f"Функция потока: {exc_thread._target.__name__}")  # noqa:SLF001
    print(f"Аргументы потока: {exc_thread._args[0]}")  # noqa:SLF001
    # print("Traceback исключения:")
    # traceback.print_tb(exc_traceback)

threading.excepthook = custom_hook
```

## `ThreadPoolExecutor`

### Описание

Работа с потоками достаточно распространенная операция, поэтому есть высокоуровневые классы для работы с ними. Встроенная библиотека `concurrent` предоставляет класс `ThreadPoolExecutor` для конкурентного выполнения задач в потоках (модулем предоставляется так же `ProcessPoolExecutor` для параллельного запуска процессов). Использование `ThreadPoolExecutor` значительно упрощает использование потоков, и все применение сводится к тому, что нужно отправить задачу на выполнение и получить результат при необходимости.

Пул потоков и пул процессов имеют общий интерфейс, поэтому переход между потоками и процессами так же может быть выполнен достаточно просто. В качестве общего родителя `ThreadPoolExecutor` и `ProcessPoolExecutor` используют абстрактный класс `concurrent.futures.Executor`.

### Создание

Пул потоков создается классом `concurrent.futures.ThreadPoolExecutor`, передаваемые аргументы:

- `max_workers` - число одновременно выполняемых потоков
- `thread_name_prefix` - префикс имени потока
- `initializer` / `initargs` - инициализатор и его аргументы (запускается перед каждым стартом потока)

Параметры опциональны, поэтому простейший пул создается как

```python
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor()
```

При этом max_workers вычисляется как process-cpu-count+4, но не более 32.

Для завершения работы с пулом (что бы завершить потоки, обслуживаемые пулом) нужно вызвать метод `shutdown`.

```python
pool.shutdown()
```

Но есть возможность работы с контекстным менеджером, что является более удобным вариантом:

```python
with ThreadPoolExecutor() as pool:
    pass
```

### `map`

Пул сам по себе ничего не делает, что бы передать функции для работы, нужно воспользоваться методами пула `map` или `submit`.

Метод `ThreadPoolExecutor.map` похож на обычную функцию `map`. В качестве аргументов метод принимает функцию, которую нужно выполнять, и итерируемый объект, к элементам которого нужно применять указанную функцию.

```python
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def foo(count: int) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)

with ThreadPoolExecutor() as pool:
    pool.map(foo, [7, 5, 2])
```

Если нужно передать несколько аргументов:

```python
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def foo(count: int, flag: bool) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}, flag: {flag}")
        time.sleep(1)

with ThreadPoolExecutor() as pool:
    pool.map(foo, (7, 5, 2), (True, False, True))

```

Или

```python
params = (
    (7, True),
    (5, False),
    (2, True),
)
with ThreadPoolExecutor() as pool:
    pool.map(foo, *zip(*params))
```

Результатом вызова метода `map` является итератор, проходя по которому можно получить результат работы вызванной функции.

```python
from concurrent.futures import ThreadPoolExecutor

from scrapli import Scrapli

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def print_version(host: str) -> str:
    print(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    print(f"{host:>15}: завершено")
    return result


ids = [1, 2]
ids.extend(range(9, 19))
ip_addresses = [f"192.168.122.1{i:02}" for i in ids]


with ThreadPoolExecutor(max_workers=5) as pool:
    results = pool.map(print_version, ip_addresses)

for r in results:
    print(r)
```

### `submit`

Функция `map` применяет одну функцию к входным данным, если требуется применение различных функций, то можно написать универсальную обертку, которую использовать в `map`, а можно воспользоваться методом `submit` который запускает определенную функцию с переданными аргументами.

```python
from concurrent.futures import ThreadPoolExecutor

from scrapli import Scrapli

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def print_version(host: str) -> str:
    print(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    print(f"{host:>15}: завершено")
    return result


def print_serial(host: str) -> str:
    print(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}

    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")

    parsed_output = output.textfsm_parse_output()[0]
    serial = parsed_output.get("serial")[0]
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {serial}"
    print(f"{host:>15}: завершено")
    return result


ids = [1, 2]
ids.extend(range(9, 19))
ip_addresses = [f"192.168.122.1{i:02}" for i in ids]


results = []
with ThreadPoolExecutor(max_workers=5) as pool:
    for ip in ip_addresses:
        if int(ip.split(".")[-1]) % 2 == 0:
            results.append(pool.submit(print_version, ip))
        else:
            results.append(pool.submit(print_serial, ip))

for r in results:
    print(r.result())
```

При использовании `submit` возвращается объект класса `concurrent.futures.Future`, представляющий собой операцию, выполняемую в фоне. У объекта этого типа есть некоторые полезные атрибуты/методы:

- `cancel()` попытка отменить работу, если отмена успешно прошла, метод возвращает True
- `cancelled()` возвращает True если задача была отменена
- `running()` True если задача в данный момент выполняется (не может быть отменена)
- `done()` True если задача была успешно завершена (или отменена)
- `result()` результат выполнения задачи
- `exception()` исключение, возникшее в ходе выполнения задачи (если его не было, возвращается None)

`submit` добавляет задачу в очередь задач пула и возвращает `Future`. `Future`, в свою очередь хранят состояние задач, позволяют обращаться к результату и к исключениям. `map` это обертка над `submit`, которая уменьшает код и создает итератор для получения результатов (т.е. `map` возвращает не `Future`, а уже готовые результаты).

### `as_completed`

функция позволяет извлекать завершенные Future по мере их завершения, а не по мере их постановки в пул. Вариант можно использовать, когда порядок получения результата не важен.

Т.е. подход вида

```python
with ThreadPoolExecutor(max_workers=5) as pool:
    futures: list[Future] = [pool.submit(print_version, ip) for ip in ip_addresses]

    for f in futures:
        print(f.result())
```

Выдает результаты в том же порядке, в котором они были поставлены в очередь. А подход вида:

```python
with ThreadPoolExecutor(max_workers=5) as pool:
    futures: list[Future] = [pool.submit(print_version, ip) for ip in ip_addresses]

    for f in as_completed(futures):
        print(f.result())
```

Извлекает результаты по мере из готовности.
