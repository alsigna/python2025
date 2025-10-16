import subprocess

import grpc
from pb import ping_pb2, ping_pb2_grpc

# создание insecure_channel — канала без TLS (plaintext в cli), канал это HTTP/2 соединение под капотом
# канал потокобезопасен - можно использовать из разных потоков
# объект канала ленивый, т.е. его создание не равно установление tcp сессии с сервером. channel знает куда
# и как подключаться, но реальное подключение будет при первом вызове rpc метода.
channel = grpc.insecure_channel(
    target="localhost:50051",
)

# stub-обертка, для вызова rpc. При создании передаем channel, по которому будет идти взаимодействие.
# объект занимается сериализацией/десериализацией сообщений. stub - легковесный и потокобезопасный
stub = ping_pb2_grpc.PingServiceStub(channel)  # type: ignore[no-untyped-call]

# создаем сообщение и передаем его как аргумент в метод stub-объекта. Это блокирующий метод и на этом
# места исполнение кода блокируется до получения ответа или таймаута/ошибки
# подключение к серверу (tcp сессия) создается в этом месте, а не при создании канала. Т.е. в этой
# строке будет:
# - установка tcp-сессии (если запрос первый и сессии еще нет), http/2 handshake
# - отправка rpc-запроса
# - получение ответа
response: ping_pb2.PingReply = stub.Ping(ping_pb2.PingRequest(target="example.com"))
print(response)

# закрываем канал
channel.close()


def show_tcp_sessions() -> None:
    lsof = subprocess.run(  # noqa: S603
        ["lsof", "-iTCP:50051"],  # noqa: S607
        encoding="utf-8",
        stdout=subprocess.PIPE,
    )
    print(lsof.stdout)


# channel поддерживает контекстный менеджер, и close выполняется автоматически при выходе
with grpc.insecure_channel(
    target="localhost:50051",
) as channel:
    # show_tcp_sessions()
    # можно принудительно установить tcp сессию до первого обращения
    # grpc.channel_ready_future(channel).result(timeout=2)
    # show_tcp_sessions()
    stub = ping_pb2_grpc.PingServiceStub(channel)  # type: ignore[no-untyped-call]
    response = stub.Ping(ping_pb2.PingRequest(target="example.com"))
    print(response)
    # show_tcp_sessions()
# show_tcp_sessions()
