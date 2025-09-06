# docker exec -it redis /bin/bash
# root@bfac16e733bc:/data# redis-cli


from redis import Redis

r = Redis(decode_responses=True)

# 127.0.0.1:6379> set name bar
# OK
r.set(name="name", value="bar")

# 127.0.0.1:6379> get name
# "bar"
print(r.get(name="name"))

# 127.0.0.1:6379> get title
# (nil)
print(r.get("title"))

# 127.0.0.1:6379> append name -foo
# (integer) 7
r.append(key="name", value="-foo")

# 127.0.0.1:6379> get name
# "bar-foo"
print(r.get(name="name"))

# 127.0.0.1:6379> getrange name 2 5
# "r-fo"
print(r.getrange("name", 2, 4))


# 127.0.0.1:6379> set counter 42
# OK
# 127.0.0.1:6379> get counter
# "42"
# 127.0.0.1:6379> incr counter
# (integer) 43
# 127.0.0.1:6379> get counter
# "43"
# 127.0.0.1:6379> decr counter
# (integer) 42
# 127.0.0.1:6379> get counter
# "42"

r.set("counter", 2)
print(r.incr("counter", 2))
print(r.decr("counter"))
