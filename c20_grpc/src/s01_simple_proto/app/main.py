"""команда для генерации.

python -m grpc_tools.protoc \
  --proto_path=./proto \
  --python_out=./app/pb \
  --grpc_python_out=./app/pb \
  --mypy_out=./app/pb \
  ./proto/ping.proto
"""

from pb import ping_pb2

reply = ping_pb2.PingReply()
print(f"{reply=}")
print(f"{reply.SerializeToString()=}")
print(f"{reply.ByteSize()=}")

reply.ok = True
print(f"{reply=}")
print(f"{reply.SerializeToString()=}")
print(f"{reply.ByteSize()=}")

reply.Clear()
print(f"{reply=}")
print(f"{reply.SerializeToString()=}")
print(f"{reply.ByteSize()=}")


# сериализация/десериализация через файл
request = ping_pb2.PingRequest(target="привет", ok=True)
with open("msg.bin", "wb") as f:
    f.write(request.SerializeToString())

restored = ping_pb2.PingRequest()
with open("msg.bin", "rb") as f:
    restored.ParseFromString(f.read())
print(restored.target)
print(restored.ok)


# DESCRIPTOR - метаданные
for field in request.DESCRIPTOR.fields:
    print("-" * 20)
    print(f"name   : {field.name}")
    print(f"tag    : {field.number}")
    print(f"type   : {field.type}")
    print(f"default: {field.default_value!r}")
    print(f"default: {field.default_value!r}")
