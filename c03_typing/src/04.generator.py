from collections.abc import Generator


def processor() -> Generator[int, int | None, int]:
    agg_sum = 0
    while True:
        # возвращаем текущий agg_sum (поэтому нужна инициализация), получаем значение из send()
        received_value = yield agg_sum
        # проверяем полученное значение на условие
        if received_value is None:
            # завершение генератора
            return agg_sum
        agg_sum += received_value


if __name__ == "__main__":
    # создание
    gen = processor()
    # инициализация, доходим первый раз до yield, который возвращает 0
    # и ждет очередного значения через send
    print(next(gen))

    # передаем в send новые параметры. Это событие возобновляет генератор до очередного yield
    print(gen.send(1))
    print(gen.send(2))
    print(gen.send(5))

    # завершение
    try:
        gen.send(None)
    except StopIteration as exc:
        # значение, возвращаемое через return доступно по атрибуту value
        print(f"Итог: {exc.value}")
