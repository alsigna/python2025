from typing import Protocol


class RegularClass:
    def existing_method(self) -> int:
        return 0


# TypeError: Protocols can only inherit from other protocols, got <class '__main__.RegularClass'>
class ProtocolClass(RegularClass, Protocol):
    def new_method(self) -> str: ...


class Concrete:
    def existing_method(self) -> int:
        return 42

    def new_method(self) -> str:
        return "hello"


def print_info(obj: ProtocolClass) -> None:
    print(obj.existing_method(), obj.new_method())


if __name__ == "__main__":
    o = Concrete()
    print_info(o)
