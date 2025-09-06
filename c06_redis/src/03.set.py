from redis import Redis

r = Redis(decode_responses=True)

# добавить элементы в множество
r.sadd("tags", *["python", "redis"])

# число элементов в множестве
r.scard("tags")

# элементы множества
r.smembers("tags")

# случайный элемент множества
r.srandmember("tags")

# проверка принадлежности множеству (1-входит в состав, иначе 0)
r.sismember("tags", "python")

# удалить последний элемент из множества
r.spop("tags")

# удалить элемент(ы) по значению
r.srem("tags", "python")

r.sadd("old-tags", *["netbox", "python", "scrapli"])
# объединение двух множеств
r.sunion("tags", "old-tags")
# пересечение
r.sinter("tags", "old-tags")
# разность
r.sdiff("tags", "old-tags")
