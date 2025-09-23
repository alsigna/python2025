import sys

import pytest


@pytest.mark.skip(reason="функционал ещё не готов")
def test_feature() -> None:
    assert True


@pytest.mark.skipif(
    sys.platform != "darwin",
    reason="тест только для macos",
)
def test_macos_only() -> None:
    assert sys.platform == "darwin"


@pytest.mark.xfail(reason="баг 123")
def test_bug() -> None:
    assert 1 == 2


@pytest.mark.api()
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
    # return
    raise NotImplementedError


# затем вызываем только тесты с меткой api: pytest -m api
@pytest.mark.api()
def test_api() -> None:
    assert True
