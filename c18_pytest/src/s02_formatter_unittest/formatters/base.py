from typing import Callable, ClassVar, Protocol, TypeVar

T = TypeVar("T", bound="FormatterABC")


class FormatterABC(Protocol):
    @classmethod
    def format(cls, config: str) -> str:
        raise NotImplementedError("требуется переопределить в классе")


class FormattersRegistry:
    REGISTRY: ClassVar[list[type["FormatterABC"]]] = []

    @classmethod
    def register(cls) -> Callable[[type[T]], type[T]]:
        def wrapper(formatter: type[T]) -> type[T]:
            if formatter not in cls.REGISTRY:
                cls.REGISTRY.append(formatter)
            return formatter

        return wrapper
