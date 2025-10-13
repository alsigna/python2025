"""команда для генерации.

python -m grpc_tools.protoc \
  --proto_path=./proto \
  --python_out=./app/pb \
  --grpc_python_out=./app/pb \
  --mypy_out=./app/pb \
  ./proto/*
"""

#
# message
#
from pb import message_pb2

address = message_pb2.Address()
address.city = "msk"
address.street = "unknown"
user = message_pb2.User(name="john", age=30, address=address)

print(user)

#
# enum
#
from pb import enum_pb2

print(enum_pb2.Status.STATUS_FAIL)
# >> 2
print(enum_pb2.Status.STATUS_OK)
# >> 1


#
# oneof
#
from pb import oneof_pb2

event = oneof_pb2.Event()

event.text = "hello"
print(f"{event.text!r}")
print(f"{event.code!r}")
print(f"{event.WhichOneof("payload")!r}")

event.code = 404
print(f"{event.text!r}")
print(f"{event.code!r}")
print(f"{event.WhichOneof("payload")!r}")

#
# map
#
from pb import map_pb2

platform = map_pb2.Platform()
platform.scrapli["cisco"] = "cisco_iosxe"
print(platform)

platform.scrapli["huawei"] = "huawei_vrp"
print(platform)

platform.scrapli.get("huawei")
platform.scrapli.pop("huawei")
platform.scrapli.clear()
platform.scrapli.items()
platform.scrapli.values()
platform.scrapli.keys()

#
# repeated
#
from pb import repeated_pb2

devices = repeated_pb2.Devices(site="msk")
print(devices.ip)
devices.ip.append("1.2.3.4")
devices.ip.append("4.3.2.1")
devices.ip.extend(["1.1.1.", "2.2.2.2"])
print(devices.ip)
