from typing import Any, ClassVar, TypeVar, cast

T = TypeVar("T", bound="PluginABC")


class PluginRegistry(type):
    REGISTRY: ClassVar[dict[str, type["PluginABC"]]] = {}

    def __new__(mcls, name: str, bases: tuple[type, ...], attrs: dict[str, Any], **kwargs: Any) -> type[T]:
        new_class = cast(type[T], super().__new__(mcls, name, bases, attrs))
        if not name.startswith("PluginABC") and name not in mcls.REGISTRY:
            mcls.REGISTRY[name] = new_class
        return new_class


class PluginABC(metaclass=PluginRegistry):
    @classmethod
    def process(cls, config: str) -> str:
        raise NotImplementedError(f"в '{cls.__name__}' требуется реализация классового метода 'process()'")


class PluginTitle(PluginABC):
    @classmethod
    def process(cls, config: str) -> str:
        return config.title()


class PluginReverse(PluginABC):
    @classmethod
    def process(cls, config: str) -> str:
        return config[::-1]


class PluginOrderWord(PluginABC):
    @classmethod
    def process(cls, config: str) -> str:
        return " ".join(config.split()[::-1])


class PluginTitleSecond(PluginTitle): ...


if __name__ == "__main__":
    config = "some config of a device"
    for plugin in PluginRegistry.REGISTRY.values():
        print(config := plugin.process(config))
