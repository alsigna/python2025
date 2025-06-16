# Форматирование кода

- [Форматирование кода](#форматирование-кода)
  - [Black](#black)
    - [Описание](#описание)
    - [Настройка](#настройка)
    - [Отключение форматирования](#отключение-форматирования)
    - [IDE](#ide)
  - [Ruff](#ruff)
    - [Описание](#описание-1)
    - [Настройка](#настройка-1)
    - [Исправление ошибок](#исправление-ошибок)
    - [Отключение правил](#отключение-правил)
    - [IDE](#ide-1)
  - [Читаемости кода](#читаемости-кода)
  - [wemake-python-styleguide](#wemake-python-styleguide)
    - [Описание](#описание-2)
    - [Настройка](#настройка-2)
    - [Отключение правил](#отключение-правил-1)

## Black

### Описание

[Black](https://black.readthedocs.io/) — это инструмент для автоматического форматирования python кода. Основная концепция - строгие правила и минимум настроек. Такой подход дает единообразный и читаемый код, а так же сокращает разногласия о стиле внутри команды.

Интегрируется с IDE / CICD / Git хуками. Может читать настройки из `pyproject.toml`.

Устанавливается из PyPi: `pip install black` / `poetry add --dev black`.

Пример работы:

```bash
$ black \
  --line-length 120 \
  --check \
  --diff \
  main.py

--- main.py    2025-05-20 10:49:44.026557 +0000
+++ main.py    2025-05-20 10:50:33.282912 +0000
@@ -1,3 +1,3 @@
-def example( a :int, b:int):
+def example(a: int, b: int):
     # сумма чисел
-    return a+b
+    return a + b
would reformat main.txt

Oh no! 💥 💔 💥
1 file would be reformatted.
```

### Настройка

Концепция black - минимум свободы, поэтому настроек крайне мало, наиболее полезная - изменение максимальной длины строки. Далее запуск утилиты можно прописать в makefile и cicd.

- `pyproject.toml`

  ```toml
  [tool.black]
  line-length = 120
  ```

- makefile:

  ```makefile
  .PHONY: lint
  lint:
      poetry run black --check .
  ```

- ci-cd:

  ```yaml
  jobs:
    <job-name>:
      steps:
          ...
        - name: lint
          run: make lint
          ...
  ```

### Отключение форматирования

- `# fmt: off` / `# fmt: on` - если требуется отключить форматирование блока кода
- `# fmt: skip` - отключает форматирование одной строки, на которой инструкция расположена

```python
# fmt: off
if (
    a == 1
    and b == 2
    and c == 3
):
    print('done')
# fmt: on

print('done') # fmt: skip
```

### IDE

Для PyCharm нужно поставить пакет black и включить его использование в настройках. Для VSCode black идет в составе пакета по работе с Python. Более подробнее в [документации](https://black.readthedocs.io/en/stable/integrations/editors.html).

## Ruff

### Описание

[Ruff](https://docs.astral.sh/ruff/) - это инструмент для линтинга и форматирования python кода. Написан на rust, поэтому работает значительно быстрее аналогов (flake8, pylint).

Совместим с IDE (через плагины), CICD, Git хуками. Форматирование совместимо с black, поэтому оба инструмента могут использоваться совместно, либо black можно заменить на ruff format.

Устанавливается из PyPi: `pip install ruff` / `poetry add --dev ruff`.

- `ruff check .` - проверка кода (линтинг)
- `ruff format .` - форматирование кода

```shell
$ poetry run ruff check main.py
main.py:2:5: F841 Local variable `f` is assigned to but never used
  |
1 | def concat(a: str, b: str) -> str:
2 |     f = "test"
  |     ^ F841
3 |     return a + b
  |
  = help: Remove assignment to unused variable `f`

Found 1 error.
No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```

### Настройка

Как и в случае с black, поддерживается конфигурация в `pyproject.toml` файле. Далее запуск утилиты можно прописать в makefile и cicd.

- `pyproject.toml`

  ```toml
  [tool.ruff]
  # https://docs.astral.sh/ruff/settings
  extend-exclude = ["__init__.py"]
  line-length = 120
  lint.pydocstyle.convention = "google"
  lint.select = [
      "N",    # pep8-naming
      "B",    # flake8-bugbear
      "A",    # flake8-builtins
      "E",    # pycodestyle.error
      "W",    # pycodestyle.warning
      "F",    # pyflakes
      "S",    # flake8-bandit
      "D",    # pydocstyle
      "I",    # isort
      "C90",  # maccabe
      "C4",   # flake8-comprehensions
      "COM",  # flake8-commas
      "DTZ",  # flake8-datetimez
      "ERA",  # flake8-eradicate
      "SLOT", # flake8-slots
  ]
  lint.ignore = [
      "D100",   # Missing docstring in public module
      "D101",   # Missing docstring in public class
      "D102",   # Missing docstring in public method
      "D103",   # Missing docstring in public function
      "D105",   # Missing docstring in magic method
      "D106",   # Missing docstring in public nested class
      "D107",   # Missing docstring in `__init__`
      "S101",   # Use of `assert` detected
      "S311",   # Standard pseudo-random generators are not suitable for cryptographic purposes
      "ERA001", # Remove commented-out code
  ]
  ```

- makefile:

  ```makefile
  .PHONY: lint
  lint:
      poetry run ruff check .
  ```

- cicd:

  ```yaml
  jobs:
    <job-name>:
      steps:
          ...
        - name: lint
          run: make lint
          ...
  ```

### Исправление ошибок

Ruff может автоматически исправлять некоторые ошибки, при запуске с ключом `--fix`. В дополнение может использоваться для `--unsafe-fixes`, но такие исправления могут влиять на код.

```bash
$ ruff check main.py --unsafe-fixes --fix
Found 1 error (1 fixed, 0 remaining).
```

Можно выбирать для проверки и исправления отдельные правила, например сортировать импорты:

```bash
$ ruff check main.py --fix --select I
Found 1 error (1 fixed, 0 remaining).
```

### Отключение правил

- `# ruff: noqa` в начале файла отключает его проверку целиком
- `# ruff: noqa: F401, F841` в начале файла отключает его проверку для указанных проверок
- `# noqa` в конце строки отключает ее проверку
- `# noqa: F401, E501` отключение проверки строки для указанных правил

```python
import io  # noqa: F401
```

### IDE

Интеграция с IDE реализована в виде плагинов

- [VSCode](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [PyCharm](https://plugins.jetbrains.com/plugin/20574-ruff)

## Читаемости кода

Читаемость это важная часть разработки. Код, который легко понять и поддерживать, снижает количество ошибок и ускоряет работу. Для количественной оценки читаемости существует очень много метрик, которые можно разделить как минимум на две большие группы.

- Статические метрики
  - Цикломатическая сложность (Cyclomatic Complexity)
  - Когнитивная сложность (Cognitive Complexity)
  - Индекс удобочитаемости (Readability Index)
  - Индекс поддерживаемости (Maintainability Index)
  - Индекс сложности Джонса (Jones Complexity)
  - Глубина вложенности (Nesting Depth)
- Субъективные метрики
  - Стиль именования переменных
  - Соблюдение PEP8
  - Наличие комментариев
  - Использование анти-паттернов
  - Использование языковых идиом

Субъективные метрики невозможно оценить, некоторая часть покрывается правилами линтеров полностью или частично. Например стиль именования переменных: можно отслеживать и запретить однобуквенные имена (a, b, c), но нельзя/сложно запретить транслитерацию (zakaz вместо order). Субъективные метрики дальше не рассматриваются.

Статические метрики вычисляются с сравниваются с некими порогами.

- **Цикломатическая сложность**. количества независимых путей выполнения в кода функции. Грубо говоря, чем больше условий, тем больше веток по которым может пойти выполнение функции. Акцент на техническом пути выполнения кода.
- **Когнитивная сложность**. показывает на сколько сложно человеку воспринимать написанный код, учитывает вложенность, условия, циклы, тернарные операторы и пр. Акцент на читаемость, а не на техническом пути выполнения кода.
- **Индекс удобочитаемости**. Отражает, насколько легко воспринимать код как текст. Зачастую основан на длине строк, именах переменных, комментариях.
- **Индекс поддерживаемости**. Комплексная оценка на основе других оценок, объема кода, наличия и комментариев.
- **Индекс сложности Джонса**. Учитывает количество операторов и их уровни вложенности, показывает, насколько строка перегружена логикой.
- **Глубина вложенности**. Максимальный уровень вложенности условий/циклов (например, if внутри for внутри if).

Для оценки статистических метрик существуют различные утилиты:

| Метрика | Инструмент оценки |
| - | - |
| Цикломатическая сложность | Ruff, McCabe, radon cc, pylint, WPS |
| Когнитивная сложность | SonarQube, WPS |
| Индекс удобочитаемости | radon hal |
| Индекс поддерживаемости | radon mi, WPS |
| Индекс сложности Джонса | WPS |
| Глубина вложенности | WPS, pylint |

Ссылки:

- WPS - [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide)
- [Radon](https://github.com/rubik/radon)
- [Ruff](https://github.com/astral-sh/ruff)
- [Pylint](https://github.com/pylint-dev/pylint)
- [McCabe](https://github.com/PyCQA/mccabe)
- [SonarQube](https://www.sonarsource.com/products/sonarqube/)
- <https://habr.com/ru/companies/oleg-bunin/articles/433480/>
- <https://1c-syntax.github.io/bsl-language-server/diagnostics/CognitiveComplexity/>
- <https://sobolevn.me/2019/10/complexity-waterfall>

## wemake-python-styleguide

### Описание

Расширенный и строгий линтер для Python, поставляемый как плагин к flake8. Он добавляет большое число дополнительных проверок. Проверяет стиль кода, антипаттерны, сложность, безопасность и другие аспекты.

Устанавливается из PyPi `pip install flake8 wemake-python-styleguide`. (это плагин для flake8, поэтому кроме него нужен и сам flake8). Если установка происходит через poetry, то дополнительно нужно поставить `flake8-pyproject`, что бы flake8 смог брать настройки из pyproject файла:

```shell
poetry add flake8 flake8-pyproject
poetry add wemake-python-styleguide --python ">=3.11,<4.0"
```

### Настройка

Настройка производится с секции `[tool.flake8]`. Как и другие утилиты, запуск можно прописать в makefile и cicd.

- `pyproject.toml`

  ```toml
  [tool.flake8]
  # https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/index.html
  exclude = ["venv", ".venv", ".git", "__pycache__"]
  select = "WPS"
  ignore = [
      "WPS421", # Found wrong function call: {}
      "WPS102", # Found incorrect module name pattern
      "WPS1",   # или всю группу WPS1xx целиком
  ]
  per-file-ignores = [
      "03.output_collect.py:WPS221,WPS407", # отключаем на уровне файла
  ]
  max-jones-score = 10 # WPS200
  max-line-complexity = 10 # WPS221
  max-cognitive-score = 10 # WPS231
  allowed-domain-names = [ # некоторые проверки позволяют себя настраивать
      "value",
      "data",
      "item",
  ]
  ```

- makefile:

  ```makefile
  .PHONY: lint
  lint:
      poetry run flake8 .
  ```

- cicd:

  ```yaml
  jobs:
    <job-name>:
      steps:
          ...
        - name: lint
          run: make lint
          ...
  ```

### Отключение правил

Общий способ для `# noqa: WPS407`.
