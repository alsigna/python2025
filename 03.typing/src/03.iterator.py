from collections.abc import Generator, Iterator


class Counter:
    def __init__(self, max_count: int) -> None:
        self._max_count = max_count
        self._current = 0

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self._current < self._max_count:
            self._current += 1
            return self._current
        raise StopIteration


# если генератор делает только yield, то его можно аннотировать как
# Iterator[int]
# Generator[int]
# Generator[int, None, None]
def counter(max_count: int) -> Iterator[int]:
    i = 0
    while i < max_count:
        i += 1
        yield i


if __name__ == "__main__":
    print("функция-генератор:")
    for i in counter(5):
        print(i)

    print("итератор через for:")
    for i in Counter(5):
        print(i)

    print("итератор через next:")
    c = Counter(2)
    print(next(c))
    print(next(c))
    print(next(c))
