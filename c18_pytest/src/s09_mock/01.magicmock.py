from unittest.mock import MagicMock

if __name__ == "__main__":
    mock = MagicMock()
    mock.some_method.return_value = 42
    print(mock.some_method())

    mock = MagicMock(some_method=MagicMock(return_value=42))
    print(mock.some_method())
