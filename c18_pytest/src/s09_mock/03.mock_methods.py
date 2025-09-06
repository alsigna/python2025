from unittest.mock import MagicMock

if __name__ == "__main__":
    mock = MagicMock(
        foo=MagicMock(return_value=42),
        zoo=MagicMock(side_effect=lambda x: x * 2),
    )
    print(mock.foo())
    print(mock.zoo(2))
    print(mock.zoo(3))

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
    # список всех вызовов
    print(mock.zoo.call_args_list)
    # количество вызовов
    print(mock.zoo.call_count)
    # список всех вызовов, включая вложенные
    print(mock.zoo.mock_calls)

    # сброс статистики вызовов
    mock.zoo.reset_mock()
    print(mock.zoo.call_count)
