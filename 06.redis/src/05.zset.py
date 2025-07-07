from redis import Redis

r = Redis(decode_responses=True)

# создание с указанием весов
r.zadd("leaderboard", {"player1": 100, "player2": 150})
r.zadd("leaderboard", {"player3": 50})

# обновляем вес у записи
r.zadd("leaderboard", {"player1": 50})


# размер множества
r.zcard("leaderboard")

# состав множества
r.zrange("leaderboard", 0, -1, withscores=False)
# ['player1', 'player3', 'player2']
r.zrange("leaderboard", 0, -1, withscores=True)
# [('player1', 50.0), ('player3', 50.0), ('player2', 150.0)]
r.zrange("leaderboard", 0, -1, withscores=True, score_cast_func=int)
# [('player1', 50), ('player3', 50), ('player2', 150)]
r.zrevrange("leaderboard", 0, 0, withscores=True)
# [('player2', 150.0)]

# pop элемента с максимальным весом (zpopmin - минимальным)
r.zpopmax("leaderboard")
