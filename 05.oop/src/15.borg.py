class RedisPool:
    _state = {}

    def __init__(self):
        self.__dict__ = self._state
        self._session = None

    def connect(self):
        if self._session is None:
            print("first call, need to create connection...")
            self._session = "some redis session"
        else:
            print("session already exists, no need to connect")

    def disconnect(self):
        self._session = None


if __name__ == "__main__":
    r1 = RedisPool()
    r2 = RedisPool()

    print("до первого обращения:")
    print(r1._session)
    print(r2._session)

    r1.connect()
    print("после")
    print(r1._session)
    print(r2._session)

    print("объекты при этом разные")
    print(f"{id(r1) == id(r2) = }")
    print("но атрибуты - единые на всех")
    print(f"{id(r1._session) == id(r2._session) = }")
