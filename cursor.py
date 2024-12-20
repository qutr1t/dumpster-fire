import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="user1",
    password = "mypass",
    database = "testdb")

mycursor = mydb.cursor()

mycursor.execute('''
        CREATE TABLE vehicles (
            registration_number VARCHAR(20) PRIMARY KEY,
            veh_type ENUM('CAR', 'VAN', 'MOTORCYCLE') NOT NULL,
            is_handicapped BOOLEAN DEFAULT FALSE
        )
    ''')
mycursor.execute('''
        CREATE TABLE parking_slots (
            slot_number INT PRIMARY KEY,
            spot_type ENUM('HANDICAPPED', 'REGULAR') NOT NULL,
            is_occupied BOOLEAN DEFAULT FALSE,
            vehicle_registration_number VARCHAR(20,
            FOREIGN KEY (vehicle_registration_number) REFERENCES vehicles(registration_number)
        )
    ''')
mycursor.execute('''
        CREATE TABLE tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_registration_number VARCHAR(20) NOT NULL,
            slot_number INT NOT NULL,
            spot_type ENUM('HANDICAPPED', 'REGULAR') NOT NULL,
            issue_time DATETIME NOT NULL,
            exit_time DATETIME,
            fee DECIMAL(10, 2),
            FOREIGN KEY (vehicle_registration_number) REFERENCES vehicles(registration_number),
            FOREIGN KEY (slot_number) REFERENCES parking_slots(slot_number)
        )
    ''')
mydb.commit()
mydb.close()