from flask import Flask, jsonify, request
import time
from parking_lot import ParkingLot
from enums import VehicleType


if __name__ == "__main__":
    parking_lot_capacity = 10
    parking_lot = ParkingLot(parking_lot_capacity)  # Создаем парковку с заданной вместимостью

    # Паркуем некоторые транспортные средства (указывая необходимость в месте для инвалидов)
    parking_lot.park_vehicle("ABC123", VehicleType.CAR, is_handicapped=True)   # Автомобиль для инвалида
    parking_lot.park_vehicle("XYZ789", VehicleType.VAN)                        # Обычный фургон
    
    # Пытаемся припарковать мотоцикл на месте для инвалидов (должно завершиться неудачей)
    parking_lot.park_vehicle("MNO456", VehicleType.MOTORCYCLE)

    time.sleep(2)  # Ждем некоторое время (для тестирования)

    parking_lot.exit_vehicle("ABC123")   # Выход автомобиля и расчет платы за парковку.
    parking_lot.exit_vehicle("ABC123")   # Выход автомобиля и расчет платы за парковку.