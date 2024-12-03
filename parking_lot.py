import math
from models import Vehicle, ParkingSlot, Ticket
from enums import SpotType, VehicleType

# Класс, представляющий парковку
class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity  # Вместимость парковки
        self.slots = []  # Список парковочных мест
        
        # Вычисляем количество мест для инвалидов (30% от общей вместимости)
        num_handicapped_spots = max(1, math.ceil(capacity * 0.3))  # Минимум одно место для инвалидов
        
        # Создаем места для инвалидов для первых 30% слотов
        for i in range(num_handicapped_spots):
            self.slots.append(ParkingSlot(i + 1, SpotType.HANDICAPPED))
        
        # Создаем обычные места для оставшихся слотов
        for i in range(num_handicapped_spots, capacity):
            self.slots.append(ParkingSlot(i + 1, SpotType.REGULAR))
        
        self.tickets = {}  # Словарь для хранения билетов

    def park_vehicle(self, registration_number, veh_type, is_handicapped=False):
        vehicle = Vehicle(registration_number, veh_type, is_handicapped)  # Создаем объект транспортного средства
        
        for slot in self.slots:
            # Проверяем доступность слота и соответствие типу транспортного средства
            if not slot.is_occupied and ((is_handicapped and slot.spot_type == SpotType.HANDICAPPED)or(not is_handicapped and slot.spot_type != SpotType.HANDICAPPED)):
                
                slot.occupy(vehicle)  # Занимаем слот транспортным средством
                ticket = Ticket(vehicle, slot.slot_number, slot.spot_type)  # Создаем билет на парковку
                self.tickets[registration_number] = ticket  # Сохраняем билет по номеру регистрации
                print(f"Выдан билет: Место {slot.slot_number}, {vehicle}, Тип места: {slot.spot_type.value}")
                return ticket
        
        print("Парковка заполнена или транспортное средство не может занять это место!")
        return None

    def exit_vehicle(self, registration_number):
        if registration_number in self.tickets:
            ticket = self.tickets[registration_number]  # Получаем билет по номеру регистрации
            slot = self.slots[ticket.slot_number - 1]  # Находим соответствующее парковочное место
            fee = ticket.calculate_fee()  # Вычисляем плату за парковку
            slot.vacate()  # Освобождаем место
            del self.tickets[registration_number]  # Удаляем билет из системы
            print(f"Транспортное средство с регистрацией {ticket.vehicle.registration_number} покинуло место {ticket.slot_number}. Плата: ${fee:.2f}")
            return fee
        else:
            print("Такое транспортное средство не найдено на парковке!")
            return None

