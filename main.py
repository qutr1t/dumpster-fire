from flask import Flask, jsonify, request, render_template
from parking_lot import ParkingLot
from enums import VehicleType, SpotType
import time

# Инициализация приложения Flask
app = Flask(__name__)
# Создание парковки с 100 местами
parking_lot = ParkingLot(100)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    # Получение истории парковки из ParkingLot
    history = parking_lot.get_parking_history()
    return render_template('history.html', history=history)

@app.route('/api/slots', methods=['GET'])
def get_slots():
    slots_info = []
    for slot in parking_lot.slots:
        slot_info = {
            'slot_number': slot.slot_number,
            'is_occupied': slot.is_occupied,
            'vehicle': str(slot.vehicle) if slot.is_occupied else None,
            'spot_type': slot.spot_type.value
        }
        slots_info.append(slot_info)
    return jsonify(slots_info)

@app.route('/api/park', methods=['POST'])
def park_vehicle():
    data = request.json
    registration_number = data.get('registration_number')

    if not registration_number:
        return jsonify({"message": "Registration number is required"}), 400
    
    try:
        veh_type = VehicleType[data.get('veh_type')]
    except KeyError:
        return jsonify({"message": "Invalid vehicle type"}), 400
    
    is_handicapped = data.get('is_handicapped', False)
    
    ticket = parking_lot.park_vehicle(registration_number, veh_type, is_handicapped)
    
    if ticket == -1:
        return jsonify({"message": "Парковка переполнена"}), 400
    if ticket == -2:
        return jsonify({"message": "Это транспортное средство уже заняло место на парковке!"}), 400
    
    return jsonify({"message": "Vehicle parked successfully", "ticket": str(ticket), "slot_number": ticket.slot_number}), 200

@app.route('/api/exit', methods=['POST'])
def exit_vehicle():
    data = request.json
    registration_number = data.get('registration_number')
    
    fee = parking_lot.exit_vehicle(registration_number)
    
    if fee is not None:
        # Обновление истории парковки с временем выезда и стоимостью будет происходить автоматически в методе exit_vehicle класса ParkingLot.
        return jsonify({"message": "Vehicle exited successfully", "fee": fee}), 200
    else:
        return jsonify({"message": "Vehicle not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)