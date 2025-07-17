# Паттерны проектирования

- [Паттерны проектирования](#паттерны-проектирования)
  - [Описание](#описание)
  - [Адаптер](#адаптер)
    - [Наследование](#наследование)
    - [Агрегация](#агрегация)
    - [Композиция](#композиция)
  - [Мост](#мост)
  - [Фасад](#фасад)
  - [Фабрика](#фабрика)
    - [Простая фабрика](#простая-фабрика)
    - [Фабричный метод](#фабричный-метод)
    - [Абстрактная фабрика](#абстрактная-фабрика)
  - [Одиночка](#одиночка)
    - [Декоратор](#декоратор)
    - [`__new__`](#__new__)
    - [Метакласс](#метакласс)
  - [Строитель](#строитель)
  - [Наблюдатель](#наблюдатель)
  - [Шаблонный метод](#шаблонный-метод)
  - [Цепочка обязанностей](#цепочка-обязанностей)

## Описание

Паттерны проектирования помогают создавать гибкий, поддерживаемый и масштабируемый код.
Паттерны разделяют на несколько видов:

- структурные: построение удобных иерархий классов в проекте
  - адаптер (adapter)
  - мост (bridge)
  - фасад (facade)
  - ...
- порождающие: отвечают за создание новых объектов
  - фабрика (factory)
  - одиночка (singleton)
  - строитель (builder)
  - ...
- поведенческие: взаимодействие объектов между собой
  - наблюдатель (observer)
  - шаблонный метод (template method)
  - цепочка обязанностей (chain of responsibility)
  - ...

## Адаптер

Обеспечивает совместную работу классов с несовместимыми интерфейсами, трансформируя методы/данные одного объекта таким образом, что бы они стали понятны другому объекту.

Адаптер применяется в основном:

- при использовании сторонних библиотек, когда их интерфейсы не соответствуют тому, что используется в проекте.
- когда нужно менять код классов нельзя, но необходимо обеспечить совместную их работу

Адаптер добавляется в проект по мере его жизни, когда требуется добавить новый функционал, перейти на другие библиотеки и пр. Т.е. это паттерн который не закладывается на этапе разработки проекта.

Адаптер можно реализовать несколькими подходами, например

- наследование
- агрегация
- композиция

### Наследование

```python
# целевой класс - предоставляет интерфейс, с которым работает клиентский код
class Target:
    def request(self) -> tuple[str, str]:
        return "192.168.0.1", "255.255.255.0"

# внешний адаптируемый класс - содержит что-то полезное, но не совместим с клиентским кодом
class External:
    def unsupported_request(self) -> IPv4Interface:
        return IPv4Interface("192.168.255.1/24")

# адаптер - делает интерфейс адаптируемого класса, совместимым с целевым
class Adapter(Target, External):
    def request(self):
        ip = self.unsupported_request()
        return str(ip.ip), str(ip.netmask)

# клиентский код
if __name__ == "__main__":
    a = Adapter()
    ip, mask = a.request()
    print(f"{ip=}")
    print(f"{mask=}")
```

### Агрегация

```python
from ipaddress import IPv4Interface

# целевой класс - предоставляет интерфейс, с которым работает клиентский код
class Target:
    def request(self) -> tuple[str, str]:
        return "192.168.0.1", "255.255.255.0"

# адаптируемый класс - содержит что-то полезное, но не совместим с клиентским кодом
class External:
    def unsupported_request(self) -> IPv4Interface:
        return IPv4Interface("192.168.255.1/24")

# адаптер - делает интерфейс адаптируемого класса, совместимым с целевым
class Adapter(Target):
    def __init__(self, external: External):
        self.external = external

    def request(self):
        ip = self.external.unsupported_request()
        return str(ip.ip), str(ip.netmask)

if __name__ == "__main__":
    a = Adapter(External())
    ip, mask = a.request()
    print(f"{ip=}")
    print(f"{mask=}")
```

### Композиция

```python
# целевой класс, предоставляет интерфейс (draw)
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self) -> None:
        print(".", end="")

# адаптируемый класс
class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

# адаптер, дающий возможность использовать адаптируемый класс и существующий интерфейс
class LineToPointAdapter:
    def __init__(self, line: Line):
        self.points = self._line_points(line.start, line.end)

    def _line_points(self, p0: Point, p1: Point) -> list[Point]:
        ...

    def __iter__(self) -> Iterator[Point]:
        return iter(self.points)


if __name__ == "__main__":
    line = Line(Point(0, 0), Point(10, 5))
    for p in LineToPointAdapter(line):
        p.draw()
```

## Мост

Паттерн, который разделяет один или несколько классов на два направления: абстракция и реализация, позволяя изменять их независимо друг от друга. В отличии от адаптера, мост закладывается на этапе проектирования системы.

```python
from abc import ABC, abstractmethod


class Device(ABC):
    @property
    @abstractmethod
    def platform(self): ...

    def __init__(self, ip: str) -> None:
        self.ip = ip

    @abstractmethod
    def get_running_config(self) -> None: ...


class CiscoIOSXE(Device):
    platform = "cisco_iosxe"

    def get_running_config(self) -> None:
        print("собираем show running-config с устройства")


class HuaweiVRP(Device):
    platform = "huawei_vrp"

    def get_running_config(self) -> None:
        print("собираем display current-configuration с устройства")


if __name__ == "__main__":
    d1 = CiscoIOSXE("192.168.1.1")
    d1.get_running_config()
    d2 = HuaweiVRP("192.168.1.2")
    d2.get_running_config()
```

## Фасад

Идея в том, что бы предоставлять легкий для понимания пользовательский интерфейс, скрывающий большой и сложный код. Фасад может не покрывать 100% функциональности, но предоставляет тот функционал, который наиболее часто требуется.

Фасад создает новый интерфейс, объединяя под собой множество систем.

```python
class NetworkDevice:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_output(self, command: str) -> str:
        print(f"собираем вывод '{command}' с устройства '{self.ip}'")
        return f"вывод команды '{command}'"

class Netbox:
    DEVICES = {
        "rt1": "192.168.1.1",
        "rt2": "192.168.2.1",
    }

    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.token = token

    def get_device(self, hostname: str) -> None:
        print(f"получаем информацию об '{hostname}' из '{self.url}'")
        return self.DEVICES[hostname]

class Redis:
    def __init__(self, url: str):
        self.url = url

    def store(self, data: dict) -> None:
        print(f"сохраняем данные в redis '{self.url}'")

class ConfigCollector:
    NETBOX_URL = "netbox.my.lab"
    NETBOX_TOKEN = "12345"
    REDIS_URL = "redis.my.lab"

    def __init__(
        self,
        hostname: str,
        netbox_url: str = "",
        netbox_token: str = "",
        redis_url: str = "",
    ):
        self.netbox = Netbox(
            url=netbox_url or self.NETBOX_URL,
            token=netbox_token or self.NETBOX_TOKEN,
        )
        self.redis = Redis(
            url=redis_url or self.REDIS_URL,
        )
        self.hostname = hostname
        self.device = NetworkDevice(
            ip=self.netbox.get_device(hostname),
        )

    def backup_config(self) -> None:
        config = self.device.get_output("show running")
        self.redis.store({self.hostname: config})

if __name__ == "__main__":
    collector = ConfigCollector("rt1")
    collector.backup_config()
```

## Фабрика

Фабрика определяет интерфейс для создания объектов, позволяющий создавать различные объекты без указания конкретных классов. В зависимости от количества создаваемых объектов, иерархии, сложности можно выделить три типа:

- простая фабрика (simple factory)
- фабричный метод (factory method)
- абстрактная фабрика (abstract factory)

### Простая фабрика

- один класс
- нет наследования
- выбор класса объекта через параметр (например через атрибут создающего метода)

```python
class Device(ABC):
    def __init__(self, ip: str):
        self.ip = ip

    @property
    @abstractmethod
    def platform(self) -> str: ...

    @property
    @abstractmethod
    def show_version_command(self) -> str: ...


class CiscoIOSXE(Device):
    platform = "cisco_iosxe"
    show_version_command = "show version"


class HuaweiVRP(Device):
    platform = "huawei_vrp"
    show_version_command = "display version"


class DeviceFactory:
    _PLATFORM_MAP: dict[str, type[Device]] = {
        "cisco_iosxe": CiscoIOSXE,
        "huawei_vrp": HuaweiVRP,
    }

    @classmethod
    def create(cls, ip: str, platform: str) -> Device:
        if platform not in cls._PLATFORM_MAP:
            raise ValueError(f"Unknown platform '{platform}'")
        return cls._PLATFORM_MAP[platform](ip)
```

### Фабричный метод

Отличается от простой фабрики тем, что фабрика представляет собой не один класс, а абстрактный класс + конкретные реализации фабрики для каждого из типов объектов. При этом в абстрактном классе существует абстрактный метод, который создает объекты, и который должен быть реализован в каждой из конкретной реализации. Так же в конкретные реализации можно добавлять какие-то атрибуты/методы для учета особенностей типа объектов.

```python
class DeviceFactory(ABC):
    @classmethod
    @abstractmethod
    def create(cls, ip: str) -> Device: ...


class CiscoFactory(DeviceFactory):
    @classmethod
    def create(cls, ip: str) -> Device:
        return CiscoIOSXE(ip)


class HuaweiFactory(DeviceFactory):
    @classmethod
    def create(cls, ip: str) -> Device:
        return HuaweiVRP(ip)
```

### Абстрактная фабрика

Отличается от фабричного метода тем, что создает не один объект, а семейство связанных объектов одного типа. Например есть:

- абстрактный класс, описывающий устройство (подключение к нему) и конкретные реализации для различных производителей
- абстрактный класс, описывающий парсер конфигурации и конкретные реализации для различных производителей

Абстрактная фабрика создает устройство и парсер одного производителя, так как они связаны друг с другом.

```python
class Factory(ABC):
    @classmethod
    @abstractmethod
    def create_device(cls, ip: str) -> Device: ...

    @classmethod
    @abstractmethod
    def create_parser(cls) -> Parser: ...

class CiscoIOSXEFactory(Factory):
    @classmethod
    def create_device(cls, ip: str) -> Device:
        ...
    @classmethod
    def create_parser(cls) -> Parser:
        ...

class HuaweiVRPFactory(Factory):
    @classmethod
    def create_device(cls, ip: str) -> Device:
        ...
    @classmethod
    def create_parser(cls) -> Parser:
        ...

def some_client_code(ip: str, factory: Factory):
    device = factory.create_device(ip)
    parser = factory.create_parser()

    output = device.send_command(device.show_version_command)
    version = parser.parse_version(output)
    print(version)
```

## Одиночка

Паттерн гарантирует, что класс имеет только один экземпляр и предоставляет точку доступа к этому экземпляру.

Очень популярный паттерн и есть несколько вариантов его реализации:

- через декоратор
- через переопределение `__new__`
- через метакласс

### Декоратор

Декоратор, который сохраняет экземпляр класса при первом его создании, затем возвращает его, вместо создания новых экземпляров.

Плюсы:

- легко применить к классу без изменения его определения
- легко встраивается в уже существующий код
- удобен, когда не нужно наследование

Минусы:

- сложно типизировать, теряется информация о классе
- трудности в наследовании

```python
from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")

def singleton(cls: type[T]) -> Callable[P, T]:
    instance: T | None = None

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        nonlocal instance  # можно через instance в виде словаря делать, тогда nonlocal не нужно
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper

@singleton
class Database:
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")
```

### `__new__`

В базовом классе переопределяется метод `__new__`.

Плюсы:

- простой и прямолинейный способ
- работает с наследованием

Минусы:

- вносит изменения в класс
- нужно явно проверять вызовы `__new__`, `__init__`

```python
class Singleton:
    _instance: T | None = None

    def __new__(cls: type[T], *args: Any, **kwargs: Any) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class Database(Singleton):
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")

class Redis(Singleton):
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")
```

> [!warning]
> при таком подходе `__init__` будет вызываться каждый раз, что может приводить к перезаписи данных и некорректной работе.

### Метакласс

Плюсы:

- применяется к классу без его модификации
- можно просто встроить в уже существующий код
- не мешает наследованию
- подходит для сложных архитектур и библиотек

Минусы:

- более сложный подход
- применение метаклассов

```python
class Singleton[T](type):
    _INSTANCES: dict["Singleton[T]", T] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in cls._INSTANCES:
            cls._INSTANCES[cls] = super().__call__(*args, **kwargs)
        return cls._INSTANCES[cls]


class Database(metaclass=Singleton):
    ...

class Redis(metaclass=Singleton):
    ...
```

## Строитель

Паттерн, который предлагает разделять создание сложных объектов на различные части, каждая из которых отвечает за определенную часть объекта. Так построение становится более наглядным, гибким и понятным.

```python
class NetboxRequestBuilder:
    def __init__(self):
        self._method = "GET"
        self._url = ""
        self._headers = {}
        self._params = {}

    def method(self, method: Literal["get", "post"] = "get") -> Self:
        self._method = method.upper()
        return self

    def url(self, url: str) -> Self:
        self._url = url
        return self

    def add_header(self, key: str, value: str) -> Self:
        self._headers[key] = value
        return self

    def add_params(self, key: str, value: str) -> Self:
        if key in self._params:
            if isinstance(self._params[key], list):
                self._params[key].append(value)
            else:
                self._params[key] = [self._params[key], value]
        else:
            self._params[key] = value
        return self

    def send(self) -> dict[str, Any]:
        response = requests.request(
            method=self._method,
            url=self._url,
            params=self._params,
            headers=self._headers,
        )
        print(response.url)
        response.raise_for_status()
        return response.json()

builder = NetboxRequestBuilder()
data = (
    builder.method("get")
    .url(NETBOX_URL)
    .add_header("Authorization", f"Token {NETBOX_TOKEN}")
    .add_header("Content-Type", "application/json")
    .add_header("Accept", "application/json")
    .add_params("manufacturer", "cisco")
    .add_params("role", "router")
    .add_params("role", "switch")
    .add_params("brief", True)
    .send()
)
```

Одним из примеров строителя является построение запросов в Django ORM. Вместо написания сырых запросов используется методы ORM для построения запросов по частям. Это упрощает чтение и поддержку кода

```python
devices = (
    Device.objects.filter(
        role__slug__in=["router", "switch"],
    )
    .exclude(
        Q(site__group__name__in=["MSK", "KLG"])
        | Q(status=DeviceStatusChoices.STATUS_PLANNED)
    )
    .exclude(tags__name="skip-this")
    .prefetch_related("site")
    .order_by("-name")
)
```

## Наблюдатель

Паттерн, который позволяет объектам (наблюдателям) подписываться на события другого объекта (субъекта) и автоматически получать уведомления о изменениях его состояния.

- subject (субъект) - за которым наблюдают
- observers (наблюдатели) - получают уведомления об изменениях

Для работы с наблюдателями в субъектах должны быть предусмотрены необходимые методы. Обычно это

- `attach()` - для добавления наблюдателя
- `detach()` - для удаления наблюдателя
- `notify()` - для оповещения

```python
# Абстрактный класс наблюдателя
class DeviceObserver(ABC):
    @abstractmethod
    def update(self, device: "Device", status: str) -> None: ...


# Конкретные реализации наблюдателей
class Logger(DeviceObserver):
    def update(self, device: "Device", status: str) -> None:
        print(f"[LOG] статус '{device.name}' поменялся на '{status}'")

# Субъект (сетевое устройство)
class Device:
    def __init__(self, name: str) -> None:
        self.name = name
        self._status = "down"
        self._observers = []

    def attach(self, observer: DeviceObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: DeviceObserver) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self, self._status)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value
        self.notify()

if __name__ == "__main__":
    router = Device("dmi01-utica-rtr01")

    logger = Logger()
    alert = Alerting()

    router.attach(logger)
    router.attach(alert)

    router.status = "up"
    router.status = "down"
```

## Шаблонный метод

Паттерн, который определяет скелет алгоритма в базовом классе, позволяя подклассам переопределять определенные шаги алгоритма без изменения его структуры.

```python
from abc import ABC, abstractmethod
from datetime import datetime

class DeviceConfigBackup(ABC):
    # Шаблонный метод - определяет каркас алгоритма
    def backup_configuration(self, ip: str) -> str:
        self.connect(ip)
        config = self.get_configuration()
        config = self.format_configuration(config)
        backup_filename = self.generate_backup_filename(ip)
        self.save_to_file(backup_filename, config)
        return backup_filename

    def connect(self, ip: str) -> None:
        print(f"подключаемся к устройству {ip} по ssh...")

    @abstractmethod
    def get_configuration(self) -> str: ...

    def format_configuration(self, config: str) -> str:
        return f"=== Конфигурация ===\n{config}\n=== EOF ==="

    def generate_backup_filename(self, ip: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{self.__class__.__name__}_{ip}_{timestamp}.txt"

    def save_to_file(self, filename: str, config: str) -> None:
        print(f"сохранение конфигурации в файл {filename}...")
        with open(filename, "w") as f:
            f.write(config)


class CiscoConfigBackup(DeviceConfigBackup):
    def get_configuration(self) -> str:
        ...

class HuaweiConfigBackup(DeviceConfigBackup):
    def get_configuration(self) -> str:
        ...
    
    def format_configuration(self, config: str) -> str:
        ...
```

## Цепочка обязанностей

Паттерн позволяет передавать данные последовательно по обработчикам. Каждый обработчик делает какую-то свою операцию (или пропускает данные без изменения).

```python
class HandlersRegistry:
    REGISTRY: ClassVar[list[type["HandlerABC"]]] = []

    @classmethod
    def add(cls) -> Callable[[type[T]], type[T]]:
        def wrapper(handler: type[T]) -> type[T]:
            if not handler.__name__.startswith("HandlerABC") and handler not in cls.REGISTRY:
                cls.REGISTRY.append(handler)
            return handler

        return wrapper


class HandlerABC(ABC):
    @classmethod
    @abstractmethod
    def format(cls, config: str) -> str: ...


@HandlersRegistry.add()
class IndentAligner(HandlerABC):
    @classmethod
    def format(cls, config: str) -> str:
        # полезный код
        return config


@HandlersRegistry.add()
class CommunityStripper(HandlerABC):
    @classmethod
    def format(cls, config: str) -> str:
        # полезный код
        return config


@HandlersRegistry.add()
class CipherStripper(HandlerABC):
    @classmethod
    def format(cls, config: str) -> str:
        # полезный код
        return config


class HuaweiVRP:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_configuration(self) -> str:
        return HUAWEI_CONFIG

    def format_configuration(self, config: str) -> str:
        # передаем данные по цепочки, каждый обработчик занимается своей частью
        for handler in HandlersRegistry.REGISTRY:
            config = handler.format(config)
        return config

    def save_config_to_file(self, config: str, filename: str) -> None:
        with open(filename, "w") as f:
            f.write(config)
```
