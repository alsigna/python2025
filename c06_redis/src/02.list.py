# docker exec -it redis /bin/bash
# root@bfac16e733bc:/data# redis-cli


from redis import Redis

r = Redis(decode_responses=True)

# 127.0.0.1:6379> rpush r-tasks task-1 task-2 task-3
# (integer) 3
tasks = ["task-1", "task-2", "task-3"]
# положить справа
r.rpush("tasks", "task1", "task2", "task-3")
# положить слева
r.lpush("tasks", *tasks)
# размер списка
r.llen("tasks")

# вернуть элемент по индексу
r.lindex("tasks", 2)
# извлечь все элементы
r.lrange("tasks", 0, -1)
# только один элемент
r.lrange("tasks", 2, 2)

# вернуть и удалить один элемент слева
r.lpop("tasks")

# можно указать количество элементов
r.lpop("tasks", 2)

# позиция элемента, можно использовать как проверку принадлежности
r.lpos("tasks", "task-2")
