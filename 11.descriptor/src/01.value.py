class MinValue:
    def __get__(self, instance: "Values", owner: type) -> int:
        return min(instance.values, default=0)


class Values:
    min_value = MinValue()

    def __init__(self, values: list[int]) -> None:
        self.values = values


if __name__ == "__main__":
    v1 = Values([5, 10, -5])
    print(v1.min_value)

    v2 = Values([5, 10, -5, -100, 100])
    print(v2.min_value)
