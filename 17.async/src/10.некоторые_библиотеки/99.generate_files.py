import random
from datetime import datetime, timedelta


def generate_asa_log():
    log_types = [
        (
            "%ASA-4-106023",
            'Deny tcp src dmz:10.1.2.{}/{} dst outside:192.0.0.{}/{} by access-group "acl_dmz" [0x{:x}, 0x0]',
        ),
        (
            "%ASA-6-106100",
            "access-list acl_in permitted tcp inside/10.0.0.{}({}) -> outside/192.0.0.{}({}) hit-cnt 1 first hit [0x{:x}, 0x0]",
        ),
        (
            "%ASA-6-302013",
            "Built outbound TCP connection {} for outside:192.0.2.{}/{} to inside:10.1.2.{}/{}",
        ),
        (
            "%ASA-6-305011",
            "Built dynamic TCP translation from inside:192.168.{}.{}/{} to outside:192.0.0.{}/{}",
        ),
        (
            "%ASA-4-106023",
            'Deny udp src outside:192.0.2.{}/{} dst inside:10.1.2.{}/{} by access-group "acl_out" [0x{:x}, 0x0]',
        ),
    ]

    log_type, log_template = random.choice(log_types)
    timestamp = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%b %d %Y %H:%M:%S")

    ip1 = random.randint(1, 255)
    ip2 = random.randint(1, 255)
    port1 = random.randint(1024, 65535)
    port2 = random.randint(1, 65535)
    conn_id = random.randint(100000, 999999)
    hex_val = random.randint(0x10000000, 0xFFFFFFFF)

    log_msg = (
        log_template.format(ip1, port1, ip2, port2, hex_val)
        if "connection" not in log_type
        else log_template.format(conn_id, ip1, port1, ip2, port2)
    )

    return f"{timestamp}: {log_type}: {log_msg}\n"


for i in range(50):
    with open(f"./src/files/asa_logs_{i:>02}.txt", "w") as f:
        for _ in range(1000):
            f.write(generate_asa_log())

    print(f"Файл asa_logs_{i:>02}.txt успешно создан!")
