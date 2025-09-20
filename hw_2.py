'''
Создать базовый класс Vehicle (транспортное средство), который должен содержать:
приватные атрибуты _brand (марка) и _speed (скорость);
свойство brand: доступно только для чтения (read-only, без setter), изменить марку после создания объекта нельзя;
свойство speed: доступно для чтения и изменения, при установке (setter) не допускает отрицательных значений,
при попытке задать отрицательное значение выбрасывает ValueError
(почитай про исключения https://skillbox.ru/media/code/isklyucheniya-v-python-chto-eto-takoe-i-kak-s-nimi-rabotat/)
метод get_info() для вывода общей информации о транспорте.


Создать классы-наследники:
Car — дополнительно имеет поле seats (количество мест),
Bus — дополнительно имеет поле capacity (вместимость пассажиров),
Bike — дополнительно имеет поле bike_type (например, "горный" или "шоссейный").

В каждом из этих классов переопределить метод get_info(), чтобы он выводил общие данные из базового класса и
свои специфические данные.

Добавить метод trip_cost(distance) в каждый класс:
Для Car стоимость рассчитывается как distance * 0.1. Для Bus — distance * 0.05 * capacity. Для Bike — 0 (поездка бесплатная).

Создать список из объектов разных классов (Car, Bus, Bike) и в цикле:
вывести их информацию через метод get_info(),
посчитать стоимость поездки на дистанцию, например, 100 км.
'''


class Vehicle:
    def __init__(self, brand, speed):
        self._brand = brand
        self._speed = speed

    def get_info(self):
        print(f"Марка транспортного средства: {self._brand}. Максимально возможная скорость: {self._speed} км/ч")

    @property
    def brand(self):
        print(f"Марка транспортного средства: {self._brand}")
        return self._brand

    @property
    def speed(self):
        print(f"Максимально возможная скорость: {self._speed}")
        return self._speed

    @speed.setter
    def speed(self, new_speed_value):
        if new_speed_value < 0:
            raise ValueError("Скорость не может быть отрицательной!")
        self._speed = new_speed_value


class Car(Vehicle):
    def __init__(self, brand, speed, seats):
        super().__init__(brand,speed)
        self.seats = seats
        self.get_info()

    def get_info(self):
        super().get_info()
        print(f"Количество мест: {self.seats}")

    def trip_cost(self, distance):
        print(f"Стоимость поездки: {(distance * 0.1):.2f} руб.")


class Bus(Vehicle):
    def __init__(self, brand, speed, capacity):
        super().__init__(brand, speed)
        self.capacity = capacity
        self.get_info()

    def get_info(self):
        super().get_info()
        print(f"Вместимость пассажиров: {self.capacity}")

    def trip_cost(self, distance):
        print(f"Стоимость поездки: {(distance * 0.05 * self.capacity):.2f} руб.")


class Bike(Vehicle):
    def __init__(self, brand, speed, bike_type):
        super().__init__(brand, speed)
        self.bike_type = bike_type
        self.get_info()

    def get_info(self):
        super().get_info()
        print(f"Тип велосипеда: {self.bike_type}")

    def trip_cost(self, distance):
        print(f"Стоимость поездки: {distance * 0} руб.")


car1 = Car("BMW", 220, 5)
bus1 = Bus("Mercedes", 150, 100)
bike1 = Bike("Lapierre", 40, "горный")
print("-" * 30)

for i in car1, bus1, bike1:
    i.get_info()
    i.trip_cost(100)
    print("-" * 30)

