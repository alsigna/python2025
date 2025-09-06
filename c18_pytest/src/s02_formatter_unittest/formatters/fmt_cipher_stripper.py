import re

from .base import FormattersRegistry


@FormattersRegistry.register()
class CipherStripper:
    @classmethod
    def format(cls, config: str) -> str:
        config = re.sub(
            pattern=r"(irreversible-cipher) \S+",
            repl=r"\1 ****",
            string=config,
        )
        return config
