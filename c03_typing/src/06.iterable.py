from collections.abc import Iterable


# def squared_sum(seq: Sequence[int]) -> int:
def squared_sum(seq: Iterable[int]) -> int:
    # def squared_sum(seq: list[int] | set[int]) -> int:
    # sum_result = 0
    # for i in seq:
    #     sum_result += i**2
    # return sum_result
    return sum(i**2 for i in seq)


if __name__ == "__main__":
    numbers = [1, 2, 3, 1, 2, 3]
    print(squared_sum([]))
    print(squared_sum(numbers))
    print(squared_sum(tuple(numbers)))
    print(squared_sum(set(numbers)))
    print(squared_sum(dict.fromkeys(numbers)))
