import re

from .base import FormattersRegistry


@FormattersRegistry.register()
class JunkLineStripper:
    junk_lines = [
        r"Software Version V\S+\n",
    ]

    @classmethod
    def format(cls, config: str) -> str:
        for junk_line in cls.junk_lines:
            config = re.sub(
                pattern=junk_line,
                repl="",
                string=config,
            )
        return config
