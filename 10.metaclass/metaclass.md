# Метаклассы

- [Метаклассы](#метаклассы)
  - [Описание](#описание)
  - [`type`](#type)
  - [Создание и использование метакласса](#создание-и-использование-метакласса)
  - [Примеры использования](#примеры-использования)
    - [Регистрация классов](#регистрация-классов)
    - [Singleton](#singleton)

## Описание

Метаклассы - это классы, которые занимаются созданием классов, они позволяют вмешиваться и переопределять процесс создания.

Класс - это объект, который создает экземпляры
Метакласс - это объект, который создает классы

## `type`

Это метакласс, который по-умолчанию используется для создания классов. Python, вызывает его и передает:

- имя создаваемого класса
- список родителей классов
- словарь атрибутов класса

Т.е. определение вида:

```python
class Device:
    platform: "cisco_iosxe"

    def __init__(self, ip: str) -> None:
        self.ip = ip
        self.hostname = self._resolve_hostname(ip)

    def _resolve_hostname(self, ip: str) -> str:
        return "rt1"
```

равносильно

```python
def _resolve_hostname(self, ip: str) -> str:
    return "rt1"


def __init__(self, ip: str) -> None:
    self.ip = ip
    self.hostname = self._resolve_hostname(ip)


Device = type(
    "Device",
    (),
    {
        "platform": "cisco_iosxe",
        "__init__": __init__,
        "_resolve_hostname": _resolve_hostname,
    },
)
```

## Создание и использование метакласса

Для создания собственного метакласса нужно наследоваться от `type`.

```python
class MyMeta(type):
    def __new__(mcls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> type[Any]:
        print(f"создание класса '{name}'")
        attrs["created_by"] = "MyMeta"
        return super().__new__(mcls, name, bases, attrs)
```

После чего можно его использовать:

```python
class MyClass(metaclass=MyMeta):
    def __init__(self, value: str):
        self.value = value
```

`metaclass=MyMeta` говорит о том, что для создания будет использоваться не стандартный `type`, а его потомок `MyMeta`.

## Примеры использования

Метаклассы это сложные для понимания и отладки конструкции, их стоит применять, когда:

- нужно контролировать создание классов
- требуется автоматически модифицировать класс при его создании

В большинстве случаев лучше использовать декораторы классов или другие подходы, что бы избежать использование метаклассов.

### Регистрация классов

```python
class PluginRegistry(type):
    REGISTRY: ClassVar[dict[str, type["PluginABC"]]] = {}

    def __new__(mcls, name: str, bases: tuple[type, ...], attrs: dict[str, Any], **kwargs: Any) -> type[T]:
        new_class = cast(type[T], super().__new__(mcls, name, bases, attrs))
        if not name.startswith("PluginABC") and name not in mcls.REGISTRY:
            mcls.REGISTRY[name] = new_class
        return new_class

class PluginABC(metaclass=PluginRegistry):
    @classmethod
    def process(cls, config: str) -> str:
        raise NotImplementedError(f"в '{cls.__name__}' требуется реализация классового метода 'process()'")

class PluginTitle(PluginABC):
    @classmethod
    def process(cls, config: str) -> str:
        return config.title()
```

### Singleton

Наиболее частое применение метеклассов - реализация паттерна singleton.

```python
# Использование параметризации generic классов (`Singleton[T]`) поддерживается с py3.12
# На версиях ниже нужно дополнительно наследоваться от `Generic[T]`:
# T = TypeVar("T")
# class Singleton(type, Generic[T]):
class Singleton[T](type):
    # ключи - экземпляры метакласса Singleton[T], т.е. сами классы, созданные этим метаклассом
    # значения - экземпляры классов, созданных метаклассом
    _INSTANCES: dict["Singleton[T]", T] = {}

    # __call__ в вызывается до __new__ (а __new__ до __init__). Поэтому в __call__ можно
    # перехватить и переопределить создание объекта
    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        # если это первое создание объекта, то создаем его и заносим в словарь
        if cls not in cls._INSTANCES:
            cls._INSTANCES[cls] = super().__call__(*args, **kwargs)
        return cls._INSTANCES[cls]


class RedisDB(metaclass=Singleton): ...
```
