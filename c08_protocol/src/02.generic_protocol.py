from typing import Generic, Protocol, TypeVar, runtime_checkable

# T = TypeVar("T", bound=int | str)


# @runtime_checkable
# class Adder(Protocol):
#     def add(self, a: int, b: int) -> int: ...


# generic protocol
# @runtime_checkable
# class Adder(Protocol[T]):
#     def add(self, a: T, b: T) -> T: ...


# py3.12
@runtime_checkable
class Adder(Protocol):
    def add[T: int | str](self, a: T, b: T) -> T: ...


class IntAdder:
    def add(self, a: int, b: int) -> int:
        return a + b


class StrAdder:
    def add(self, a: str, b: str) -> str:
        return a + b


# --------
# T = TypeVar("T")


@runtime_checkable
class MyBox[T](Protocol):
    def put(self, item: T) -> None: ...
    def get(self) -> T: ...


class IntBox:
    def put(self, item: int) -> None:
        pass

    def get(self) -> int:
        return 42


class StrBox:
    def put(self, item: str) -> None:
        pass

    def get(self) -> str:
        return "hello"


def test_int_box(box: MyBox[int]) -> int:
    return box.get() * 2


if __name__ == "__main__":
    int_adder = IntAdder()
    print(f"{isinstance(int_adder, Adder)=}")
    print(int_adder.add(1, 2))

    str_adder = StrAdder()
    print(f"{isinstance(str_adder, Adder)=}")
    print(str_adder.add("1", "2"))

    int_box = IntBox()
    print(f"{isinstance(int_box, MyBox)=}")

    str_box = StrBox()
    print(f"{isinstance(str_box, MyBox)=}")

    print(test_int_box(int_box))
    print(test_int_box(str_box))
