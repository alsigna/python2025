# poetry run mypy 04.mypy/src/02.disallow-untyped-calls.py
# poetry run mypy 04.mypy/src/02.disallow-untyped-calls.py --disallow-untyped-calls


def concat(a, b):
    return a + b


def main() -> None:
    print(concat("1", "2"))


if __name__ == "__main__":
    main()
