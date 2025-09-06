from redis import Redis

r = Redis(decode_responses=True)


# задать значения (items устаревший аргумент, сейчас mapping)
r.hset(name="user:1", mapping={"name": "Alice", "age": 30})
r.hset(name="user:2", key="name", value="Bob")

# получить значение по ключу
r.hget(name="user:1", key="age")
# все значения (dict)
r.hgetall(name="user:1")
# список ключей (dict.keys)
r.hkeys(name="user:1")
# список значение (dict.values)
r.hvals(name="user:1")
