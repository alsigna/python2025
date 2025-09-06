from typing import Protocol, runtime_checkable


@runtime_checkable
class Readable(Protocol):
    def read(self) -> str: ...


@runtime_checkable
class Writable(Protocol):
    def write(self, data: str) -> None: ...


@runtime_checkable
class ReadWritable(Readable, Writable, Protocol): ...


class File:
    def __init__(self, filename: str):
        self.filename = filename

    def read(self) -> str:
        with open(self.filename, "r") as f:
            data = f.read()
        return data

    def write(self, data: str) -> None:
        with open(self.filename, "w") as f:
            f.write(data)


def read_write_data(data: str, obj: ReadWritable) -> None:
    obj.write(data)
    print(obj.read())


if __name__ == "__main__":
    f = File("test.txt")
    print(f"{isinstance(f, Readable)=}")
    print(f"{isinstance(f, Writable)=}")
    print(f"{isinstance(f, ReadWritable)=}")
    read_write_data("hello", f)
