# poetry run mypy 04.mypy/src/03.disallow-untyped-defs.py
# poetry run mypy 04.mypy/src/03.disallow-untyped-defs.py --disallow-untyped-defs


def concat(a, b):
    return a + b


def main() -> None:
    print(concat("1", "2"))


if __name__ == "__main__":
    main()
