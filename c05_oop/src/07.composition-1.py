class Engine:
    def start(self):
        print("двигатель запущен")


class Car:
    def __init__(self, model: str):
        self.model = model
        self.engine = Engine()

    def drive(self):
        self.engine.start()
        print("автомобиль едет")


if __name__ == "__main__":
    car = Car("camry")
    car.drive()
