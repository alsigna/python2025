class AttributeCheckerMeta(type): ...


class PluginBase(metaclass=AttributeCheckerMeta):
    required_attributes = ["name", "version"]


class Plugin(PluginBase):  # OK
    name = "MyPlugin"
    version = "1.0"


class BrokenPlugin(PluginBase):  # TypeError: В классе 'BrokenPlugin' отсутствует атрибут 'version'
    name = "MyOtherPlugin"
