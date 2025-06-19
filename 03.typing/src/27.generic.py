from typing import Generic, TypeVar

T = TypeVar("T")


# class MyBox[T]:
class MyBox(Generic[T]):
    def __init__(self, item: T):
        self.item = item

    def show_item(self) -> T:
        return self.item


def use_int_box(box: MyBox[int]) -> None:
    print(box.show_item())


if __name__ == "__main__":
    # int_box = MyBox[int](42)
    # str_box = MyBox[str]("user")
    int_box = MyBox(42)
    str_box = MyBox("user")
    print(f"{int_box.show_item()=}")
    print(f"{str_box.show_item()=}")
    use_int_box(int_box)
    # use_int_box(str_box)  # тут ошибка, use_int_box ожидает MyBox[int], а не MyBox[str]
    # reveal_type(int_box.show_item())
    # reveal_type(str_box.show_item())
