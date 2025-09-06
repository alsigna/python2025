from typing import Callable, ClassVar, TypeVar

T = TypeVar("T", bound="PluginABC")


class PluginRegistry:
    REGISTRY: ClassVar[dict[str, type["PluginABC"]]] = {}

    @classmethod
    def register(cls) -> Callable[[type[T]], type[T]]:
        def wrapper(plugin: type[T]) -> type[T]:
            if not plugin.__name__.startswith("PluginABC") and plugin.__name__ not in cls.REGISTRY:
                cls.REGISTRY[plugin.__name__] = plugin
            return plugin

        return wrapper


class PluginABC:
    @classmethod
    def process(cls, config: str) -> str:
        raise NotImplementedError(f"в '{cls.__name__}' требуется реализация классового метода 'process()'")


@PluginRegistry.register()
class PluginTitle(PluginABC):
    @classmethod
    def process(cls, config: str) -> str:
        return config.title()


@PluginRegistry.register()
class PluginReverse(PluginABC):
    @classmethod
    def process(cls, config: str) -> str:
        return config[::-1]


@PluginRegistry.register()
class PluginOrderWord(PluginABC):
    @classmethod
    def process(cls, config: str) -> str:
        return " ".join(config.split()[::-1])


@PluginRegistry.register()
class PluginTitleSecond(PluginTitle): ...


if __name__ == "__main__":
    config = "some config of a device"
    for plugin in PluginRegistry.REGISTRY.values():
        print(config := plugin.process(config))
