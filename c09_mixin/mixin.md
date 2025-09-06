# MixIn

- [MixIn](#mixin)
  - [Описание](#описание)
  - [`LoggerMixIn`](#loggermixin)
  - [MixIn с зависимостями](#mixin-с-зависимостями)
  - [`__init__` и `super()`](#__init__-и-super)
  - [Рекомендации](#рекомендации)

## Описание

MixIn - это специальный вид класса, предназначенный для предоставления дополнительной функциональности другим классам через наследование. MixIn классы не предназначены для самостоятельного использования и от них нельзя создать экземпляры, а служат для "подмешивания" методов и атрибутов к другим классам.

Основные характеристики MixIn:

- Не предназначены для создания экземпляров
- Обычно не имеют собственных атрибутов атрибутов и `__init__` метода
- Обычно Предоставляют дополнительные методы
- Используются через множественное наследование

MixIn обычно используются:

- когда нужно повторно использовать код между несколькими классами, но наследование логически не подходит
- когда вы хотите добавить функциональность к существующим классам без изменения их кода

> [!note]
> в python нет отдельного типа для MixIn классов, поэтому с точки зрения кода это обычные классы. Что бы отличать их, к именам классов обычно дописывают `MixIn`

Распространенные примеры использования:

- добавление методов сериализации
- логирование
- авторизация и аутентификация

## `LoggerMixIn`

Пример MixIn класса, добавляющего методы логирования.

```python
class LoggerMixIn:
    __SUCCEEDED = "\u2705"  # ✅
    __WARNING = "\u2757"  # ❗
    __ERROR = "\u274c"  # ❌
    hostname: str

    def log_debug(self, msg: str, *args: str, **kwargs: str) -> None:
        log.debug(f"%s: {msg}", self.hostname, *args, **kwargs)

    def log_info(self, msg: str, *args: str, **kwargs: str) -> None:
        log.info(f"%s: {msg}", self.hostname, *args, **kwargs)

    def log_warning(self, msg: str, *args: str, **kwargs: str) -> None:
        log.warning(f"%s: {self.__WARNING} {msg}", self.hostname, *args, **kwargs)

    def log_error(self, msg: str, *args: str, **kwargs: str) -> None:
        log.error(f"%s: {self.__ERROR} {msg}", self.hostname, *args, **kwargs)

    def log_succeeded(self, msg: str, *args: str, **kwargs) -> None:
        log.info(f"%s: {self.__SUCCEEDED} {msg}", self.hostname, *args, **kwargs)
```

## MixIn с зависимостями

Если mixin класс использует методы наследника, то эти зависимости желательно проверять в коде mixin'a:

```python
class SaveLoadMixIn:
    def save(self, filename: str) -> None:
        method_name = "_serialize"
        method = getattr(self, method_name, None)
        if method is None:
            raise AttributeError(f"класс должен иметь метод {method_name}()")

        data: str = method()
        with open(filename, "w") as f:
            f.write(data)
```

## `__init__` и `super()`

Если в mixin необходимо объявить `__init__` метод, то необходимо правильно выстраивать цепочку наследования:

- MRO работает слева направо
- вызов super() необходим в каждом классе цепочки

```python
class LoggingMixin:
    def __init__(self, *args, **kwargs):
        print("инициализация LoggingMixin")
        super().__init__(*args, **kwargs)

    def log(self, msg: str) -> None:
        print(msg)


class TaggingMixin:
    def __init__(self, *args, tag: str = "", **kwargs):
        print("инициализация TaggingMixin")
        self.tag = tag
        super().__init__(*args, **kwargs)


class Device(TaggingMixin, LoggingMixin):
    def __init__(self, ip: str, platform: str, *args, **kwargs):
        print("инициализация Device")
        self.ip = ip
        self.platform = platform
        super().__init__(*args, **kwargs)
```

## Рекомендации

- явная проверка требований, нужно фиксировать (документировать) и проверять, что должен реализовать класс для работы с mixin
- mixin это максимально независимый класс, реализующий какую-то одну функцию, которая часто требуется в коде
- при множественном наследовании важно помнить про mro, super() и порядок наследования
- нужно следить за именами методов/атрибутов, что бы при наследовании они не переопределялись
- иногда композиция лучше наследования
