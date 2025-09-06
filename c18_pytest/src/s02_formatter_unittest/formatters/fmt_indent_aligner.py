from .base import FormattersRegistry


@FormattersRegistry.register()
class IndentAligner:
    @classmethod
    def format(cls, config: str) -> str:
        result = []
        section = False
        for line in config.splitlines():
            if len(line) == 0:
                continue
            if line == "#":
                section = False
                space_count = 0
            elif not line.startswith(" "):
                section = True
            if line.startswith(" ") and not section:
                if space_count == 0:
                    space_count = len(line) - len(line.lstrip())
                result.append(line.removeprefix(" " * space_count))
            else:
                result.append(line)
        return "\n".join(result)
