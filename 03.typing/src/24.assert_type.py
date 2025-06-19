from typing import Any, Awaitable, assert_type


def hello(name: str) -> str:
    return f"hello {name}"


if __name__ == "__main__":
    answer = hello("user")
    assert_type(answer, int)
    assert isinstance(answer, int)
    print(answer)
