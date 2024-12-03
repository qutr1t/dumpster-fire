import time
import math
from enums import VehicleType, SpotType
# Класс, представляющий транспортное средство
class Vehicle:
    def __init__(self, registration_number, veh_type, is_handicapped=False):
        self.registration_number = registration_number  # Номер регистрации
        self.type = veh_type  # Тип транспортного средства
        self.is_handicapped = is_handicapped  # Указывает, нуждается ли водитель в месте для инвалидов

    def __str__(self):
        return f"Транспортное средство(Регистрация: {self.registration_number}, Тип: {self.type.value}, Инвалид: {self.is_handicapped})"


# Класс, представляющий парковочное место
class ParkingSlot:
    def __init__(self, slot_number, spot_type):
        self.slot_number = slot_number  # Номер парковочного места
        self.is_occupied = False  # Занято ли место
        self.vehicle = None  # Транспортное средство, занимающее место
        self.spot_type = spot_type  # Тип парковочного места

    def occupy(self, vehicle):
        self.is_occupied = True  # Помечаем место как занятое
        self.vehicle = vehicle  # Записываем занятое транспортное средство

    def vacate(self):
        self.is_occupied = False  # Освобождаем место
        self.vehicle = None  # Удаляем информацию о транспортном средстве


# Класс, представляющий билет на парковку
class Ticket:
    def __init__(self, vehicle, slot_number, spot_type):
        self.vehicle = vehicle  # Транспортное средство
        self.slot_number = slot_number  # Номер парковочного места
        self.spot_type = spot_type  # Тип парковочного места
        self.issue_time = time.time()  # Время выдачи билета

    def calculate_fee(self):
        # Структура оплаты в зависимости от типа транспортного средства и типа места
        self.exit_time = time.time()
        parked_duration = self.exit_time - self.issue_time
        
        if self.spot_type == SpotType.HANDICAPPED:
            return 0  # Нет платы за места для инвалидов
        
        hours_parked = math.ceil(parked_duration / 3600)  # Округляем до ближайшего часа
        
        if self.vehicle.type == VehicleType.VAN:
            return hours_parked * 3  # Фургон платит $3 за час
        elif self.vehicle.type == VehicleType.CAR:
            return hours_parked * 2  # Автомобиль платит $2 за час
        elif self.vehicle.type == VehicleType.MOTORCYCLE:
            return hours_parked * 1  # Мотоцикл платит $1 за час
