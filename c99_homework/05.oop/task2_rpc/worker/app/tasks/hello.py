def hello(user: str, count: int) -> str:
    msg = f"hello {user}"
    for _ in range(count):
        print(msg)
    # 4 / 0
    return msg
