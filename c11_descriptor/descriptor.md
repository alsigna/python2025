# Дескрипторы

- [Дескрипторы](#дескрипторы)

Дескрипторы это способ управлять доступом к атрибутам объекта через методы, определённые в специальном классе. Это позволяет переопределять поведение при чтении, записи или удалении атрибутов.

Дескриптор — это класс, в котором определён хотя бы один из методов:

- `__get__(self, instance, owner)` — вызывается при чтении атрибута
- `__set__(self, instance, value)` — вызывается при установке значения атрибута
- `__delete__(self, instance)` — вызывается при удалении атрибута

Так же есть опциональный метод `__set_name__(self, owner, name)`, который позволяет управлять именем переменной, которой был присвоен дескриптор.

Аргументы в указанных методах:

- self — сам экземпляр дескриптора
- instance — объект, у которого был вызван атрибут (obj.attr) (если доступ происходит через класс, то instance == None)
- owner — класс, в котором был определён дескриптор (или его подкласс, если использовалось наследование)

Основные применения дескрипторов:

- Контроль доступа
- Валидация данных
- Ленивые вычисления
- Автоматизацию поведения при доступе к атрибутам (например логирование обращений)

Пример простого дескриптора

```python
class MinValue:
    def __get__(self, instance: "Values", owner: type) -> int:
        return min(instance.values, default=0)

class Values:
    min_value = MinValue()

    def __init__(self, values: list[int]) -> None:
        self.values = values

if __name__ == "__main__":
    v1 = Values([5, 10, -5])
    print(v1.min_value)

    v2 = Values([5, 10, -5, -100, 100])
    print(v2.min_value)
```

Дескриптор работает при использовании в качестве переменных класса и является способом предоставления хуков, позволяющих контролировать то, что происходит во время поиска атрибута (точечное обращение)

Во методах дескриптора есть аргумент `instance`, который представляет собой экземпляр класса, к атрибуту которого происходит обращение. Важно понимать, что `self` дескриптора и `instance` это ссылки на разные объекты, хранение данных в виде `self.<var-name>` может привести к их перезаписи.

```python
from typing import Any

class Integer:
    def __init__(self, name: str) -> None:
        self.name = name
        setattr(self, f"__{self.name}", 0)

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(self, f"__{self.name}")

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"значение '{self.name}' должно быть int")
        setattr(self, f"__{self.name}", value)

class Person:
    age: Integer = Integer("age")
    height: Integer = Integer("height")

    def __init__(self, age: int, height: int) -> None:
        self.age = age
        self.height = height

if __name__ == "__main__":
    p1 = Person(42, 190)
    print(f"{p1.age=}")
    print(f"{p1.height=}")

    p1.age = 40
    print(f"{p1.age=}")

    # словарь пустой
    print(f"{p1.__dict__=}")

    # значения p1 затираются
    p2 = Person(10, 150)
    print(f"{p1.age=}")
    print(f"{p2.age=}")
```

Метод `__set_name__(self, owner, name)` вызывается автоматически, когда дескриптор присваивается как атрибут в теле класса. Это удобно, чтобы не передавать имя вручную.

```python
from typing import Any

class Integer:
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> int:
        value = instance.__dict__.get(self.name)
        if not isinstance(value, int):
            raise ValueError(f"значение '{self.name}' должно быть int")
        return value

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"значение '{self.name}' должно быть int")
        instance.__dict__[self.name] = value

class Person:
    age: Integer = Integer()
    height: Integer = Integer()

    def __init__(self, age: int, height: int) -> None:
        self.age = age
        self.height = height

if __name__ == "__main__":
    p1 = Person(42, 190)
    print(f"{p1.age=}")
    print(f"{p1.height=}")

    p1.age = 40
    print(f"{p1.age=}")

    print(f"{p1.__dict__=}")
```

Внутри дескриптора нельзя использовать функции `setattr()` или `getattr()`, так как в результате эх работы вызываются setter/getter, которые определяются этим же дескриптором и получается рекурсия.

```python
class Integer:
    def __get__(self, instance: object, owner: type) -> int:
        value = instance.__dict__.get(self.name)  # Да
        value = getattr(instance, self.name)  # Нет, будет рекурсия
```

При обращении через класс значение аргумента `instance` равно `None`, по соглашению в этом случае возвращают сам дескриптор.

```python
class Integer:
    def __get__(self, instance: object | None, owner: type) -> int:
        if instance is None:
            return self

        value = instance.__dict__.get(self.name)
        # <дальнейшая реализация>
```
