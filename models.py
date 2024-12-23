import time
import math
from enums import VehicleType, SpotType
from datetime import datetime, timedelta
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
        self.exit_time = None
        self.fee = None
        #self.issue_time=time.time()
        #self.issue_time =time.strftime("%Y-%m-%d %H:%M:%S")
        self.issue_time= datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calculate_fee(self):
        # Структура оплаты в зависимости от типа транспортного средства и типа места
        #self.exit_time = time.time()
        #self.exit_time =  time.strftime("%Y-%m-%d %H:%M:%S")
        self.exit_time =(datetime.now() ).strftime("%Y-%m-%d %H:%M:%S")
        time1 = datetime.strptime(self.issue_time, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(self.exit_time, "%Y-%m-%d %H:%M:%S")
        parked_duration = time2 - time1

        print(parked_duration)
        if self.spot_type == SpotType.HANDICAPPED:
            return 0  # Нет платы за места для инвалидов
        
        hours_parked = math.ceil(parked_duration.total_seconds() / 3600)  # Округляем до ближайшего часа
        
        if self.vehicle.type == VehicleType.VAN:
            self.fee =  hours_parked * 3  # Фургон платит $3 за час
        elif self.vehicle.type == VehicleType.CAR:
            self.fee =  hours_parked * 2  # Автомобиль платит $2 за час
        elif self.vehicle.type == VehicleType.MOTORCYCLE:
            self.fee =  hours_parked * 1  # Мотоцикл платит $1 за час
        return self.fee
