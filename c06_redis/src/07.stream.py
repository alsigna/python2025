from redis import Redis

r = Redis(decode_responses=True)

TOPIC = "netbox:device:actions"
CONSUMER_GROUP = "workers"

# публикация сообщений
msg_ids = [
    r.xadd(TOPIC, {"user": "alice", "action": "create", "device": "r01"}),
    r.xadd(TOPIC, {"user": "bob", "action": "delete", "device": "r02"}),
]

# чтение сообщений

# чтений всего диапазона
msgs = r.xrange(TOPIC, min="-", max="+")
for msg_id, fields in msgs:
    print(f"{msg_id} => {fields}")

# создание consumer группы
r.xgroup_create(
    name=TOPIC,  # имя stream
    groupname=CONSUMER_GROUP,  # имя группы, должны быть уникальны на весь redis
    id="0",  # offset, $ - с последнего сообщения (по умолчанию)
    mkstream=True,  # создаем stream, если его нет, иначе при попытке создания группы будет ошибка
)


# чтение из группы
entries = r.xreadgroup(
    groupname=CONSUMER_GROUP,
    consumername="consumer-1",
    streams={TOPIC: ">"},
    count=2,
)
for stream, messages in entries:
    for msg_id, fields in messages:
        print(f"[{stream}] [{msg_id}] {fields}")


# подтверждение сообщения
r.xack(TOPIC, CONSUMER_GROUP, msg_id)

# сообщения, ожидающие подтверждения
r.xpending(TOPIC, CONSUMER_GROUP)
# {
#     "pending": 1,
#     "min": "1751876390721-0",
#     "max": "1751876390721-0",
#     "consumers": [
#         {
#             "name": "consumer-1",
#             "pending": 1,
#         },
#     ],
# }

# забрать сообщения себе
r.xclaim(
    name=TOPIC,  # имя stream
    groupname=CONSUMER_GROUP,  # имя группы
    consumername="consumer-2",  # имя нового consumer'a
    min_idle_time=60000,  # забирать сообщения, находящиеся в pending более 60сек
    message_ids=msg_ids,  # список id сообщений
)
