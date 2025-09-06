from unittest.mock import MagicMock, PropertyMock

if __name__ == "__main__":
    mock = MagicMock()
    mock.__class__.some_property = PropertyMock(return_value=42)
    print(mock.some_property)
