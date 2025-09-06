from os import getenv

REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = getenv("REDIS_PORT", 6379)
REDIS_DB = getenv("REDIS_DB", 0)
REDIS_PASSWORD = getenv("REDIS_PASSWORD", None)
