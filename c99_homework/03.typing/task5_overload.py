# есть функция parse_value:
#  - если на вход подана строка (str), возвращает float (если есть точка) иначе - int
#  - если на вход подано число (int | float), возвращает строку (str)
# нужно сделать аннотацию типов двух вариантов выше через overload. mypy --strict должен проходить без ошибок


def parse_value(value):
    if isinstance(value, str):
        return float(value) if "." in value else int(value)
    return str(value)


if __name__ == "__main__":
    assert parse_value("123") == 123
    assert parse_value("3.14") == 3.14
    assert parse_value(42) == "42"
    assert parse_value(3.14) == "3.14"
