from collections.abc import Iterator
from types import TracebackType
from typing import Any, Literal, Self

from scrapli.response import MultiResponse, Response

from .rpc_method import RPCMethod as RPCMethod
from .rpc_result import RPCResult as RPCResult

class RPC:
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_password: str | None = None,
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]: ...
    def __getattr__(self, name: str) -> RPCMethod: ...
    def gather(self, *tasks: RPCResult[Any], timeout: float = 600.0) -> None: ...
    def as_completed(self, *tasks: RPCResult[Any], timeout: float = 600.0) -> Iterator[RPCResult[Any]]: ...
    def hello(
        self,
        user: str,
        count: int,
    ) -> RPCResult[str]: ...
    def send_command(
        self,
        platform: str,
        host: str,
        command: str,
        *args: Any,
        **kwargs: Any,
    ) -> RPCResult[Response]:
        """Выполняет scrapli.send_command() на удаленном сервере."""
        ...

    def send_commands(
        self,
        platform: str,
        host: str,
        commands: list[str],
        *args: Any,
        **kwargs: Any,
    ) -> RPCResult[MultiResponse]:
        """Выполняет scrapli.send_commands() на удаленном сервере."""
        ...
