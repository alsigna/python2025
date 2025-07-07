# Абстрактные классы

- [Абстрактные классы](#абстрактные-классы)
  - [Описание](#описание)
  - [Вариант создания абстрактного метода без `abc`](#вариант-создания-абстрактного-метода-без-abc)
  - [Реализация через `abc`](#реализация-через-abc)
  - [`ABC.register`](#abcregister)
  - [abstractmethod + setter/getter](#abstractmethod--settergetter)
  - [`ABCMeta`](#abcmeta)

## Описание

Абстрактные классы - это классы, которые не предназначены для создания экземпляров напрямую, а служат шаблоном для других классов. Они содержат абстрактные методы и свойства, которые либо наследуются, либо должны быть реализованы в дочерних классах. Основная целей использования абстракции – повышение гибкости, упрощение разработки и обеспечение полиморфизма, который тесно связан с абстракцией.

- выделяют существенные характеристики объекта, и игнорируя незначительные детали, оставляю их на реализацию в подклассах
- требуют от подклассов реализацию методов или свойств с заданными сигнатурами свойств
- позволяют создавать общие модели объектов, которые могут использоваться для создания конкретных объектов

Для работы с абстрактными классами и методами в Python используется модуль `abc` (Abstract Base Classes). Модуль предоставляет

- `abc.ABC` - базовый класс для создания абстрактных классов
- `abc.abstractmethod` – декоратор для создания абстрактного метода. Класс, который наследует свойства и методы от абстрактного класса, должен реализовать все абстрактные методы.

`abc.abstractmethod` можно комбинировать с

- `@classmethod` для получения абстрактного классового метода
- `@property` для получения абстрактного свойства
- `@staticmethod` для получения абстрактного статического метода

## Вариант создания абстрактного метода без `abc`

В Python существует исключение `NotImplementedError` которое обычно (в принципе можно любое использовать) используется для обозначения мест в коде, функционал которых еще не описан. Используется для защиты от вызова метода.

```python
class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_running_config(self) -> str:
        raise NotImplementedError("метод должен быть переопределен")

class CiscoIOS(Device):
    platform = "cisco_ios"

sw = CiscoIOS("192.168.1.1")
config = sw.get_running_config()

# NotImplementedError: метод должен быть переопределен
```

Такой подход заставляет реализовать метод `get_running_config` в классе наследнике. Но это потребуется только тогда, когда необходимо вызывать указанный метод, и не гарантирует того, что такой метод будет реализован всегда.

Более правильный подход - использование модуля `abc`.

## Реализация через `abc`

```python
from abc import ABC, abstractmethod


class Device(ABC):
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    @abstractmethod
    def platform(self): ...

    @abstractmethod
    def get_running_config(self) -> str: ...


class CiscoIOS(Device):
    platform = "cisco_ios"


sw = CiscoIOS("192.168.1.1")

# >>>    sw = CiscoIOS("192.168.1.1")
# >>>          ^^^^^^^^^^^^^^^^^^^^^^^
# >>> TypeError: Can't instantiate abstract class CiscoIOS without an implementation for abstract method 'get_running_config'
```

В этом случае проверка будет выполнена на этапе создания экземпляра класса наследника, и если абстрактные методы не реализованы, будет вызвано исключение. Тем самым гарантируется, что абстрактные методы будут переопределены и в каждом дочернем классе будет их своя собственная реализация, учитывающая особенности класса.

## `ABC.register`

Абстрактный класс позволяет зарегистрировать какой-либо класс в качестве виртуального подкласса без явного наследования. Это полезно, когда регистрируемый класс уже имеет нужный интерфейс, но не может или не должен наследоваться от ABC напрямую. Выполняется через декоратор, либо метод `register()`

```python
from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    @abstractmethod
    def platform(self): ...

@Device.register
class CiscoIOS:
    def __init__(self, ip: str) -> None:
        self.ip = ip

sw = CiscoIOS("192.168.1.1")
isinstance(sw, Device)  # True
```

При этом реализация абстрактных методов не проверятся и регистрируемый класс не наследует реализованные методы из ABC.

## abstractmethod + setter/getter

abstractmethod может комбинироваться с getter/setter/deleter свойств:

```python
from abc import ABC, abstractmethod

from netaddr import IPAddress

class Device(ABC):
    def __init__(self, ip: str) -> None:
        self._ip: str
        self.ip = ip

    @property
    @abstractmethod
    def ip(self) -> str: ...

    @ip.setter
    @abstractmethod
    def ip(self, ip: str) -> None: ...

class CiscoIOS(Device):
    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self._ip = ip
```

## `ABCMeta`

Модуль `abc` предоставляет два способа создания абстрактных классов:

- через наследование от `ABC` (современный и более удобный способ)
- через указание мета-класса `ABCMeta` (низкоуровневый подход)

`ABC` это просто обертка над `ABCMeta`, поэтому фактически мы получаем одно и тоже, только в коде это выглядит как наследование, без указания metaclass, что более понятно при чтении.

```python
class ABC(metaclass=ABCMeta):
    __slots__ = ()
```
