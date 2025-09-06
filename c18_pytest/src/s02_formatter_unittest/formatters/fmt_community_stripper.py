import re

from .base import FormattersRegistry


@FormattersRegistry.register()
class CommunityStripper:
    @classmethod
    def format(cls, config: str) -> str:
        config = re.sub(
            pattern=r"(snmp-agent community (?:read|write)) \S+",
            repl=r"\1 ****",
            string=config,
        )
        return config
