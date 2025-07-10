# Протокол

- [Протокол](#протокол)
  - [Описание](#описание)
  - [Generic Protocol](#generic-protocol)
  - [Модификация методов](#модификация-методов)
  - [Subprotocols](#subprotocols)
  - [Наследование от обычных классов](#наследование-от-обычных-классов)

## Описание

Protocol в python - это механизм структурной типизации, который позволяет определять интерфейсы без явного наследования.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Device(Protocol):
    platform: str
    def reload(self, delay: int = 0) -> None: ...

class CiscoIOSXE:
    platform = "cisco_iosxe"

    def __init__(self, ip: str) -> None:
        self.ip = ip

    def reload(self, delay: int = 0) -> None:
        if delay == 0:
            print("отправляю команду 'reload'")
        else:
            print(f"отправляю команду 'reload in {delay}'")

device = CiscoIOSXE("192.168.0.1")
print(f"{isinstance(device, Device)=}")
device.reload(delay=30)
```

Для работы `isinstance` в runtime требуется объявлять протокол с декоратором `@runtime_checkable`

## Generic Protocol

Protocol можно комбинировать с Generic, такая комбинация позволяет создать интерфейсы с параметризованными типами.

```python
# py3.12
@runtime_checkable
class Box[T](Protocol):
    def put(self, item: T) -> None: ...
    def get(self) -> T: ...

# в более старых версиях
class Container(Protocol, Generic[T]):
    def put(self, item: T) -> None: ...
    def get(self) -> T: ...
```

## Модификация методов

При описании протокола можно применять обычные модификаторы методов (staticmethod, property и пр.)

```python
from abc import abstractmethod
from typing import ClassVar, Protocol

class Example(Protocol):
    class_attribute: ClassVar[int]
    instance_attribute: str = ""

    def method(self, arg: int) -> str: ...

    @classmethod
    def class_method(cls) -> str: ...

    @staticmethod
    def static_method(arg: int) -> str: ...

    @property
    def property_name(self) -> str: ...

    @property_name.setter
    def property_name(self, value: str) -> None: ...

    @abstractmethod
    def abstract_method(self) -> str: ...
```

## Subprotocols

Поддерживается наследование протоколов друг от друга, это позволяет составлять сложные конструкции из более простых составных частей.

```python
from typing import Protocol, runtime_checkable

class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

class ReadWritable(Readable, Writable, Protocol): ...
```

Отличия от обычного наследования:

- в родительском классе так же нужно указывать Protocol
- Protocol должен идти последнем в списке родителей

## Наследование от обычных классов

Обычный класс не может быть родителем для протокола. В этой роли могут выступать либо ABC классы, либо протоколы.
