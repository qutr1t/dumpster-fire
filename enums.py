from enum import Enum

# Перечисление типов транспортных средств
class VehicleType(Enum):
    CAR = "Автомобиль"
    VAN = "Фургон"
    MOTORCYCLE = "Мотоцикл"

# Перечисление типов парковочных мест
class SpotType(Enum):
    REGULAR = "Обычное"
    HANDICAPPED = "Для инвалидов"