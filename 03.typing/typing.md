# Аннотация типов

- [Аннотация типов](#аннотация-типов)
  - [Описание](#описание)
  - [Аннотация переменных](#аннотация-переменных)
    - [Списки](#списки)
    - [Кортежи](#кортежи)
    - [Словари](#словари)
  - [Аннотация функций](#аннотация-функций)
  - [Некоторые важные типы](#некоторые-важные-типы)
    - [`Literal`](#literal)
    - [`Final`, `final`](#final-final)
    - [`Iterator`, `Generator`](#iterator-generator)
    - [`Iterable`, `Sequence`](#iterable-sequence)
    - [`Callable`](#callable)
    - [`TypeAlias`, `TypeAliasType`, `type`](#typealias-typealiastype-type)
    - [`TypeVar`](#typevar)
    - [`Any`](#any)
    - [`Never`, `NoReturn`, `assert_never`, `assert_type`](#never-noreturn-assert_never-assert_type)
    - [`ParamSpec`](#paramspec)
    - [`overload`](#overload)
    - [`Generic`](#generic)
    - [`Protocol`](#protocol)
    - [`Self`](#self)
    - [`TYPE_CHECKING`](#type_checking)
    - [`type[C]`](#typec)
    - [`ClassVar`](#classvar)
    - [`NewType`](#newtype)
  - [Внешние библиотеки](#внешние-библиотеки)
    - [`py.typed`](#pytyped)
    - [Stub-файлы (`pyi`)](#stub-файлы-pyi)
    - [`types-*`](#types-)
    - [`.*-stubs`](#-stubs)
  - [StrEnum](#strenum)

## Описание

Python язык с неявной динамической строгой типизацией:

- неявная - при объявлении переменной не нужно указывать её тип
- динамическая - тип переменной определяется во время выполнения программы, в ходе работы программы можно в одну переменную складывать данные различных типов
- строгая - нельзя совершать операции над данными разных типов

Аннотация типов используется для обозначения типа для переменных и функций (как параметров, так и возвращаемых значений). Аннотация не обеспечивает проверку типов на уровне интерпретатора. Аннотация предназначена для разработчика, IDE, линтеров, статического анализа.

Для чего вводится аннотация типов:

- выявление ошибок на этапе работы с кодом, а не в runtime
- повышение читаемости и понятности кода
- помощь для IDE и разработчика

## Аннотация переменных

Для аннотации переменных используется синтаксис `<имя_переменной>: <тип>`, например:

```python
force: bool = True
delay: int = 30
devices: list = ["rt1", "rt2"]
```

Если переменная может быть нескольких типов, то это можно указать через `|` либо `Union` (из модуля typing):

```python
# delay либо integer либо NoneType
delay: int | None = 30
```

Для последовательностей можно указывать не только тип самой последовательности, но и тип элементов и/или их количество, из которых эта последовательность состоит

### Списки

Тип объектов в списке задается как `list[<objects-type>]`. Если требуется описать смешанный список, тогда можно использовать `|` для объединения нескольких типов.

```python
# список со строковыми элементами
devices: list[str] = ["rt1", "rt2"]

# список смешанных типов
params: list[int | bool] = [1, 4, True, 5]

# вложенные списки
ip_addresses: list[list[str | bool]] = [
    ["192.168.0.1", True],
    ["10.0.0.1", False],
]
```

### Кортежи

У кортежей есть два варианта аннотации:

- в кортежах с фиксированной длиной аннотируется каждый элемент.

    ```python
    person: tuple[str, int, bool] = ("Alice", 30, True)
    ```

- в кортежах с заранее неизвестной длинной, задается тип элементов + используется оператор ellipsis

    ```python
    numbers: tuple[int, ...] = (1, 2, 3)
    mixed: tuple[int | str, ...] = (4, "a", "b", 5)
    ```

> [!warning]
>
> - `list[int]` - список с элементами типа `int`
> - `tuple[int]` - кортеж только из **одного** элемента типа `int`
> - `tuple[int, ...]` - кортеж с элементами типа `int`

### Словари

При аннотировании словарей указываются типы ключей и типы значений.

```python
# dict[str, int] - ключи = str, значения = int
devices: dict[str, int] = {
    "rt1": 4,
    "rt2": 5,
}
```

Можно использовать вложенные структуры.

```python
# dict[str, dict] - ключи = str, значения = dict (со своими типами ключей/значений)
scrapli: dict[str, dict[str, str | int]] = {
    "rt1": {
        "port": 22,
        "transport": "system",
    },
}
```

## Аннотация функций

Для аннотации параметров функций используются те же правила, что и для аннотации переменных. Для аннотации возвращаемого результата используется символ `->`:

```python
def get_device_output(device: str, command: str, *, timeout: int = 30) -> str:
    return ""
```

## Некоторые важные типы

Наиболее часто используемые типы данных можно аннотировать встроенными типами (int, str, bool) как показано выше, но для более сложных случаев потребуется подключение библиотеки `typing`, в которой содержится и другие типы. Python развивается и меняется, аннотация не исключение, поэтому есть разные способы сделать одно и то же действие, например:

- до python3.9 аннотация коллекций производилась с помощью модуля `typing`, с 3.9 можно использовать стандартные коллекции (list / dict / tuple / set), которые стали дженериками [GenericAlias Type](https://docs.python.org/3/library/stdtypes.html#types-genericalias)

    ```python
    from typing import List

    # до 3.9
    routers: List[str] = ["rt1", "rt2"]
    # c 3.9
    switches: list[str] = ["sw1", "sw2"]
    ```

- до python3.10 аннотация несколькими типами производилась через тип `Union` (а для комбинации с `None` был дополнительный тип `Optional`), с 3.10 можно использовать символ `|` для объединения нескольких типов [Union Type](https://docs.python.org/3/library/stdtypes.html#types-union):

```python
from typing import Optional, Union

# до 3.10 в Union через запятую перечисляем возможные типы
delay: Union[int, None] = 30
# до 3.10 для комбинации с None вместо Union можно использовать Optional
delay: Optional[int] = 30
# с 3.10 типы можно перечислять через |
delay: int | None = 30
```

### `Literal`

Одно из перечисленных значений.

```python
def get_command_output(
    hostname: str,
    command: str,
    transport: Literal["ssh", "telnet"],
) -> str:
    return ""
```

### `Final`, `final`

`Final` говорит о том, что значение переменной нельзя менять в коде

```python
from typing import Final

MIN_LENGTH: Final[int] = 2

MIN_LENGTH += 1
```

`final` дает аналогичное поведение, только для классов/методов

```python
# наследоваться от класса A нельзя
@final
class A:
    def info(self) -> None:
        print("класс А")
```

### `Iterator`, `Generator`

- `Iterator[YieldType]` - итератор (может быть передан в `next` для получения очередного элемента)
- `Generator[YieldType, SendType, ReturnType]` - полный генератор

```python
from collections.abc import Generator, Iterator

# Iterator[int] или Generator[int] или Generator[int, None, None]
def counter(max_count: int) -> Iterator[int]:
    i = 0
    while i < max_count:
        i += 1
        yield i
```

Отличия `Iterator` и `Generator`:

| Характеристика | `Iterator[T]` | `Generator[Y, S, R]` |
| - | - | - |
| возврат промежуточных значений | `yield T` | `yield Y` |
| прием значений | Нет | через `.send(S)` |
| возврат значения в конце | Нет | `return R` |
| сложность реализации | проще | сложнее |
| применение | для простых случаев | для сложных сценариев с send/return |

### `Iterable`, `Sequence`

- `Iterable[Type]` - тип итерируемого объекта (может быть преобразован в итератор через `iter`), условно говоря: все объекты, которые могут быть перебраны циклом `for`. Практически все контейнеры (списки, кортежи, множества, словари) являются Iterable. Тип не требует, что бы объект давал доступ к элементам по индексам и поддерживал срезы.
- `Sequence[Type]` - более узкий интерфейс, объекты должны предоставлять доступ по индексам, поддерживать срезы и уметь возвращать длину (списки, кортежи, строки)

```python
from collections.abc import Iterable, Iterator, Sequence

l = [1, 3, 2]
s = set(l)

isinstance(l, Iterable)         # True, объект итерируемый (есть __iter__ интерфейс)
isinstance(l, Iterator)         # False, но еще не итератор

isinstance(iter(l), Iterable)   # True
isinstance(iter(l), Iterator)   # True

isinstance(s, Sequence)         # False, set не дает доступ по индексу
isinstance(l, Sequence)         # True, а список - дает
```

| Характеристика | `Iterable[T]` | `Sequence[T]` |
| - | - | - |
| доступ по индексу | не гарантирует | да |
| срезы | не гарантирует | да |
| определение длины | нет | да |
| упорядоченность | нет | да |
| повторное чтение | нет | да |
| память | вычисления могут быть ленивыми| хранит все элементы |
| необходимые методы | `__iter__()` | `__getitem__()`, `__len__()` |
| примеры | генераторы, множества | списки, строки |

`Sequence` это наследник `Iterable` (как и `Mapping` c `Set`, их не рассматриваем, логика в них такая же)

```text
Iterable
    ├── Sequence: list, tuple, str
    ├── Mapping: dict
    └── Set: set, frozenset
```

### `Callable`

Вызываемый объект: функция (в т.ч. и lambda), методы классов, классы с `__call__()`.

Синтаксис записи `Callable[[<типы-аргументов>], <тип-возвращаемого-значения>]`

- `Callable[[int], str]` для сигнатуры `foo(a: int) -> str`. Функция принимает int аргумент, возвращает str результат.
- `Callable[[list[str], bool], tuple[int, ...]]` для сигнатуры `foo(v: list[str], flag: bool) -> tuple[int, ...]`. Функция принимает два аргумента: первый список из строк, второй - булево значение, возвращает кортеж заранее неизвестной длины с элементами типа int.
- `Callable[..., int]` для аннотации `*args, **kwargs`. Функция принимает любые аргументы (`...`), возвращает int.

```python
from collections.abc import Callable

def process(
    funcs: list[Callable[[int, int], int]],
    numbers: tuple[int, int],
) -> None:
    for func in funcs:
        print(func(*numbers))

if __name__ == "__main__":
    process(
        funcs=[
            pow,
            lambda a, b: a + b,
            lambda a, b: a - b,
            lambda a, b: a // b,
            lambda a, b: a % b,
        ],
        numbers=(5, 2),
    )
```

### `TypeAlias`, `TypeAliasType`, `type`

Используются для задания псевдонимов типов, что делает код более читаемым:

```python
from typing import TypeAlias

Address: TypeAlias = str
a: Address = "192.168.0.1"
```

Особенно заметно на сложных типов:

```python
from typing import TypeAlias

ScrapliDict: TypeAlias = dict[str, str | bool | int | dict[str, list[str]]]

scrapli: ScrapliDict = {}

def collect_output(scrapli: ScrapliDict, command: str) -> str:
    return ""
```

- `TypeAlias` добавлен в Python3.10 и deprecated в Python3.12
- `TypeAliasType` добавлен в Python3.12 и предлагается как более функциональная замена `TypeAlias`
- `type` начиная с Python3.12 является функциональной заменой `TypeAlias`

```python
from typing import TypeAliasType

ScrapliDict = TypeAliasType("ScrapliDict", dict[str, str | bool | int | dict[str, list[str]]])

scrapli: ScrapliDict = {}
```

```python
type ScrapliDict = dict[str, str | bool | int | dict[str, list[str]]]

scrapli: ScrapliDict = {}
```

| Характеристика | `TypeAlias` | `type` | `TypeAliasType` |
| - | - | - | - |
| Python | 3.10+ (deprecated в 3.12) | 3.12+ | 3.12+ |
| Синтаксис | `MyAlias: TypeAlias = int` | `type MyAlias = int` | `MyAlias = TypeAliasType("MyAlias", int)` |
| Параметризация| нет | нет | да |
| runtime | нет | нет | да |
| Аннотация | да | да | да |

### `TypeVar`

Используется для создания тип-переменных (type variables) в Python, куда сохраняется тип переменной, а не её значение.

```python
from typing import TypeVar

# без ограничения возможных типов
T = TypeVar("T")
# или с ограничением
T = TypeVar("T", int, float)
# int и все его наследники (например bool)
T = TypeVar("T", bound=int)

def repeat(value: T, n: int) -> list[T]:
    return [value] * 2

print(repeat(1, 2))  # ОК
print(repeat("1", 2))  # ошибка, так как либо int, либо float
```

Главная задача - сохранить тип, в этом отличие от `Any`:

```python
# тип сохраняется: какой на входе, такой же на выходе
def foo(x: T) -> T: ...
# тип теряется, и тип на выходе никак не связан с типов на входе
def foo(x: Any) -> Any: ...
```

> [!note]
> `T` это сокращение от `Type` и часто используется оно, но имя может быть любым

### `Any`

Означает любой тип.

```python
from typing import Any

example: Any = "OK"
example = True
```

### `Never`, `NoReturn`, `assert_never`, `assert_type`

`Never` / `NoReturn` - противоположность `Any`, означает, отсутствие какого-либо значения.

```python
from typing import Never

def never_call(arg: Never) -> None: ...

def to_int(a: int | float) -> int:
    match a:
        case int():
            return a
        case float():
            return int(round(a, 0))
        case _:
            never_call(a)
            raise ValueError("ошибка")
```

`NoReturn` - изначально отсутствие значение было названо `NoReturn` и для возвращаемого значение это название семантически подходит, но в качестве типа аргументов вызывало путаницу, поэтому был добавлен тип `Never`, фактически означающий тоже самое.

```python
from typing import NoReturn

def log_exception(exc: Exception) -> NoReturn:
    print(f"panic!!! {exc.__class__.__name__}: {str(exc)}")
    # сохраняем логи / закрываем сессии и пр.
    raise exc
```

Для использования `Never` нужно создавать функцию-заглушку, и зачастую она имеет один и тот же вид, поэтому существует уже готовая `assert_never` функция, которую можно использовать, вместо создания собственной.

```python
from typing import assert_never

def lag_name(vendor: Vendor, intf_id: int) -> str:
    <...>
    assert_never(vendor)
```

Для проверки типа существует `assert_type`.

```python
from typing import assert_type

def hello(name: str) -> str:
    return f"hello {name}"

answer = hello("user")
assert_type(answer, int)
```

> [!warning] важно помнить, что assert_never и assert_type работают только на уровне тайпчекеров и не имеют эффекта во время исполнения кода.

### `ParamSpec`

"Parameter Specification" для сохранения типов параметров функции (*args, **kwargs), и переноса их в другие функции с сохранением типов. Основное применение - использование в декораторах.

```python
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

# до python3.12
# from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def record_calling(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"'{func.__name__}': start")
        result = func(*args, **kwargs)
        print(f"'{func.__name__}': finish")
        return result

    return wrapper
```

Для объединения какого-то известного типа с ParaSpec введен специальный тип `Concatenate`. Синтаксис использования `Callable[Concatenate[int, P], int]`

### `overload`

Это декоратор, который используется для определения различных сигнатур одной функции (разные типы и/или количество). В некоторых случаях может быть удобнее, чем `TypeVar`.

```python
from typing import TypeVar, overload

T = TypeVar("T", int, str)

@overload
def foo(a: str, b: str) -> int: ...

@overload
def foo(a: int, b: int) -> int: ...

def foo(a: T, b: T) -> int:
    if isinstance(a, int):
        return a + b
    else:
        return int(a) + int(b)
```

### `Generic`

Класс, который используется для создания generic типов. Это позволяет создавать классы, которые работают с разными типами данных, сохраняя при этом типизацию. Например нужно создать класс-контейнер (аналог list/tuple/set/...) который может хранить данные разных типов.

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class MyBox(Generic[T]):
    def __init__(self, item: T):
        self.item = item

    def get_item(self) -> T:
        return self.item

if __name__ == "__main__":
    int_box = MyBox[int](42)
    str_box = MyBox[str]("user")
```

### `Protocol`

- номинальная типизация - совместимость типов задается явно в коде. Например через наследование классов: если B наследник A, то объекты класса B могут быть использованы там, где ожидается объекты класса А.
- структурная типизация - совместимость типов определяется на основе структуры этих типов (одинаковые сигнатуры методов, атрибуты и пр).

`Protocol` является способом реализации структурной типизации в python. При этом стандартные протоколы уже использовались выше, например Iterator (доступ к методу \_\_iter\_\_), а `Protocol` позволяет определить собственные пользовательские протоколы.

```python
from typing import Protocol

class Figure(Protocol):
    name: str

    @property
    def area(self) -> int: ...

class Square:
    name = "квадрат"

    def __init__(self, side: int):
        self.side = side

    @property
    def area(self) -> int:
        return self.side**2

def show_info(f: Figure) -> None:
    print(f"фигура '{self.name}', c площадью '{self.area}'")
```

Атрибуты/методы, определенные в теле класса-протокола должны быть реализованы во всех классах, соответствующих этому протоколу. При этом есть возможность задать значения по-умолчанию, в этом случае классы должны явно наследоваться от класса-протокола. В такой реализации протокол становится похожим на `abc.ABC`.

Протокол это только для проверки тайпчекерами, и для использования в runtime нужно добавить декоратор `runtime_checkable` перед определение класса-протокола.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Figure(Protocol): ...

if isinstance(f, Figure): ...
```

### `Self`

Специальный типа, который позволяет аннотировать методы, возвращающие экземпляр своего же класса.

```python
from typing import Self


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def with_name(self, name: str) -> Self:
        self.name = name
        return self
```

`Self` пришел на смену аннотации через строковые названия ("Person") или использованию `from __future__ import annotations`

### `TYPE_CHECKING`

Специальная константа, которая в runtime всегда равна `False`, а во время статической проверки типов - `True`. Нужна в некоторых случаях, когда нужно обмануть python, или не импортировать лишние тяжелые модули, или решить проблему циклических импортов.

```python
if TYPE_CHECKING:
    from device import Device
else:
    type Device = object
```

### `type[C]`

C - некоторый класс. Тип означает, что ожидается сам класс, а не его экземпляр. Обычно используется в фабрике классов.

### `ClassVar`

Для явного обозначения классовой переменной, позволяет сделать запрет переопределения объектом класса.

```python
from typing import ClassVar

class Counter:
    count: ClassVar[int] = 0
```

### `NewType`

Позволяет создать тип-обертку над существующим типом, добавив дополнительные проверки. Новый тип учитывается только тайпчекерами, в runtime остается оригинальный тип.

```python
from ipaddress import IPv4Address
from typing import NewType

IP = NewType("IP", str)

def ip(value: str) -> IP:
    try:
        IPv4Address(value)
    except Exception as exc:
        raise ValueError(f"incorrect ip: {str(exc)}")
    else:
        return IP(value)


def connect_to_device(ip: IP) -> str: ...
```

## Внешние библиотеки

Типы для внешних библиотек могут быть получены несколькими способами:

- из исходников + файл `py.typed`
- из "types-*" пакетов проекта [typeshed](https://github.com/python/typeshed)
- из ".*-stubs" пакетов

### `py.typed`

Это специальный маркерный файл для указания того, что исходный код пакета содержит аннотации типов. Сам файл при этом пустой, для статических анализаторов/IDE важен факт его наличия, говорящий о том, что аннотация типов пакета не является внутренней и доступна для внешних систем.

### Stub-файлы (`pyi`)

Stub-файлы — это файлы с расширением `.pyi`, которые содержат только аннотации типов (без реализации кода). Они помогают тайпчекеру понимать, какие типы используются, даже даже если сам код не имеет аннотаций.

Stub-файлы могут использоваться, когда аннотацию невозможно сделать в самом коде (старые версии библиотек, C расширения, нельзя влезать в исходники), а аннотации получить нужно. Эти файлы содержат только сигнатуры с аннотациями, без конкретных реализаций.

```python
def my_sum(a: int, b: int) -> int: ...
```

Stub-файлы могут распространяться как в составе самого пакета, к которому они относятся, так и выделятся в отдельные пакеты `types-*` или `.*-stubs`.

### `types-*`

[typeshed](https://github.com/python/typeshed) это официальный репозиторий для python type stubs. В typeshed хранятся .pyi файлы для:

- встроенных модулей (os, sys, ...)
- сторонних пакетов (requests, pyyaml)
- специальных модулей (typing)

Например `types-pyyaml`, `types-requests`.

### `.*-stubs`

Когда нет возможности добавить stub-файлы в typeshed (например нужны дополнительные плагины для тайпчекеров), то stub-файлы и сопутствующий код распространяется через `.*-stubs` пакеты.

Например `django-stubs`.

## StrEnum

Вместо `Literal` зачастую можно использовать `StrEnum` как более лаконичное, надежное и удобное перечисление возможных значений. `StrEnum` появился с Python3.11, до этого нужно было комбинировать str и Enum (`class Transport(str, Enum):`).

Каждый возможный вариант, описанный через атрибут класса, наследованного от Enum, является экземпляром самого этого класса.

```python
# всегда True
isinstance(Transport.SSH, Transport)
```

Это дает возможность в аннотациях указывать сам класс, а в качестве значений передавать какой-либо из его атрибутов.

```python
class Transport(StrEnum):
    SSH = auto()
    TELNET = auto()

def get_command_output(
    hostname: str,
    command: str,
    transport: Transport,
) -> str:
    return ""

get_command_output(
        hostname="r1",
        command="show version",
        transport=Transport.SSH,
)
```

`auto()` автоматически присваивает значение на основе имени атрибута в lowercase варианте (переопределить можно через метод `_generate_next_value_`).

Преимущества `StrEnum` + `auto()`:

- автоматическое преобразование имени атрибута в строку
- можно использовать в аннотации типов
- читаемость, понятные именованные константы
- существует в одном экземпляре, поэтому сравнивается через `is` вместо `==` (что более надежно)
