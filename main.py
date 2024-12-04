from flask import Flask, jsonify, request, render_template
from parking_lot import ParkingLot
from enums import VehicleType, SpotType
import time
import math

# Инициализация приложения Flask
app = Flask(__name__)
# Создание парковки с 5 местами
parking_lot = ParkingLot(5)

# Хранение истории парковки
parking_history = []

@app.route('/')
def home():
    # Отображение главной страницы
    return render_template('index.html')

@app.route('/history')
def history():
    # Отображение страницы с историей парковки
    return render_template('history.html', history=parking_history)

@app.route('/api/slots', methods=['GET'])
def get_slots():
    # Получение информации о парковочных местах
    slots_info = []
    for slot in parking_lot.slots:
        slot_info = {
            'slot_number': slot.slot_number,  # Номер места
            'is_occupied': slot.is_occupied,   # Занято ли место
            'vehicle': str(slot.vehicle) if slot.is_occupied else None,  # Транспортное средство на месте (если занято)
            'spot_type': slot.spot_type.value   # Тип парковочного места
        }
        slots_info.append(slot_info)
    return jsonify(slots_info)  # Возврат информации в формате JSON

@app.route('/api/park', methods=['POST'])
def park_vehicle():
    # Парковка транспортного средства
    data = request.json  # Получение данных из запроса
    registration_number = data.get('registration_number')  # Номер регистрации

    if not registration_number:
        return jsonify({"message": "Registration number is required"}), 400  # Ошибка, если номер регистрации не указан
    
    try:
        veh_type = VehicleType[data.get('veh_type')]  # Получение типа транспортного средства
    except KeyError:
        return jsonify({"message": "Invalid vehicle type"}), 400  # Ошибка, если тип транспортного средства некорректен
    
    is_handicapped = data.get('is_handicapped', False)  # Проверка на наличие инвалидности
    
    ticket = parking_lot.park_vehicle(registration_number, veh_type, is_handicapped)  # Попытка припарковать транспортное средство
    if ticket == -1:
        return jsonify({"message": "Парковка переполнена"}), 400  # Ошибка, если парковка переполнена
    if ticket == -2:
        return jsonify({"message": "Это транспортное средство уже заняло место на парковке!"}), 400  # Ошибка, если транспортное средство уже занято
    
    elif ticket:
        # Добавление информации о билете в историю парковки
        parking_history.append({
            'registration_number': registration_number,
            'slot_number': ticket.slot_number,
            'vehicle_type': ticket.vehicle.type.value,
            'issue_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ticket.issue_time)),  # Время выдачи билета
            'exit_time': None,
            'fee': None
        })
        return jsonify({"message": "Vehicle parked successfully", "ticket": str(ticket), "slot_number": ticket.slot_number}), 200  # Успешная парковка
    
    else:
        return jsonify({"message": "Parking failed"}), 400  # Ошибка при парковке

@app.route('/api/exit', methods=['POST'])
def exit_vehicle():
    # Выезд транспортного средства с парковки
    data = request.json  # Получение данных из запроса
    registration_number = data.get('registration_number')  # Номер регистрации
    
    fee = parking_lot.exit_vehicle(registration_number)  # Вычисление стоимости за выезд
    
    if fee is not None:
        # Обновление истории парковки с временем выезда и стоимостью
        for record in parking_history:
            if record['registration_number'] == registration_number and record['exit_time'] is None:
                record['exit_time'] = time.strftime('%Y-%m-%d %H:%M:%S')  # Время выезда
                record['fee'] = fee  # Стоимость за выезд
                break
        
        return jsonify({"message": "Vehicle exited successfully", "fee": fee}), 200  # Успешный выезд
    else:
        return jsonify({"message": "Vehicle not found"}), 404  # Ошибка, если транспортное средство не найдено

if __name__ == '__main__':
    app.run(debug=True)  # Запуск приложения в режиме отладки