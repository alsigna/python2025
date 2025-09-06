from unittest.mock import MagicMock

if __name__ == "__main__":
    # return_value
    mock = MagicMock(return_value=42)
    print(mock())

    # side_effect / exception
    # mock = MagicMock()
    # mock.side_effect = ValueError("ошибка!")
    # или
    mock = MagicMock(side_effect=ValueError("ошибка!"))
    try:
        mock()
    except Exception as exc:
        print(f"Исключение - {exc.__class__.__name__}: {str(exc)}")

    # side_effect / iter
    mock = MagicMock(side_effect=[10, 20, 30])
    while True:
        try:
            print(mock())
        except StopIteration:
            print("список кончился")
            break

    # side_effect / function
    mock = MagicMock(side_effect=lambda x: x * 2)
    print(mock(3))
