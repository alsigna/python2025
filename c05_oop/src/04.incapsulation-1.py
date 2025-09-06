class Device:
    def __init__(self) -> None:
        self._uptime = 0
        self.__hostname = "r1"

    def get_hostname(self) -> str:
        return self.__hostname


if __name__ == "__main__":
    d = Device()

    print(f"{d._uptime=}")
    d._uptime += 1
    print(f"{d._uptime=}")

    print(f"{d.get_hostname()=}")
    # print(f"{d.__hostname=}")
    print(f"{d._Device__hostname=}")
