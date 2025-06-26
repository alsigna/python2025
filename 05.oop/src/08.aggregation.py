class Room:
    def __init__(self, name: str, area: int) -> None:
        self.name = name
        self.area = area

    def __str__(self) -> str:
        return f"{self.name} ({self.area} м^2)"


class House:
    def __init__(self, address: str) -> None:
        self.rooms: list[Room] = []
        self.address = address

    def __str__(self) -> str:
        rooms = "\n  ".join(str(room) for room in self.rooms)
        return f"Дом по адресу: {self.address}\nКомнаты:\n  {rooms}"


if __name__ == "__main__":
    kitchen = Room("кухня", 10)
    bedroom = Room("спальня", 12)
    house = House("ул. крылатская 17к4")
    house.rooms.append(kitchen)
    house.rooms.append(bedroom)
    print(house)
    bedroom.area = 15
    print(house)
