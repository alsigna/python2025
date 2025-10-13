from concurrent import futures

import grpc

from c20_grpc.src.s03_simple_client_server.app.pb import ping_pb2, ping_pb2_grpc


# класс-реализация сервера. Можно не наследоваться от Servicer, единственный метод
# которого мы и так переопределяем, но для чистоты кода лучше это делать
class PingService(ping_pb2_grpc.PingServiceServicer):
    # определяем единственную функцию Ping, описанную в сервисе
    # тут PascalCase идет против snake_case, но это продиктовано фреймворком
    def Ping(  # noqa: N802
        self,
        # входное сообщение
        request: ping_pb2.PingRequest,
        # контекст выполнения RPC, создается на каждый RCP запрос и содержит мета информацию
        # дает возможность управления запросом и каналом (сессией)
        context: grpc.ServicerContext,
        # выходное сообщение
    ) -> ping_pb2.PingReply:
        print(f"новый запрос: {request.target}")
        return ping_pb2.PingReply(
            ok=True,
            msg=f"запрос к {request.target}",
        )


def serve() -> None:
    # создаем сервер, минимально необходимый аргумент - пул потоков - сколько запросов
    # одновременно может обрабатываться. Если будет больше, то они ставятся в очередь
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # определяем сокет, на котором будет слушать запросы сервер
    server.add_insecure_port("[::]:50051")

    # регистрация Services на grpc сервере. Функция генерируется автоматически и имя
    # зависит от имени сервиса. Принимает экземпляр Servicer'а, в котором есть реализация
    # всех prc методов, и сервер (grpc.server), созданный строчкой выше, где нужно регистрировать.
    # если на сервере нужно обслуживать более одного сервиса, то каждый регистрируется отдельно.
    # в результате
    # - сервер знает, у него есть сервис PingService и запросы по маршруту
    #   app.ping.v1.PingService/Ping будут привязаны к методу PingService().Ping()
    # - для каждого rpc метода сервиса будет создан обработчик, который умеет принимать и
    #   десериализовать запросы, вызывать python-метод который мы реализовали, сериализовать
    #   результат и отправлять бинарные данные клиенту
    ping_pb2_grpc.add_PingServiceServicer_to_server(PingService(), server)

    try:
        # запуск сервера, это не блокирующий метод, поэтому сервер стартует и начинает обрабатывать
        # запросы в потоках, но main-thread продолжает выполняться, и если он будет закончен, то и
        # порожденные им потоки так же будут закрыты.
        server.start()
        print("gRPC сервер запущен на порту 50051")
        # поэтому блокируем main-thread вручную
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Остановка сервера...")
        # остановка сервера, 0 - без graceful, но можно дать время на мягкое завершение
        server.stop(0)


if __name__ == "__main__":
    serve()
