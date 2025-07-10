from abc import abstractmethod
from typing import ClassVar, Protocol, runtime_checkable


@runtime_checkable
class Example(Protocol):
    class_attribute: ClassVar[int]
    instance_attribute: str = ""

    def method(self, arg: int) -> str: ...

    @classmethod
    def class_method(cls) -> str: ...

    @staticmethod
    def static_method(arg: int) -> str: ...

    @property
    def property_name(self) -> str: ...

    @property_name.setter
    def property_name(self, value: str) -> None: ...

    @abstractmethod
    def abstract_method(self) -> str: ...
