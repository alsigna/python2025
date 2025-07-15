def bad_hello(user: str, count: int) -> str:
    msg = f"hello {user}"
    for _ in range(count):
        print(msg)
    4 / 0  # noqa: B018
    return msg
