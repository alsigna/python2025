from collections.abc import Generator
from ipaddress import IPv4Address, IPv4Network


def get_ip_addresses(net: IPv4Network) -> Generator[IPv4Address, bool, int]:
    total_ip = 0
    for ip in net.hosts():
        total_ip += 1
        continue_ = yield ip
        if not continue_:
            return total_ip
    return total_ip


def count_ip_before(net: IPv4Network, max_ip: IPv4Address) -> None:
    gen = get_ip_addresses(net)
    if max_ip not in net.hosts():
        print(f"адрес хоста '{max_ip}' не может быть в сети '{net}'")
        return

    current_ip = next(gen)
    print(current_ip)
    if current_ip == max_ip:
        print("всего: 1 хост")
        return
    continue_ = True

    while True:
        try:
            current_ip = gen.send(continue_)
        except StopIteration as e:
            print(f"всего: {e.value} хоста(ов)")
            return
        else:
            if current_ip == max_ip:
                continue_ = False
            print(current_ip)


if __name__ == "__main__":
    net = IPv4Network("192.168.0.0/24")
    ip = IPv4Address("192.168.0.100")
    count_ip_before(net, ip)
