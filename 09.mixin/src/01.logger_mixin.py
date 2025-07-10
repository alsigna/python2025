import logging
from typing import Any

log = logging.getLogger("my-app")
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(message)s",
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


class Device(LoggerMixIn):
    def __init__(self, hostname: str):
        self.hostname = hostname

    def collect_output(self) -> None:
        result = "data"
        self.log_debug("подключаемся...")
        self.log_info("успешное подключение к устройству")
        self.log_error("ошибка сбора данных")
        self.log_succeeded("данные успешно собраны: %s", result)
        self.log_succeeded(f"данные успешно собраны: {result}")
        self.log_succeeded("данные успешно собраны: {}".format(result))
        self.log_warning("данные собраны частично")


if __name__ == "__main__":
    device = Device("r1.my.lab")
    device.collect_output()
