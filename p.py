import math
from models import Vehicle, ParkingSlot, Ticket
from enums import SpotType, VehicleType
import time

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
        
        self.tickets = {}  # Словарь для хранения активных билетов
        self.parking_history = []  # Список для хранения всей истории парковки

    def park_vehicle(self, registration_number, veh_type, is_handicapped=False):
        # Проверяем, есть ли уже билет на это транспортное средство
        if registration_number in self.tickets:
            print("Это транспортное средство уже заняло место на парковке!")
            return -2
        
        vehicle = Vehicle(registration_number, veh_type, is_handicapped)  # Создаем объект транспортного средства
        
        for slot in self.slots:
            # Проверяем доступность слота и соответствие типу транспортного средства
            if not slot.is_occupied and ((is_handicapped and slot.spot_type == SpotType.HANDICAPPED) or (not is_handicapped and slot.spot_type != SpotType.HANDICAPPED)):
                
                slot.occupy(vehicle)  # Занимаем слот транспортным средством
                ticket = Ticket(vehicle, slot.slot_number, slot.spot_type)  # Создаем билет на парковку
                
                self.tickets[registration_number] = ticket  # Сохраняем билет по номеру автомобиля
                self.parking_history.append(ticket)  # Добавляем билет в историю парковки
                
                print(f"Выдан билет: Место {slot.slot_number}, {vehicle}, Тип места: {slot.spot_type.value}")
                return ticket
        
        print("Парковка заполнена или транспортное средство не может занять это место!")
        return -1

    def exit_vehicle(self, registration_number):
        if registration_number in self.tickets:
            ticket = self.tickets[registration_number]  # Получаем билет по номеру автомобиля
            slot = self.slots[ticket.slot_number - 1]  # Находим соответствующее парковочное место
            
            fee = ticket.calculate_fee()  # Вычисляем плату за парковку
            
            slot.vacate()  # Освобождаем место
            
            ticket.exit_time = time.time()  # Устанавливаем время выезда
            
            print(f"Транспортное средство с регистрацией {ticket.vehicle.registration_number} покинуло место {ticket.slot_number}. Плата: ${fee:.2f}")
            
            del self.tickets[registration_number]  # Удаляем билет из активных билетов
            
            return fee
        else:
            print("Такое транспортное средство не найдено на парковке!")
            return None

    def get_parking_history(self):
        history = []
        
        for ticket in self.parking_history:
            if ticket.exit_time is None:
                status = "Активен"
            else:
                status = "Завершен"
                
            history.append({
                'registration_number': ticket.vehicle.registration_number,
                'slot_number': ticket.slot_number,
                'spot_type': ticket.spot_type.value,
                'issue_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ticket.issue_time)),
                'exit_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ticket.exit_time)) if ticket.exit_time else None,
                'fee': ticket.fee if hasattr(ticket, 'fee') else None,
                'status': status
            })
        
        return history  # Возвращаем всю историю парковки с информацией о статусе каждого билета

