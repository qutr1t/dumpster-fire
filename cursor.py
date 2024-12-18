import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="user1",
    password = "mypass",
    database = "testdb")

mycursor = mydb.cursor()

mycursor.execute('''
        CREATE TABLE IF NOT EXISTS ParkingSlot (
            slot_number INT PRIMARY KEY,
            spot_type ENUM('HANDICAPPED', 'REGULAR'),
            is_occupied BOOLEAN DEFAULT FALSE
        )
    ''')
mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Vehicle (
            registration_number VARCHAR(20) PRIMARY KEY,
            veh_type ENUM('CAR', 'MOTORCYCLE', 'VAN'),
            is_handicapped BOOLEAN DEFAULT FALSE
        )
    ''')
mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Ticket (
            id INT PRIMARY KEY AUTO_INCREMENT,
            vehicle_registration_number VARCHAR(20),
            slot_number INT,
            issue_time DATETIME,
            exit_time DATETIME,
            fee DECIMAL(10, 2),
            FOREIGN KEY (vehicle_registration_number) REFERENCES Vehicle(registration_number),
            FOREIGN KEY (slot_number) REFERENCES ParkingSlot(slot_number)
        )
    ''')
mydb.commit()
mydb.close()