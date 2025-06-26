# MyPy

- [MyPy](#mypy)
  - [Тайпчекеры](#тайпчекеры)
  - [Описание](#описание)
  - [`reveal_locals`, `reveal_type`](#reveal_locals-reveal_type)
  - [`ignore`](#ignore)
  - [Pydantic](#pydantic)

## Тайпчекеры

Это инструменты для проверки типов в Python, которые анализирует код и выявляют ошибки, связанные с несоответствием типов.
[Awesome Python Typing](https://github.com/typeddjango/awesome-python-typing) страничка с популярными тайпчекерами.

- static type checkers (статические тайпчекеры) - выполняются до запуска программы
- dynamic type checkers (runtime, динамические тайпчекеры) - выполняются во время работы программы

## Описание

[MyPy](https://mypy.readthedocs.io/en/stable/) - инструмент статического анализа типов, который помогает находить ошибки в коде до его выполнения. Основывается на аннотации типов (type hints).

Основные характеристики:

- проверяет типы во время разработки
- совместим [PEP 484](https://peps.python.org/pep-0484/) (модуль typing)
- поддерживает постепенную типизацию
- поддерживает внешние плагины
- может интегрироваться с IDE
- поддерживает generics, перегрузку функций и другие возможности системы типов

Настройки mypy, как и других утилит, можно хранить в конфигурационных файлах: mypy.ini, .mypy.ini, setup.cfg. Но удобнее это делать в `pyproject.toml`.

Пример `pyproject.toml`:

```toml
[tool.mypy]
plugins = ["pydantic.mypy"]
strict = false
disallow_untyped_calls = true
disallow_untyped_defs = true
warn_return_any = true
warn_unreachable = true
```

- plugins: список подключенных плагинов
- strict: alias для включения ряда проверок: --disallow-untyped-calls, --disallow-untyped-defs, ...
- disallow-untyped-calls: запрет аннотируемым функциям вызывать неаннотированные
- disallow-untyped-defs: запрет определения функций без аннотаций
- warn-return-any: запрет Any аннотаций для возвращаемых значений

## `reveal_locals`, `reveal_type`

Полезные функции, которые помогают понять типы переменных во время проверки mypy. Используются только при отладке, в runtime вызывают ошибку.

```python
type Response = dict[str, str]

def foo(a: Response, b: int) -> str:
    reveal_locals()
    reveal_type(a)
    return a["value"][::-1] * b
```

```bash
(.venv)$ mypy reveal_type_locals.py 
reveal_type_locals.py:9: note: Revealed local types are:
reveal_type_locals.py:9: note:     a: builtins.dict[builtins.str, builtins.str]
reveal_type_locals.py:9: note:     b: builtins.int
reveal_type_locals.py:10: note: Revealed type is "builtins.dict[builtins.str, builtins.str]"
Success: no issues found in 1 source file
```

## `ignore`

Если требуется отключить проверку для определенной строки, то к ней добавляется комментарий вида

```python
def arista_eos_get_running_config(hostname): ...  # type: ignore[no-untyped-def]
```

`type: ignore [no-untyped-def]` говорит анализатору типов (например, mypy) игнорировать ошибку no-untyped-def (функция без аннотаций типов) в этой строке.

Когда может понадобиться:

- при работе с метаклассами, где сигнатуры методов могут быть сложными для типизации
- в legacy коде
- для временного отключения проверки в сложных местах

Возможны различные варианты использования:

- отключить несколько проверок, они указываются через запятую `type: ignore[no-untyped-def, misc, arg-type]`
- отключить какие-то проверки целиком в настройках

```toml
[tool.mypy]
disable_error_code = ["no-untyped-def", "misc", "no-untyped-def"]
```

## Pydantic

Pydantic предоставляет функционал автоматического приведения типов, а так же требует, что бы атрибуты модели были явно типизированы. В mypy эти аспекты трактуются иначе.

```python
class Model(BaseModel):
    list_of_int: list[int]

Model(list_of_int=[1, "2", b"3"])
```

С точки зрения python и pydantic является корректным кодом, так как pydantic автоматически приведет типы, но с точки зрения mypy это ошибка, так как ожидается список int. Что бы интегрировать mypy и pydantic существует plugin `pydantic.mypy`, входящий в состав mypy (дополнительно ставить не нужно), который необходимо активировать в настройках.

```toml
[tool.mypy]
plugins = ["pydantic.mypy"]
```
