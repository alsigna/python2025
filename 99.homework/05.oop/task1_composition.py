# при использовании композиции в примере ниже создаются циклические ссылки вида
# Device -> BGP -> Device. Это делает невозможным удаление объектов после того
# как количество ссылок на объект станет равным нулю (такое событие просто не
# наступит из-за циклических ссылок). Такие объекты удаляются циклическим сборщиком
# мусора, который запускается с некой периодичностью и ищет подобные ситуации,
# разрывает зацикливание и удаляет объекты. Нужно сделать рефакторинг кода, что бы:
#  - логика сохранилась (Device/BGP остались и BGP был частью Device)
#  - при завершении функции demo() объекты удалялись: в __del__ добавлены print функции,
#     и их вывод должен быть ДО финального `= работа кода закончена =`, а не после,
#     как сейчас
#  - поможет решить задачу модуль weakref и WeakSet из него

from typing import Self


class Device:
    def __init__(self, ip: str, asn: str) -> None:
        self.ip = ip
        self.asn = asn
        self.bgp = BGP(self)

    def add_peer(self, peer: Self) -> None:
        self.bgp.add_peering(peer)

    def __str__(self) -> str:
        return f"Device({self.ip}, {self.asn})"

    def __repr__(self) -> str:
        return str(self)

    def __del__(self) -> None:
        print(f"<< удаление объекта {self} >>")


class BGP:
    def __init__(self, device: Device) -> None:
        self._ip = device.ip
        self.device = device
        self.peers: set[Device] = set()

    def add_peering(self, peer: Device) -> None:
        if peer is self.device:
            return
        self.peers.add(peer)
        peer.bgp.peers.add(self.device)  # noqa: SLF001

    def __str__(self) -> str:
        return f"BGP объект для Device({self._ip})"

    def __del__(self) -> None:
        print(f"<< удаление объекта {self} >>")


def demo() -> None:
    pe1 = Device("192.168.0.1", "64512")
    pe2 = Device("192.168.0.2", "64512")
    pe3 = Device("192.168.0.3", "64512")
    rr1 = Device("192.168.0.255", "64512")
    pe1.add_peer(rr1)
    pe1.add_peer(pe3)
    pe2.add_peer(rr1)
    pe3.add_peer(rr1)
    print(pe1.bgp.peers)
    print(pe2.bgp.peers)
    print(pe3.bgp.peers)
    print(rr1.bgp.peers)


if __name__ == "__main__":
    demo()
    print("= работа кода закончена =")
