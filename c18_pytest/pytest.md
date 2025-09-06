# Тестирование

- [Тестирование](#тестирование)
  - [Введение](#введение)
  - [Расположение тестов](#расположение-тестов)
  - [unittest](#unittest)
    - [`TestCase`](#testcase)
    - [Параметризация (`.subTest`)](#параметризация-subtest)
    - [Исключения (`.assertRaises`)](#исключения-assertraises)
    - [Предварительная настройка и уборка отдельного теста (`.setUp`, `.tearDown`)](#предварительная-настройка-и-уборка-отдельного-теста-setup-teardown)
    - [Предварительная настройка и уборка всего TestCase (`.setUpClass()`, `.tearDownClass()`)](#предварительная-настройка-и-уборка-всего-testcase-setupclass-teardownclass)
    - [async (`IsolatedAsyncioTestCase`)](#async-isolatedasynciotestcase)
    - [Stub](#stub)
    - [Mock-объекты](#mock-объекты)
      - [`MagicMock`](#magicmock)
      - [Атрибуты Mock (`.return_value`, `.side_effect`)](#атрибуты-mock-return_value-side_effect)
      - [Методы Mock](#методы-mock)
      - [PropertyMock](#propertymock)
      - [AsyncMock](#asyncmock)
      - [spec, autospec](#spec-autospec)
      - [patch](#patch)
      - [patch.object, patch.multiple](#patchobject-patchmultiple)
      - [new и PropertyMock](#new-и-propertymock)
      - [summary](#summary)
  - [Покрытие](#покрытие)
  - [PyTest](#pytest)
    - [`assert`](#assert)
    - [Группировка тестов в классы](#группировка-тестов-в-классы)
    - [conftest](#conftest)
    - [Маркировка тестов (`pytest.mark`)](#маркировка-тестов-pytestmark)
      - [Параметризация (`pytest.mark.parametrize`)](#параметризация-pytestmarkparametrize)
    - [Исключения (`pytest.raises`)](#исключения-pytestraises)
    - [Фикстуры](#фикстуры)
      - [Описание](#описание)
      - [Базовое использование](#базовое-использование)
      - [Удаление за собой](#удаление-за-собой)
      - [Автофикстуры](#автофикстуры)
      - [Композиция фикстур](#композиция-фикстур)
      - [Встроенные фикстуры](#встроенные-фикстуры)
      - [Фабрика-фикстура](#фабрика-фикстура)
      - [Scope](#scope)
        - [Зависимость фикстур (ScopeMismatch)](#зависимость-фикстур-scopemismatch)
        - [Порядок setup/teardown фикстур](#порядок-setupteardown-фикстур)
      - [Параметризация фикстур](#параметризация-фикстур)
        - [Обычная](#обычная)
        - [Косвенная](#косвенная)
      - [async](#async)
      - [conftest](#conftest-1)
    - [pytest-cov](#pytest-cov)
    - [monkeypatch](#monkeypatch)

## Введение

Тестирование — важная часть процесса разработки программного обеспечения. Позволяет проверять, насколько корректно работает код, помогает безопасно производить рефакторинг кода, так же написание тестов позволяет лучше понять уже написанный код и, возможно, сделать его улучшения.

Можно выделить несколько уровней тестирования:

- unit-тесты — тестирование отдельных модулей или функций
- интеграционные тесты — проверяют, как компоненты системы работают вместе
- end-to-end тесты - проверяют, как система взаимодействует с внешними системами

Две самые популярные библиотеки — unittest и pytest. Pytest, фактически, является стандартом написания тестов, но unittest поставляется с python, и если нет возможности ставить дополнительные пакеты, то для написания тестов может быть использован unittest.

## Расположение тестов

Обычно тесты располагают в отдельных файлах в отдельном каталоге tests (или testing) рядом к каталогом пакета:

```text
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   └── my_package
│       ├── __init__.py
│       ├── app.py
│       └── view.py
└── tests
    ├── __init__.py
    ├── test_app.py
    └── test_view.py
```

Кроме этого файлы с тестами могут располагаться рядом с файлами модуля, или же тесты могут быть написаны в том же файле, что и тестируемый код. Такой подходе не очень удобен, поэтому такие методы размещения тестов не используют.

## unittest

- поставляется с python. Как плюс - может использоваться в ограниченных или защищённых средах, когда нельзя ставить дополнительные пакеты. Минус - цикл обновления модуля очень большой
- тесты оформляются в виде методов классов, наследующихся от `unittest.TestCase`, следуя концепции ООП
- для подготовки окружения есть методы `.setUp()` / `.setUpClass()` и очистки `.tearDown()` / `.tearDownClass()`
- вместо `assert` используются поставляемые методы `.assertEqual()`, `.assertTrue()` и другие
- тесты могут группироваться в TestSuite, что помогает управлять порядком и составом тестов
- тесты могут быть запущены из командной строки, поддерживается автоматический поиск тестов
- поддержка популярными cicd (github, gitlab, jenkins, ...)

Для запуска тестов используется команда в CLI `python -m unittest`, можно добавить `-v` для verbose вывода. Или другие опции, о которых можно почитать в `python -m unittest --help`

[Документация](https://docs.python.org/3/library/unittest.html)

### `TestCase`

Все тесты реализуются как методы класса, наследника от `TestCase` и имена методов должны начинаться с `test_`.

```python
from unittest import TestCase

def concat(a: int, b: int) -> int:
    return a + b

class ConcatTestCase(TestCase):
    def test_concat(self) -> None:
        num_a = 3
        num_b = 4
        expected = num_a + num_b
        result = concat(num_a, num_b)
        self.assertEqual(expected, result)
```

### Параметризация (`.subTest`)

Когда требуется проверить код на разных входных значениях вместо использования циклов лучше использовать subTest. Такой подход рассматривает  каждое значение как независимый под-тест и не останавливает работу всего теста в случае ошибок. Так же дает понять, с какими именно входными данными тестирование не было пройдено успешно.

```python
class LoopTestCase(TestCase):
    def test_loop(self):
        for i in range(5):
            with self.subTest("Тест на четность", i=i):
                self.assertEqual(i % 2, 0)
```

Параметры, передаваемые в качестве аргументов в self.subTest() являются информационными и будут выведены в результатах. На ход самого теста влияния не имеют.

```text
test_loop (tests.utils.test_concat.LoopTestCase.test_loop) ... 
  test_loop (tests.utils.test_concat.LoopTestCase.test_loop) [Тест на четность] (i=1) ... FAIL
  test_loop (tests.utils.test_concat.LoopTestCase.test_loop) [Тест на четность] (i=3) ... FAIL
```

### Исключения (`.assertRaises`)

Если необходимо протестировать получение исключение, то необходимо использовать методы `self.assertRaises()` или `self.assertRaisesRegex()`. При использовании этих методов тест считается пройденным, если в коде возникло указанное исключение. При этом есть возможность делать более строгие проверки, например на текст исключения.

```python
class DivisionTestCase(TestCase):
    def test_division_by_zero(self):
        with self.assertRaisesRegex(
            expected_exception=(ZeroDivisionError,),
            expected_regex=r"division by \w+",
        ) as cm:
            42 / 0  # noqa: B018
            self.assertIsInstance(cm.exception, ZeroDivisionError)
            self.assertIsInstance(str(cm.exception), str)
            self.assertEqual(str(cm.exception), "division by zero")
```

### Предварительная настройка и уборка отдельного теста (`.setUp`, `.tearDown`)

Для предварительной настройки теста TestCase предоставляет пару методов `.setUp()` + `.tearDown`, которые вызываются до и после начала работы каждого из описанных тестов. Во время настройки можно подготавливать окружение и необходимые структуры, а во время очистки - удалять их. Это делается для того, что бы тесты были независимы друг от друга, и не оставляли за собой артефактов.

```python
class NetboxTestCase(TestCase):
    def setUp(self) -> None:
        test_netbox_url = os.getenv("TEST_NETBOX_URL")
        test_netbox_token = os.getenv("TEST_NETBOX_TOKEN")

        if not all((test_netbox_url, test_netbox_token)):
            raise EnvironmentError("Тестовая среда не готова")

        self.session = httpx.Client(
            transport=httpx.HTTPTransport(verify=False),
            base_url=test_netbox_url,
            headers={
                "Authorization": f"Token {test_netbox_token}",
                "Content-Type": "application/json",
                "Accept-Charset": "application/json",
                "User-Agent": "demo-python2025",
            },
        )

    def tearDown(self) -> None:
        self.session.close()
```

### Предварительная настройка и уборка всего TestCase (`.setUpClass()`, `.tearDownClass()`)

`.setUp()` и `.tearDown()` запускаются для каждого теста, но иногда нужно провести настройки один раз для всего TestCase и всех тестов в рамках него. В этом случае используются классовые методы `.setUpClass()` и `.tearDownClass()`.

```python
class RPCResultTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_redis_host = getenv("TEST_REDIS_HOST")
        test_redis_port = getenv("TEST_REDIS_PORT")
        test_redis_db = getenv("TEST_REDIS_DB", 0)
        test_redis_password = getenv("TEST_REDIS_PASSWORD")

        if not all((test_redis_host, test_redis_port)):
            raise EnvironmentError("Тестовая среда не готова")

        redis = Redis(
            host=test_redis_host,
            port=test_redis_port,
            db=test_redis_db,
            password=test_redis_password,
        )

        cls.queue = Queue(
            name="test_queue",
            connection=redis,
        )
        cls.job: Job = cls.queue.enqueue(
            f="tasks.test_func_name.test_func_name",
            args=(1, 2),
            kwargs={"a": "a", "b": "b"},
        )
        cls.instance = RPCResult(cls.job)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.job.delete()
        cls.queue.delete()
```

### async (`IsolatedAsyncioTestCase`)

Для тестирования асинхронного кода в unittest есть `IsolatedAsyncioTestCase` — наследник обычного `TestCase` (py3.8+), который предназначен  для тестирования асинхронных функций (async def). Обычный TestCase не умеет запускать async функции и при попытке использования в виде

```python
class MyTestCase(TestCase):
    async def test_foo(self) -> None:
        ...
```

будет возвращать корутину. Как альтернативное решение можно оборачивать корутину в синхронный код в виде

```python
class MyTestCase(TestCase):
    def test_foo(self):
        asyncio.run(my_async_func())
```

но это неудобно, так как нужно самостоятельно следить за циклом, который один и тот же на все вызовы, что может приводить к конфликтам. Если есть возможность - лучше использовать `IsolatedAsyncioTestCase`. Loop в для каждого теста создается свой собственный и закрывается после завершения теста, это позволяет избежать конфликтов.

IsolatedAsyncioTestCase имеет асинхронные варианты подготовки asyncSetUp/asyncTearDown, но можно использовать и синхронные варианты из TestCase, если внутри них не требуется исполнение асинхронного кода.

```python
class MyAsyncTestCase(IsolatedAsyncioTestCase):
    async def test_foo(self) -> None:
        result = await my_async_func()
        expecter_result = "abcd"
        self.assertEqual(expecter_result, result)
```

### Stub

Stub — это простейший объект-заглушка, который подменяет реальный объект и возвращает заранее прописанные данные. Главная цель — позволить тестируемому коду работать без реальных зависимостей, например походов в удаленную систему, базу данных и пр. Stub это пассивный объект, он только возвращает данные, но не проверяет как (с какими атрибутами) он был вызван.

### Mock-объекты

Интеграционные - тесты, которые используют реальные внешние системы.
Юнит - тесты, которые проверяют только работу конкретного модуля (юнита), в таких тестах ответы от внешних систем заменены на искусственные.

Такой процесс замены называется мокированием и в unittest есть специальный модуль `unittest.mock` для этого.

Это полезно, когда:

- настоящий объект дорого использовать (например, реальный API-запрос)
- он даёт нестабильные результаты (например, случайные числа или текущее время)
- он ещё не реализован (разрабатываешь "снизу вверх", интерфейс есть, реализации пока нет)

Основные понятия:

- Mock класс: базовый класс для создания mock-объекта (заглушки)
- MagicMock: наследник Mock и предоставляет дополнительные методы
- patch: контекстный менеджер/декоратор, который позволяет указывать отдельные тестируемые модули и атрибуты уровня класса для мокирования
- return_value — значение, которое мок будет возвращать
- side_effect — поведение mock-объекта при вызове (исключение, последовательность значений)

#### `MagicMock`

Почти всегда используется вместо Mock для создания mock-объекта.

```python
from unittest.mock import MagicMock

mock_obj = MagicMock()
mock_obj.some_method.return_value = 42
print(mock_obj.some_method())
```

Mock/MagicMock/другие мок классы при создании могут принимать kwargs, которые пробрасываются в атрибуты объекта. Т.е. запись:

```python
mock = MagicMock()
mock.some_method.return_value = 42
```

аналогична записи:

```python
mock = MagicMock(some_method=MagicMock(return_value=42))
```

#### Атрибуты Mock (`.return_value`, `.side_effect`)

return_value - обычное простое возвращаемое значение при вызове
side_effect - задается вместо простого return_value и позволяет гибко настраивать поведение при вызове:

- генерировать исключения
- возвращать разные значения при последовательных вызовах
- вызывать свою функцию для вычисления значения динамически

```python
# return_value
mock = MagicMock(return_value=42)
print(mock())
#>> 42
```

```python
# side_effect / exception
mock = MagicMock(side_effect=ValueError("ошибка!"))
try:
    mock()
except Exception as exc:
    print(f"Исключение - {exc.__class__.__name__}: {str(exc)}")
#>> Исключение - ValueError: ошибка!
```

```python
# side_effect / iter
mock = MagicMock(side_effect=[10, 20, 30])
while True:
    try:
        print(mock())
    except StopIteration:
        print("список кончился")
        break
#>> 10
#>> 20
#>> 30
#>> список кончился
```

```python
# side_effect / function
mock = MagicMock(side_effect=lambda x: x * 2)
print(mock(3))
#>> 6
```

Список может использоваться, например, для эмуляции разных API ответов от системы. Функция дает гибкость и динамически вычисляемые значение.

#### Методы Mock

У mock-объектов есть дополнительные методы, которые позволяют проверять, что тестируемые методы были вызваны, были вызваны с нужными атрибутами и прочее.

```python
mock = MagicMock(
    foo=MagicMock(return_value=42),
    zoo=MagicMock(side_effect=lambda x: x * 2),
)
print(mock.foo())
#>> 42
print(mock.zoo(2))
#>> 4
print(mock.zoo(3))
#>> 6

# foo был вызван хотя бы один раз
mock.foo.assert_called()

# foo был вызван ровно один раз
mock.foo.assert_called_once()

# foo был вызван с нужными аргументами (без них в случае foo)
mock.foo.assert_called_with()

# foo вызывался с аргументами (без них в случае foo) хотя бы один раз
mock.foo.assert_any_call()

# последний вызов zoo был с аргументом 3 - zoo(3)
mock.zoo.assert_called_with(3)

# хотя бы один вызов zoo был с аргументом 3
mock.zoo.assert_any_call(3)

# последний вызов
print(mock.zoo.call_args)
#>> call(3)

# список всех вызовов
print(mock.zoo.call_args_list)
#>> [call(2), call(3)]

# количество вызовов
print(mock.zoo.call_count)
#>> 2

# сброс статистики вызовов
mock.zoo.reset_mock()
print(mock.zoo.call_count)
#>> 0
```

#### PropertyMock

Используется для мокирования атрибутов (@property) объектов.

```python
from unittest.mock import MagicMock, PropertyMock

mock = MagicMock()
mock.__class__.some_property = PropertyMock(return_value=42)
print(mock.some_property)
```

#### AsyncMock

AsyncMock используется для мокирования awaitable объектов.

```python
import asyncio
from unittest.mock import AsyncMock, MagicMock

if __name__ == "__main__":
    mock = MagicMock(foo=AsyncMock(return_value=42))
    # mock.foo это awaitable объект
    print(asyncio.run(mock.foo()))
```

#### spec, autospec

Созданный мок объект по-умолчанию разрешает вызывать любые, даже несуществующие атрибуты и передавать в них любые аргументы.

```python
mock = MagicMock()
mock.existed.return_value = 42

print(mock.existed())
#>> 42
print(mock.anything())
#>> <MagicMock ...>
print(mock.not_existing_attr.foo.bar("a", "b", 1, 2))
#>> <MagicMock ...>
```

Такое поведение с большой долей вероятностью приведет к положительным тестам, даже при неверном коде, так при таком поведении mock-объект разрешает любые несуществующие методы и при опечатках, или неправильных аргументах при вызове, никак не сигнализирует об этом.

Использование `spec` задает такое поведение mock, как если бы он был экземпляром указанного класса. Т.е. mock-объект начинает повторять API указанного в `spec` класса.

- будут разрешены только те атрибуты и методы, которые есть в указанном классе
- при обращении к несуществующим атрибутам будет брошен AttributeError
- сигнатуры методов не проверяются, можно передать неправильные аргументы
- типы аргументов/возвращаемого значения не проверяются

```python
class Device:
    def get_version(self) -> str: ...

mock = MagicMock(
    spec=Device,
    get_version=MagicMock(return_value=42),
)
print(mock.get_version())
#>> 42
print(mock.anything())
#>> AttributeError
```

`autospec` расширяет `spec` тем, что дополнительно проверяет еще и сигнатуры методов.

```python
mock = create_autospec(spec=Device)
mock.get_version.return_value = 42
print(mock.get_version())
#>> 42
print(mock.get_version(1, 2, 3))
#>> TypeError
```

Обычно используется autospec как более строгий вариант.

#### patch

Mock создает искусственный mock-объект, но этого не достаточно, нужно этим объектом подменить реальный объект. Для этого используется `patch` (в различных вариациях), который подменяет реальные функции/объекты в модуле на mock-объекты. Patch может работать как контекстный менеджер или как декоратор.

```python
def patch(
    # что именно мокаем
    target: str,
    *,
    # spec и вариации - та же логика, что и у Mock, можно True
    # поставить тогда будет выбран мокируемый объект
    spec: Any | None = ...,
    spec_set: Any | None = ...,
    autospec: Any | None = ...,
    # True - создаст атрибут, даже если его нет у реального объекта
    create: bool = ...,
    # фабрика для mock-объекта, по умолчанию MagicMock
    new_callable: Any | None = ...,
    # kwargs передаются в конструктор mock-объекта
    **kwargs: Any
) -> _patch_default_new
```

Пример использования:

```python
from typing import Any
from unittest.mock import MagicMock, patch


def netbox_request() -> dict[str, Any]:
    raise RuntimeError("API недоступно")


@patch(
    # подменяем netbox_request функцию
    target="__main__.netbox_request",
    # прокидывается как return_value
    return_value={"id": 1, "name": "test"},
)
def test_api(
    key: str,
    value: int,
    # patch самостоятельно создает mock-объект и прокидывает его в функцию
    # внутри test_api netbox_request это mock, за её пределами - оригинальная функция
    mock_request: MagicMock,
) -> None:
    assert isinstance(mock_request, MagicMock)
    data = netbox_request()
    assert data[key] == value
    mock_request.assert_called_once()

if __name__ == "__main__":
    test_api("id", 1)
```

Контекстный менеджер с тем же результатом:

```python
def netbox_request() -> dict[str, Any]:
    raise RuntimeError("API недоступно")

def test_api(key: str, value: int, mock_request: MagicMock) -> None:
    assert isinstance(mock_request, MagicMock)
    data = netbox_request()
    assert data[key] == value
    mock_request.assert_called_once()

if __name__ == "__main__":
    with patch(
        target="__main__.netbox_request",
        return_value={"id": 1, "name": "test"},
    ) as mock_request:
        test_api("id", 1)
```

Или без дополнительной передачи mock_request, так как внутри контекстного менеджера netbox_request это и есть mock_request

```python
def test_api(key: str, value: int) -> None:
    data = netbox_request()
    assert data[key] == value


if __name__ == "__main__":
    with patch(
        target="__main__.netbox_request",
        return_value={"id": 1, "name": "test"},
    ):
        # тут netbox_request это mock-объекта
        test_api("id", 1)

    # а тут - реальная функция с RuntimeError
    test_api("id", 1)
```

#### patch.object, patch.multiple

patch заменяет объект целиком и используется для мокирования модуля, класса или функции. Кроме этого существуют:

- patch.object - замена атрибута конкретного экземпляра класса
- patch.multiple - замена нескольких атрибутов одновременно

```python
class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_version(self) -> str:
        # долгие вычисления
        time.sleep(2)
        return f"{self.ip}: original version"

    def parse_output(self, output) -> str:
        return f"{self.ip}: {output[::-1]}"

if __name__ == "__main__":
    device = Device("1.2.3.4")
    # тут get_version и parse_output это оригинальные функции
    device.get_version()
    device.parse_output()
    
    with patch.object(
        target=Device,
        attribute="get_version",
        return_value="mocked",
    ):
        # мокируем только get_version, parse_output остается оригинальной функцией
        device.get_version()
        device.parse_output()

    # после выхода из CM get_version становится снова оригинальной
    device.get_version()
```

Если требуется заменить несколько атрибутов, то можно применять

- вложенные контекстные менеджеры

    ```python
    with patch.object(Device, "get_version", return_value="mocked version"):
        with patch.object(Device, "parse_output", return_value="mocked output"):
            ...
    ```  

- несколько декораторов

    ```python
    @patch.object(Device, "get_version", return_value="mocked version")
    @patch.object(Device, "parse_output", return_value="mocked output")
    def test_device(mock_parse, mock_version):
        device = Device("1.2.3.4")
        ...
    ```

- patch.multiply

    ```python
    device = Device("1.2.3.4")

    def mock_parse_output(self: Device, output: str) -> str:
        return f"{self.ip}: mocked! {output[::2]}"

    with patch.multiple(
        target=Device,
        get_version=lambda self: f"{self.ip}: mocked!",
        parse_output=mock_parse_output,
    ):
        ...
    ```

Если нужно использовать mock-класс, отличный от MagicMock, то новая фабрика указывается через параметр new_callable. Например, мокирование property у объекта:

```python
from unittest.mock import MagicMock, PropertyMock, patch

class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    def version(self) -> str:
        return "1.0"

if __name__ == "__main__":
    device = Device("1.2.3.4")

    with patch.object(
        target=Device,
        attribute="version",
        spec=True,
        return_value="mocked",
        new_callable=PropertyMock,
    ):
        print(device.version)
```

#### new и PropertyMock

PropertyMock работает только для замены дескрипторов @property. Если нужно заменить обычный атрибут экземпляра класса, то у вручную создаваемого mock-объекта это делается простым назначением атрибута, а у path.object есть аргумент `new`, который используется вместо return_value для установки нового значения.

```python
device = Device("1.2.3.4")

with patch.object(
    target=device,
    attribute="ip",
    new="127.0.0.1",
):
    print(device.ip)
    #>> 127.0.0.1

print(device.ip)
#>> 1.2.3.4
```

#### summary

mock-классы

| Класс | Описание | Особенности |
| - | - | - |
| `Mock` | Универсальный подменный объект | Возвращает `Mock`, нет магических методов, самый простой класс |
| `MagicMock` | Почти всегда используется вместо `Mock` | Поддерживает `__len__`, `__iter__`, `__getitem__`, контекст-менеджеры и т.п. |
| `AsyncMock` | Для подмены `async def` | Является awaitable объектом. `mock.awaitable_foo = AsyncMock()` или `patch(..., new_callable=AsyncMock)` |
| `PropertyMock` | Для подмены `@property` | Работает только на **классе**. `mock.__class__.my_prop = PropertyMock()` или `patch.object(..., new_callable=PropertyMock)` |

Аргументы mock-класса

| Аргумент | Назначение | Пример |
| - | - | - |
| `return_value` | Возвращаемое значение | `Mock(return_value=42)` |
| `side_effect` | - исключение -> бросает<br>- функция -> вызывает<br>- список -> возвращает элементы по очереди | `Mock(side_effect=ValueError)`<br>`Mock(side_effect=lambda x: x*2)`<br>`Mock(side_effect=[1,2,3])` |
| `spec` | Ограничивает атрибуты мока<br>- списком/объектом<br>- атрибутами класса | `Mock(spec=["read", "write"])`<br>`Mock(spec=MyClass)` |
| `spec_set`| Строгий вариант `spec` | `Mock(spec_set=MyClass)` |
| `autospec` | Проверяет сигнатуру у подменных функций | `patch("foo", autospec=True)`<br>`mock=create_autospec(spec=MyClass)` |
| `wraps` | Делает «частичный мок» — реальный объект остаётся, но вызовы фиксируются | `Mock(wraps=real_obj)` |

Методы mock-класса

| Метод | Проверка |
| - | - |
| `assert_called()` | Был вызван |
| `assert_not_called()` | Не был вызван |
| `assert_called_once()` | Вызван один раз |
| `assert_called_with(*args)` | Последний вызов с аргументами |
| `assert_any_call(*args)` | Был хотя бы один вызов с аргументами |

Path

| Метод | Назначение | Пример |
| - | - | - |
| `patch` | Подменяет импортируемый атрибут | `@patch("package.module.Class")` |
| `patch.object` | Подменяет атрибут класса/объекта | `patch.object(MyClass, "some_attribute")` |
| `patch.multiple` | Подменяет несколько атрибутов разом | `patch.multiple(MyClass, attr1=Mock(), attr2=Mock())` |

## Покрытие

Когда пишутся тесты, то важно понимать, насколько полно они проверяют нашу программу. Для этого существует метрика в виде покрытия кода тестами (code coverage).

Покрытие — это процент строк кода, которые были выполнены во время запуска тестов. Если тест прошёл по строке — она считается покрытой, если ни разу не выполнилась — не покрытой.

Например для кода

```python
def divide(a: int, b: int) -> float | None:
    if b == 0:
        return None
    return a / b
```

написан тест

```python
def test_divide():
    assert divide(10, 2) == 5.0
```

который покрывает только ветку b != 0, а строка return None не была вызвана ни разу во время тестирования. Значит покрытие считается не полным.

Покрытие используется для:

- понимание охвата кода тестами: покрытие показывает, какие участки кода проверяются, а какие нет. В непокрытых участках могут быть ошибки.
- поиск "неиспользуемого кода": если участок не покрывается тестами и не удается добиться его покрытия, возможно он реализован не правильно и является лишним.
- рефакторинг: при изменении кода покрытые участки менять безопаснее, так как в случае нарушения логики тесты покажут, что что-то сломалось. Если же покрытие низкое, то внесенные во время баги или нарушения в уже работающих конструкциях внести проще.
- метрика для CI/CD: покрытие можно проверять автоматически в CI. Например можно запретить

> [!warning]
> Высокое покрытие не гарантирует отсутствие багов. Можно написать тесты, которые вызывают код, но не проверяют результат. Можно забывать о граничных значениях. Можно код подгонять под то, чтобы проходили тесты.

Покрытие — это только метрика, а не сама цель написания тестов.

Для проверки покрытия используется библиотека [coverage](https://coverage.readthedocs.io/en/latest/). Она не зависит от используемого фреймворка и работает как с unittest, так и с pytest.

```shell
poetry add --dev coverage
```

Для запуска с оценкой покрытия вместо

```text
python -m unittest <какие-то параметры запуска unittest>
```

используется

```text
coverage run -m unittest <какие-то параметры запуска unittest>
```

По-умолчанию coverage сохраняет статистику в файле `.coverage`. Которую в дальнейшем можно вывести на терминал, html, xml и другие форматы.

- `coverage report` - вывести в консоль
- `coverage html` - сгенерировать html

```text
coverage report -m --skip-covered                                
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
c18_pytest/src/s10_cov/src/divide.py       7      3    57%   3-4, 6
--------------------------------------------------------------------
TOTAL                                     14      3    79%
```

- `Stmts` — количество строк кода
- `Miss` — пропущенные строки
- `Cover` — процент покрытия
- `Missing` — номера непокрытых строк (флаг `-m` при генерации отчета)

По мере увеличения покрытия тестов свыше 75-85%, отдача от них снижается. Цифра примерная, но суть такая, что при таком уровне остаются какие-то проверки/исключения и прочий малоиспользуемый код, и вложение в покрытие этого кода значительно выше, риск того, что в этой части будет ошибка. Поэтому держать покрытие на уровне ~80% вполне нормальная практика. Но в большей мере это зависит от правил в команде/компании.

У coverage есть различные настройки запуска, генерации отчета, форматов отчетов и другие. Как и для большинства утилит, настройки удобно хранить в `pyproject.toml` файле.

> [!note]
> файл с настройками должен храниться в том же каталоге, откуда запускается coverage. `pyproject.toml` хранится в корне проекта и если запуск тестов требуется производить из другого каталога, то coverage не подхватит настройки. В этом случае можно использовать отдельный файл `.coveragerc` (который описывает только настройки coverage) и поместить его в нужный каталог.

Пример настроек

```toml
[tool.coverage.run]
command_line = "-m unittest discover -s ./c18_pytest/src/s10_cov/ -v"
branch = true

[tool.coverage.report]
skip_empty = true
omit = [
    "*/.local/*",
    # папка с тестами
    "c18_pytest/src/s10_cov/tests/*",
]
exclude_also = [
    # исключаем main секцию вместо # pragma: no cover
    'if __name__ == .__main__.:',
]
```

- command_line - позволяет прописать аргументы командной строки, с которыми будет запускаться утилита
- branch - рассматривает каждую ветку условий отдельно, точней, но медленней, чем при branch=false
- skip_empty - пропускать пустые файлы (например \_\_init\_\_.py)
- omit - пропускать определенные файлы/папки
- exclude_also - исключать описанные блоки кода

Кроме exclude_also в настройках, исключить блоки кода из покрытия можно директивой `# pragma: no cover` в самом коде, например

```python
if __name__ == "__main__":  # pragma: no cover
    ...
```

## PyTest

Отдельная библиотека python для тестирования, более гибкая и удобная, чем unittest. Преимущества pytest:

- поддержка параметризации тестов через декоратор. В unittest для этого использовались subTest.
- фикстуры (подготовка теста). В unittest только два возможных варианта: подготовка при создании класса и подготовка перед каждым тестом.
- параметризация фикстур, позволяет проверять один и тот же код с разными параметрами.
- поддержка плагинов, позволяет подстраивать тесты под требования проекта.

Для миграции с unittest на pytest не нужно вносить изменений, достаточно просто запустить `pytest`

```shell
(.venv) ➜ python -m unittest
.............................
----------------------------------------------------------------------
Ran 29 tests in 2.530s

OK

(.venv) ➜ pytest            
==================================== test session starts =====================================
platform darwin -- Python 3.13.4, pytest-8.4.1, pluggy-1.6.0
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 29 items                                                                           

tests/s01_simple_unittest/test_utils.py ..                                             [  6%]
tests/s02_formatter_unittest/test_fmt_junk_line_stripper.py .                          [ 10%]
tests/s03_subtest/test_concat.py ..                                                    [ 17%]
tests/s03_subtest/test_loop.py .                                                       [ 20%]
tests/s03_subtest/test_unrange_huawei_vlans.py .                                       [ 24%]
tests/s04_raises/test_utils.py .....                                                   [ 41%]
tests/s05_setup_teardown/test_netbox.py ..                                             [ 48%]
tests/s05_setup_teardown/test_rpc_result_auto.py .                                     [ 51%]
tests/s05_setup_teardown/test_rpc_result_manual.py .                                   [ 55%]
tests/s07_async/test_netbox_api_handler_v1.py ..                                       [ 62%]
tests/s07_async/test_netbox_api_handler_v2.py ..                                       [ 68%]
tests/s08_stub/test_netbox_api_handler.py .                                            [ 72%]
tests/s09_mock/test_device.py ..                                                       [ 79%]
tests/s09_mock/test_netbox_api_handler_v1.py ..                                        [ 86%]
tests/s09_mock/test_netbox_api_handler_v2.py ..                                        [ 93%]
tests/s10_cov/test_divide.py .                                                         [ 96%]
tests/s10_cov/test_is_even.py .                                                        [100%]

===================================== 29 passed in 2.85s =====================================
```

Есть некоторые особенности, например для pytest использование subTest является одним тестом, без параметризации. Как и для unittest, в pytest существует множество параметров запуска, передаваемых через аргументы командной строки, или файлы настроек. Например, запустить все тесты с шаблоном имени `netbox`:

```shell
(.venv) ➜ pytest -k netbox
=================================== test session starts ===================================
platform darwin -- Python 3.13.4, pytest-8.4.1, pluggy-1.6.0
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 32 items / 21 deselected / 11 selected                                          

tests/s05_setup_teardown/test_netbox.py ..                                          [ 18%]
tests/s07_async/test_netbox_api_handler_v1.py ..                                    [ 36%]
tests/s07_async/test_netbox_api_handler_v2.py ..                                    [ 54%]
tests/s08_stub/test_netbox_api_handler.py .                                         [ 63%]
tests/s09_mock/test_netbox_api_handler_v1.py ..                                     [ 81%]
tests/s09_mock/test_netbox_api_handler_v2.py ..                                     [100%]

============================ 11 passed, 21 deselected in 2.84s ============================
```

> [!note]
> PyTest модульный фреймворк, и для того, что бы он имел возможность подтягивать .env файл, нужно установить pytest-dotenv

### `assert`

Простейший тест на pytest это обычная функция, имя которой начинается с test, которая содержит оператор assert.

```python
def test_concat_int() -> None:
    num_a = randint(1, 10)
    num_b = randint(1, 10)
    expected = num_a + num_b
    result = concat(num_a, num_b)
    
    assert result == expected
```

### Группировка тестов в классы

Тесты могут существовать и в виде отдельных функций, но так как они должны быть атомарными, т.е. проверять какую-то одну характеристику, то число таких отдельных функций может быть достаточно большое. Для удобства можно группировать тесты в классы, как было в unittest (только без наследования). Имя класса должно начинаться с `Test`, а самих тестов с `test` (тут без изменения). В класс можно добавлять служебные методы, их pytest будет игнорировать (если имя не начинается с test).

### conftest

conftest.py — это специальный файл конфигурации pytest, который позволяет:

- хранить фикстуры, доступные во всех тестах проекта
- подключать общие настройки, логирование, обработку результатов, запуск кода перед/после тестов, автозагрузка .env

> Фикстуры (fixtures) — это специальные функции, которые подготавливают окружение для теста: создают данные, подключения к базе, запускают сервера (например redis), очищают файлы и т.п.

Основной плюс использования conftest в том, что его не нужно импортировать, pytest сам найдет conftest и использует его.

conftest.py файлов может быть несколько в разных каталогах, область видимости каждого из conftest - текущий каталог и ниже по дереву.

### Маркировка тестов (`pytest.mark`)

В pytest существует возможность устанавливать метки на тесты, с помощью меток можно:

- помечать специальный тесты (например slow, db, ...) и запускать только нужные группы (pytest -m ...)
- управлять выполнением теста (пропуск, ожидаемое падение)
- отмечать тесты, как параметризованные

Виды меток:

- Стандартные (уже есть в pytest):
  - `pytest.mark.skip` / `pytest.mark.skipif` — пропустить тест
  - `pytest.mark.xfail` — ожидаем падения тесты
  - `pytest.mark.parametrize` — запуск теста с разными входными данными
- Пользовательские, придумываем самостоятельно, например `pytest.mark.api`, `pytest.mark.slow`, ...
- Метки из плагинов. Некоторые плагины ([pytest-django](https://pytest-django.readthedocs.io/), [pytest-flask](https://pytest-flask.readthedocs.io/), [pytest-asyncio](https://pytest-asyncio.readthedocs.io/), ...) добавляют свои метки, например `pytest.mark.django_db`, `pytest.mark.asyncio`

Например:

```python
import sys
import pytest

@pytest.mark.skip(reason="функционал ещё не готова")
def test_feature() -> None:
    ...

@pytest.mark.skipif(
    sys.platform != "darwin",
    reason="тест только для macos",
)
def test_macos_only() -> None:
    ...

@pytest.mark.xfail(
    sys.platform == "darwin",  # условие
    reason="еще не реализовано",  # текст в отчете для причины падения
    raises=NotImplementedError,  # ожидаемый exception (можно tuple, если большое одного исключения)
    run=True,  # не запускать тест вообще
    strict=True,  # если тест пройдет, считать это успехом или нет
)
def test_exception() -> None:
    # ожидали NotImplementedError, а случился ZeroDivisionError - тест провален
    # 1 / 0
    raise NotImplementedError

# затем вызываем только тесты с меткой api: pytest -m api
@pytest.mark.api()
def test_api() -> None:
    ...
```

При использовании своих меток pytest выдает warning вида `PytestUnknownMarkWarning: Unknown pytest.mark.api`. Что бы этого не происходило кастомные метки нужно перечислить в настройках:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "api: тесты api",
    "slow: медленные тесты",
    "redis: тесты с запущенным редисом",
]
```

Посмотреть все доступные метки можно командой

```text
pytest --markers
```

Маркировать можно не только функции, но и классы и целые модули.

```python
# все тесты в модуле помечаются меткой redis
pytestmark = pytest.mark.redis()

# все тесты в классе помечаются меткой redis
@pytest.mark.redis()
class TestRPCResult: ...
```

#### Параметризация (`pytest.mark.parametrize`)

Декоратор `pytest.mark.parametrize` позволяет задать множество наборов данных, с которыми запуститься тест. Более простой и гибкий инструмент, чем subTest в unittest.

```python
@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (1, 2, 3),
        (2, 2, 4),
    ],
)
def test_sum(x: int, y: int, expected: int) -> None:
    assert x + y == expected
```

Каждый набор параметров рассматривается как отдельный тест, и если нужно сделать маркировку этого отдельного теста, то она передается через pytest.param

```python
@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (1, 2, 3),
        pytest.param(2, 2, 5, marks=pytest.mark.xfail(reason="баг 123")),
    ],
)
```

Декораторы можно стекировать. Будет 4 теста: (1, 10), (2, 10), (1, 20), (2, 20):

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_mul(x, y) -> None:
    assert x * y > 0
```

давать имена входным данным:

```python
@pytest.mark.parametrize(
    argnames=("x", "expected"),
    argvalues=[(1, 2), (3, 4)],
    ids=["one", "two"],
)
def test_inc_v1(x: int, expected: int) -> None:
    assert x + 1 == expected
```

или через pytest.param:

```python
@pytest.mark.parametrize(
    argnames=("x", "expected"),
    argvalues=[
        pytest.param(1, 2, id="one"),
        pytest.param(3, 4, id="two"),
    ],
)
def test_inc_v2(x: int, expected: int) -> None:
    assert x + 1 == expected
```

### Исключения (`pytest.raises`)

По аналогии с unittest и `TestCase.assertRaisesRegex` в pytest так есть возможность сказать, что в коде мы ожидаем исключение.

```python
import pytest


def test_division_by_zero() -> None:
    with pytest.raises(
        expected_exception=(ZeroDivisionError,),
        match=r"division by \w+",
    ) as cm:
        42 / 0  # noqa: B018
    assert isinstance(cm.value, ZeroDivisionError)
    assert isinstance(str(cm.value), str)
    assert str(cm.value) == "division by zero"
```

- исключение выброшено — тест проходит
- исключение не выброшено — тест падает
- выброшено другое исключение — тест падает
- выброшено исключение с описанием, не подходящим под match (str или re.Pattern) - тест падает

Как и в unittest пойманное исключение можно дальше обрабатывать и проверять его параметры.

### Фикстуры

#### Описание

Фикстура это специальные функции, которые подготавливают окружение для теста: создают данные, подключения к базе, запускают сервера (например redis), очищают файлы и т.п. В unittest аналогом фикстур являются `.setUp`/`.tearDown` и `.setUpClass()`/`.tearDownClass()`.

Для того, что бы превратить функцию в фикстуру применяется декоратор `@pytest.fixture`, в который, по необходимости, можно передать опциональные настройки фикстуры.

Ключевые свойства:

- внедрение по имени (dependency injection)
- управляемое время жизни ресурса (scope)
- поддержка teardown через yield
- возможность параметризации
- композиция (фикстуры могут зависеть от других фикстур)

Зачем:

- повторное использование кода: фикстуру объявляем один раз, а используем сколько угодно в разных тестах
- упрощение настройки: помогают автоматически настраивать необходимые ресурсы перед тестами и очищать их после
- улучшение читаемости: код тестов становится сфокусированным на самих тестах, а не на логики подготовки/очистки окружения

Список доступных фикстур, в том числе встроенных и из установленных модулей, доступен по ключу `--fixtures`

```text
pytest --fixtures
```

#### Базовое использование

Базовый пример: в тестах pytest увидит аргумент и вызовет одноимённую фикстуру, а её результат её выполнения передаст в тест.

```python
import pytest


@pytest.fixture()
def sample() -> list[int]:
    return [1, 2, 3]


def test_sum(sample: list[int]) -> None:
    assert sum(sample) == 6


def test_max(sample: list[int]) -> None:
    assert max(sample) == 3
```

#### Удаление за собой

Для того, что бы фикстура убрала за собой (tearDown), используется конструкция `yield` вместо `return`:

```python
@pytest.fixture()
def session() -> Iterator[httpx.Client]:
    # подготавливаем ресурс
    client = httpx.Client(...)
    # через yield отдаем ресурс тесты
    yield client
    # после возвращения управления (тест закончился), убираем за собой 
    client.close()
```

#### Автофикстуры

отмечаются с флагом `autouse=True` и подгружаются во все тесты без необходимости указания как аргумент.

```python
@pytest.fixture(autouse=True)
def set_up_logging() -> None:
    # настроить логирование перед каждым тестом
    ...

def test_api() -> None:
    ...
```

#### Композиция фикстур

Фикстуры можно использовать в других фикстурах, как зависимости.

```python
    @pytest.fixture(name="redis")
    def _redis_client(self) -> Redis:
        return Redis(...)

    # в фикстуре _create_job "redis" это фикстура _redis_client
    @pytest.fixture(autouse=True)
    def _create_job(self, redis: Redis) -> Iterator[None]:
        queue = Queue(..., connection=redis)
        self.job = queue.enqueue(...)

        yield

        job.delete()
        queue.delete()
```

#### Встроенные фикстуры

В pytest уже некоторые встроенный фикстуры, например

- [tmp_path](https://docs.pytest.org/en/latest/how-to/tmp_path.html) - временный каталок (Pathlib объект), и еще ряд связанных фикстур
- [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) - подмена env/атрибутов/импортов

#### Фабрика-фикстура

Фикстура может возвращать и callable объект, реализуя паттерн фабрики. Внутри теста появляется возможность гибко создавать объекты.

```python
@dataclass
class User:
    name: str
    role: str

@pytest.fixture
def user_factory() -> Callable[..., User]:
    def create_user(**kwargs: str) -> User:
        data = {"name": "John", "role": "user", **kwargs}
        return User(**data)

    return create_user

def test_custom_user(user_factory: Callable[..., User]) -> None:
    admin = user_factory(role="admin")
    assert admin.name == "John"
    assert admin.role == "admin"
```

#### Scope

Scope определяет, как долго живёт объект, и как часто он пересоздаётся. Правильный выбор scope помогает балансировать между скоростью тестов (меньше повторных запусков фикстур) и изоляцией (что бы у каждого теста ресурсы были созданы с нуля).

Фикстура создаётся при первом запросе в рамках своей области видимости (scope) и кешируется до конца этой области. Затем при завершении области выполняется teardown фикстуры (если есть yield).

Возможные значения:

- `function` — по умолчанию, для каждого теста фикстура создается заново
- `class` — один раз для каждого тестового класса. Т.е. все методы в пределах одного класса используют один и тот же созданный фикстурой объект)
- `module` — один раз на модуль. Все тесты в одном файле (он же модуль) используют один и тот же объект
- `package` — один раз на пакет (директория с \_\_init\_\_.py)
- `session` — один раз за весь запуск тестов (одна сессия pytest)

##### Зависимость фикстур (ScopeMismatch)

Фикстуры могут зависеть от других фикстур. При этом нужно соблюдать правило: фикстура не может зависеть от фикстуры с более узким (меньшим) scope. То есть:

- function зависит от session (узкая зависит от более широкой) - OK
- session зависит от function (широкая зависит от узкой) - ScopeMismatch

##### Порядок setup/teardown фикстур

- pytest самостоятельно строит граф зависимостей фикстур и создает фикстуры согласно этому графу
- завершение фикстур происходит в обратном порядке (LIFO)
- фикстуры с более широким скоупом завершаются позже, чем фикстуры с более узким скоупом

#### Параметризация фикстур

##### Обычная

Параметризация позволяет запускать тесты с разными вариантами ресурса. Поведение похоже на pytest.mark.parametrize, но на уровне фикстуры.

```python
@pytest.fixture(params=["admin", "user", "guest"])
def role(request: pytest.FixtureRequest) -> str:
    return request.param


def test_role_access(role: str) -> None:
    if role == "admin":
        assert True
    elif role == "user":
        assert True
    else:
        assert role == "guest"
```

##### Косвенная

При параметризации теста в декораторе `@pytest.mark.parametrize` есть ключевое слово `indirect`, говорящее о том, что параметры нужно передавать не напрямую в тест, а в фикстуру с таким же именем. В тест же попадет результат выполнения фикстуры.

Есть два варианта использования:

- `indirect=True` - все параметры считаются фикстурами
- `indirect=["var1", "var2"]` - только перечисленные параметры фикстуры, остальные попадают в тест напрямую

По сравнению с обычной параметризацией фикстуры, косвенная удобнее тем, что позволяет использовать разные параметра для разных тестов, вместо одного статического набора параметров, определенных при создании фикстуры.

#### async

Плагин `pytest-asyncio` добавляет поддержку асинхронных фикстур и тестов (существуют и другие, но рассматриваем pytest-asyncio). После его установки можно писать `async def test_XXX` тесты, и pytest сможет их запускать. Для запуска такой тест должен быть маркирован декоратором `@pytest.mark.asyncio()`:

```python
class TestNetboxAPIHandler:
    NETBOX_VERSION = "4.3.7"

    @pytest.fixture()
    def session(self) -> Iterator[httpx.Client]:
        test_netbox_url = getenv("TEST_NETBOX_URL")
        test_netbox_token = getenv("TEST_NETBOX_TOKEN")
        return NetboxAPIHandler(test_netbox_url, test_netbox_token)

    def test_get(self, session: httpx.Client) -> None:
        with session:
            response = session.get("/api/status/")

        assert isinstance(response, list)
        assert len(response) == 1
        version = response[0].get("netbox-version")
        assert version == self.NETBOX_VERSION

    @pytest.mark.asyncio()
    async def test_aget(self, session: httpx.Client) -> None:
        async with session:
            response = await session.aget("/api/status/")

        assert isinstance(response, list)
        assert len(response) == 1
        version = response[0].get("netbox-version")
        assert version == self.NETBOX_VERSION
```

Либо в настройках должна быть выставлена опция:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

В настройках декоратора `@pytest.mark.asyncio()` можно задать аргумент `loop_scope` одним из возможных значений (
по аналогии с параметром `scope`):

- `function`
- `class`
- `module`
- `package`
- `session`

`loop_scope` отвечает за то, для какой области будет действовать создаваемый цикл события. Это будет отдельный цикл событий на каждый тест (`function`), один на класс (`class`) или один на всю тестовую сессию (`session`)

#### conftest

Фикстуры, которые нужны во многих тестах можно вынести в conftest.py файл, импортировать их при этом не нужно, pytest самостоятельно их найдет. Как и с другими объектами в conftest.

### pytest-cov

Запуск тестов с покрытием можно производить через `coverage run -m pytest`, как это производится в случае с unittest. Но удобнее использовать плагин [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/). После установки

```text
poetry add --dev pytest-cov
```

Можно запускать pytest с coverage флагами, например

```text
pytest --cov=./ --cov-report=html --cov-report=term
```

- `--cov=./` - что проверяем на покрытие
- `--cov-report=html --cov-report=term` - отчет в html форме и в терминале

### monkeypatch

[monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) это встроенная фикстура pytest, которая позволяет временно (в тесте) подменять:

- атрибуты объектов и классов (`monkeypatch.setattr`)
- элементы словарей (`.setitem` / `.delitem`)
- переменные окружения (`.setenv` / `.delenv`)
- системные пути импорта (`.syspath_prepend`)

monkeypatch похожа на Mock из unittest, но:

- написана в pytest-стиле: подключается как dependency injection и сама убирает за собой после окончания теста
- более простая и легче в использовании
- не обладает дополнительными методами, например assert_called_with и подобными, что бы проверять, как был вызван метод

monkeypatch используется в простых подменах, в сложных случаях (например нужно контролировать как были вызваны методы) используется Mock.

<https://pytest-docs-ru.readthedocs.io/ru/latest/>
[text](https://docs.pytest.org/en/stable/reference/reference.html#ini-options-ref)
<https://docs.pytest.org/en/latest/>
