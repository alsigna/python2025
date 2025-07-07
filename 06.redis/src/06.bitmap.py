from redis import Redis

r = Redis(decode_responses=False)

# bitmap хранится как строка, поэтому минимальный размер 1 байт -> 8 бит
# пн - 0-ой бит, вт - 1-ый бит, ср - 2-ой бит, ...
user_id = 42
bitmap_key = f"user:{user_id}:week_activity"

# активность в пн, ср, чтв
active_days = [0, 2, 3]

for day in active_days:
    r.setbit(bitmap_key, day, 1)

WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
uses_active = []
for i in range(7):
    bit = r.getbit(bitmap_key, i)
    mark = "\u2705" if bit else "\u274c"  # ✅ или ❌
    uses_active.append(f"{WEEKDAYS[i]}: {mark}")

print(f"Активность пользователя {user_id}:")
print("\n".join(uses_active))
