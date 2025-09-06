from devices import HuaweiVRP

if __name__ == "__main__":
    device = HuaweiVRP("192.168.0.1")
    config = device.get_configuration()
    config = device.format_configuration(config)
    print(config)
