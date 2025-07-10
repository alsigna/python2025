import logging
from typing import Any

log = logging.getLogger("my-app")
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - [%(levelname)7s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
log.addHandler(sh)


class LoggerMixIn:
    __SUCCEEDED = "\u2705"  # ✅
    __WARNING = "\u2757"  # ❗
    __ERROR = "\u274c"  # ❌
    hostname: str

    def log_debug(self, msg: str, *args: str, **kwargs: Any) -> None:
        log.debug(f"%s: {msg}", self.hostname, *args, **kwargs)

    def log_info(self, msg: str, *args: str, **kwargs: Any) -> None:
        log.info(f"%s: {msg}", self.hostname, *args, **kwargs)

    def log_warning(self, msg: str, *args: str, **kwargs: Any) -> None:
        log.warning(f"%s: {self.__WARNING} {msg}", self.hostname, *args, **kwargs)

    def log_error(self, msg: str, *args: str, **kwargs: Any) -> None:
        log.error(f"%s: {self.__ERROR} {msg}", self.hostname, *args, **kwargs)

    def log_succeeded(self, msg: str, *args: str, **kwargs: Any) -> None:
        log.info(f"%s: {self.__SUCCEEDED} {msg}", self.hostname, *args, **kwargs)
