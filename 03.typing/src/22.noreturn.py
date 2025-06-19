from typing import NoReturn


def log_exception(exc: Exception) -> NoReturn:
    print(f"panic!!! {exc.__class__.__name__}: {str(exc)}")
    # сохраняем логи / закрываем сессии и пр.
    raise exc


if __name__ == "__main__":
    try:
        div_result = 42 / 0
    except Exception as exc:
        log_exception(exc)
    else:
        print(div_result)
