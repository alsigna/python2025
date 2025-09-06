import logging

from rich.logging import RichHandler

rich_log = logging.getLogger("my.rich.logger")
rich_log.setLevel(logging.DEBUG)
rh = RichHandler(
    markup=True,
    show_path=False,
    omit_repeated_times=True,
    rich_tracebacks=True,
)
rh.setFormatter(
    logging.Formatter(
        fmt="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ),
)
rich_log.addHandler(rh)

simple_log = logging.getLogger("my.simple.logger")
simple_log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - [%(levelname)7s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ),
)
simple_log.addHandler(sh)
