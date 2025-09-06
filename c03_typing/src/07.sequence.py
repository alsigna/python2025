from collections.abc import Iterable, Sequence


# def squared_sum(seq: Iterable[int]) -> int:
def squared_sum(seq: Sequence[int]) -> int:
    sum_result = 0
    for i in range(len(seq)):
        sum_result += seq[i] ** 2

    return sum_result


if __name__ == "__main__":
    numbers = [1, 2, 3, 1, 2, 3]
    print(squared_sum(numbers))
    print(squared_sum(tuple(numbers)))
    # print(squared_sum(set(numbers)))
