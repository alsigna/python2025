eg = ExceptionGroup(
    "Ошибка обработки нескольких задач",
    [
        ValueError("некорректное значение 1"),
        ValueError("некорректное значение 2"),
        TypeError("неверный тип"),
        KeyError("ключ отсутствует 1"),
        KeyError("ключ отсутствует 2"),
    ],
)

print(eg)


try:
    raise eg
except* ValueError as es:
    print("обработка ValueError:", es)
    for e in es.exceptions:
        print(f"\t{e}")
except* TypeError as es:
    print("обработка TypeError:", es)
    for e in es.exceptions:
        print(f"\t{e}")
# except* KeyError as es:
#     print("обработка KeyError:", es)
