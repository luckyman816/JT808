import sqlite3
import struct
from protocol import construct_message

def parse_terminal_registration_message(data):

    provincial_id = int.from_bytes(data[0:2], byteorder='little')
    area_id = int.from_bytes(data[2:4], byteorder='little')
    manufacturer_id = data[4:9].decode('utf-8')
    terminal_model = data[9:29].decode('utf-8')
    terminal_id = data[29:36].decode('utf-8')
    license_plate_color = data[36:37].decode('utf-8')
    plate_number = data[37:len(data)-1].decode('utf-8')

    return {
        'province_id': provincial_id,
        'city_id': area_id,
        'manufacturer_id': manufacturer_id,
        'terminal_model': terminal_model,
        'terminal_id': terminal_id,
        'license_plate_color': license_plate_color,
        'plate_number': plate_number
    }
def construct_terminal_registration_response(serial_number, result, auth_code=''):
    message_id = 0x8100
    response_body = struct.pack('>HB', serial_number, result)
    if result == 0:
        response_body += auth_code.encode('ascii')

    return response_body

def handle_terminal_registration(message_id,  serial_number, phone_num , data):
    registration_info = parse_terminal_registration_message(data)
    save_to_database(registration_info)
    result = 0
    auth_code = 'some_auth_code'  # Generate or retrieve an appropriate auth code
    response_data = serial_number.to_bytes(2, byteorder='big') + result.to_bytes(1, byteorder='big') + auth_code.encode('utf-8')
    response = construct_message(message_id, phone_num, response_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)
    return response


def save_to_database(registration_info):
    connection = sqlite3.connect('vehicle_data.db')
    cursor = connection.cursor()
    cursor.execute('select max(id) from vehicles')

    result = cursor.fetchone()
    print(f"data result {result}")
    max_id = result[0] if result[0]  else 0
    max_id += 1
    cursor.execute('''
        INSERT INTO vehicles (id,province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, plate_number)
        VALUES (?,?, ?, ?, ?, ?, ?, ?)
    ''', (
        max_id,
        registration_info['province_id'],
        registration_info['city_id'],
        registration_info['manufacturer_id'],
        registration_info['terminal_model'],
        registration_info['terminal_id'],
        registration_info['license_plate_color'],
        registration_info['plate_number']
    ))
    connection.commit()
    connection.close()
def save_to_positions_database(registration_info):
    connection = sqlite3.connect( 'vehicle_data.db' )
    cursor = connection.cursor()
    cursor.execute('select max(id) from positions')
    
    result = cursor.fetchone()
    print(f"data result {result}")
    max_id = result[0] if result[0]  else 0
    max_id += 1
    cursor.execute('''
        INSERT INTO positions (id,deviceId, latitude, longitude, speed, direction, address, signal, door, mt2v_dc_volt, deviceTime, createdAt, updatedAt)
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
    ''', (
        max_id,
        registration_info['deviceId'],
        registration_info['latitude'],
        registration_info['longitude'],
        registration_info['speed'],
        registration_info['direction'],
        registration_info['address'],
        registration_info['signal'],
        registration_info['door'],
        registration_info['mt2v_dc_volt_bytes'],
        registration_info['deviceTime'],
        '',
        ''
    ))
    connection.commit()
    connection.close()
def db_check():

    vecicle_table = 'CREATE TABLE IF NOT EXISTS vehicles (id INT AUTO_INCREMENT,\
                    province_id INT,\
                    city_id INT,\
                    manufacturer_id INT,\
                    terminal_model VARCHAR(100),\
                    terminal_id INT,\
                    license_plate_color VARCHAR(50),\
                    plate_number VARCHAR(50),\
                    PRIMARY KEY (id)\
                    )'
    location_table =  'CREATE TABLE IF NOT EXISTS location (\
                        id INT AUTO_INCREMENT,\
                        warning_mark INT,\
                        acc_flag TINYINT,\
                        pos_flag TINYINT,\
                        latitude DECIMAL(10, 7),\
                        longitude DECIMAL(10, 7),\
                        altitude VARCHAR(255),\
                        velocity VARCHAR(255),\
                        plate_number VARCHAR(50),\
                        direction INT,\
                        time TIMESTAMP,\
                        PRIMARY KEY (id))'
    devices_table = 'CREATE TABLE IF NOT EXISTS devices ( id INT AUTO_INCREMENT,\
                        deviceType VARCHAR(255) NOT NULL DEFAULT \'moovetrax\',\
                        name VARCHAR(255) DEFAULT NULL,\
                        uniqueId VARCHAR(255) DEFAULT NULL,\
                        vehicleId VARCHAR(255) NOT NULL DEFAULT \'\',\
                        userId INT DEFAULT NULL,\
                        model VARCHAR(255) DEFAULT NULL,\
                        make VARCHAR(255) DEFAULT NULL,\
                        category VARCHAR(255) DEFAULT NULL,\
                        color VARCHAR(255) DEFAULT NULL,\
                        vin VARCHAR(255) DEFAULT NULL,\
                        license_tag VARCHAR(255) NOT NULL DEFAULT \'\',\
                        distance_unit VARCHAR(20) NOT NULL DEFAULT \'mile\' CHECK(distance_unit IN (\'mile\', \'km\')),\
                        iccid VARCHAR(255) DEFAULT NULL,\
                        prev_od DECIMAL(10,1) NOT NULL DEFAULT 0.0,\
                        odometer DECIMAL(10,1) NOT NULL DEFAULT 0.0,\
                        attributes TEXT,\
                        gpsIp VARCHAR(255) DEFAULT NULL,\
                        gpsPort INT DEFAULT NULL,\
                        status VARCHAR(255) DEFAULT NULL,\
                        lastStatusChanged DATETIME DEFAULT CURRENT_TIMESTAMP,\
                        lock_status VARCHAR(50) NOT NULL DEFAULT \'\',\
                        lock_status_timestamp DATETIME DEFAULT NULL,\
                        kill_status VARCHAR(50) NOT NULL DEFAULT \'\',\
                        kill_status_timestamp DATETIME DEFAULT NULL,\
                        mt2v_bt_status TINYINT(1) NOT NULL DEFAULT \'0\',\
                        mt2v_bt_name VARCHAR(255) NOT NULL DEFAULT \'\',\
                        mt2v_bt_pin VARCHAR(6) NOT NULL DEFAULT \'\',\
                        mt2v_bt_signal INT NOT NULL DEFAULT \'0\',\
                        mt2v_bt_distance INT NOT NULL DEFAULT \'0\',\
                        mt2v_bt_on_status VARCHAR(50) NOT NULL DEFAULT \'\',\
                        mt2v_bt_lock_status VARCHAR(50) NOT NULL DEFAULT \'\',\
                        mt2v_bt_lock_status_timestamp DATETIME DEFAULT NULL,\
                        mt2v_bt_initialize TINYINT(1) DEFAULT \'0\',\
                        mt2v_dc_volt DECIMAL(10,1) DEFAULT NULL,\
                        mt2v_hood_volt DECIMAL(10,1) DEFAULT NULL,\
                        mt2v_hood_open_volt DECIMAL(10,1) DEFAULT NULL,\
                        mt2v_door_volt DECIMAL(10,1) DEFAULT NULL,\
                        mt2v_door_open_volt DECIMAL(10,1) DEFAULT NULL,\
                        mt3v_shock_status TINYINT(1) DEFAULT NULL,\
                        mt3v_shock_sensitivity INT DEFAULT NULL,\
                        mt3v_shock_duration INT DEFAULT NULL,\
                        imei VARCHAR(255) NOT NULL DEFAULT \'\',\
                        ignition_status VARCHAR(10) NOT NULL DEFAULT \'on\',\
                        lockUnlockSetting TEXT,\
                        latitude DOUBLE DEFAULT NULL,\
                        longitude DOUBLE DEFAULT NULL,\
                        speed INT DEFAULT NULL,\
                        overspeed INT DEFAULT NULL,\
                        direction INT DEFAULT NULL,\
                        acc TINYINT(1) NOT NULL DEFAULT \'0\',\
                        disabled TINYINT(1) DEFAULT NULL,\
                        isDoubleUnlock TINYINT(1) DEFAULT NULL,\
                        isDoubleLock TINYINT(1) DEFAULT NULL,\
                        enableCycle TINYINT(1) NOT NULL DEFAULT \'0\',\
                        enableInstaller TINYINT(1) NOT NULL DEFAULT \'0\',\
                        signal INT DEFAULT NULL,\
                        fuel INT DEFAULT NULL,\
                        maxFuel INT DEFAULT NULL,\
                        minFuel INT DEFAULT NULL,\
                        apiKey VARCHAR(255) DEFAULT NULL,\
                        door TINYINT(1) DEFAULT NULL,\
                        billing_source VARCHAR(50) NOT NULL DEFAULT \'paypal\',\
                        escrow_user_id INT NOT NULL DEFAULT \'0\',\
                        monthly_cost DECIMAL(10,2) NOT NULL DEFAULT \'15.00\',\
                        billing_days INT NOT NULL DEFAULT \'0\',\
                        credit DECIMAL(10,2) NOT NULL DEFAULT \'0.00\',\
                        reseller_applied TINYINT(1) NOT NULL DEFAULT \'0\',\
                        plan_id VARCHAR(255) NOT NULL DEFAULT \'\',\
                        subscription_id VARCHAR(255) NOT NULL DEFAULT \'\',\
                        lastPosition DATETIME DEFAULT NULL,\
                        lastConnect DATETIME DEFAULT NULL,\
                        lastAcc DATETIME DEFAULT NULL,\
                        factory_passed TINYINT(1) NOT NULL DEFAULT \'0\',\
                        firmwareVersion VARCHAR(20) NOT NULL DEFAULT \'\',\
                        firmwareVersionUpdatedAt DATETIME DEFAULT NULL,\
                        smartcar_subscribed TINYINT(1) NOT NULL DEFAULT \'0\',\
                        accessToken VARCHAR(255) NOT NULL DEFAULT \'\',\
                        refreshToken VARCHAR(255) NOT NULL DEFAULT \'\',\
                        measure_type VARCHAR(20) NOT NULL DEFAULT \'smoke\',\
                        no_smoke_volt INT NOT NULL DEFAULT \'1\',\
                        smoke_status TINYINT(1) NOT NULL DEFAULT \'0\',\
                        last_smoke_volt INT NOT NULL DEFAULT \'0\',\
                        last_smoke_timestamp DATETIME DEFAULT NULL,\
                        notificationSettings TEXT,\
                        commandSetting TEXT ,\
                        connected_device_id INT NOT NULL DEFAULT \'0\',\
                        image VARCHAR(1000) NOT NULL DEFAULT \'\',\
                        share_settings TEXT,\
                        share_setting_enabled TINYINT(1) NOT NULL DEFAULT \'0\',\
                        maint_charge_enabled TINYINT(1) DEFAULT NULL,\
                        maint_notification_email VARCHAR(255) NOT NULL DEFAULT \'\',\
                        turo_settings TEXT,\
                        turo_setting_disabled TINYINT(1) NOT NULL DEFAULT \'0\',\
                        abi TINYINT(1) DEFAULT NULL,\
                        createdAt DATETIME NOT NULL,\
                        updatedAt DATETIME NOT NULL,\
                        PRIMARY KEY (id, updatedAt))'
    raw_table = 'CREATE TABLE IF NOT EXISTS raw ( id INT AUTO_INCREMENT, data LONGTEXT, PRIMARY KEY (id) )'                
    positions_table = 'CREATE TABLE IF NOT EXISTS positions ( id INT AUTO_INCREMENT,\
                        deviceId INT DEFAULT NULL,\
                        latitude DOUBLE DEFAULT NULL,\
                        longitude DOUBLE DEFAULT NULL,\
                        speed INT DEFAULT NULL,\
                        direction INT DEFAULT NULL,\
                        address VARCHAR(255) DEFAULT NULL,\
                        signal INT DEFAULT NULL,\
                        door TINYINT(1) DEFAULT NULL,\
                        mt2v_dc_volt DECIMAL(10,1) DEFAULT NULL,\
                        deviceTime DATETIME NOT NULL,\
                        createdAt DATETIME NOT NULL,\
                        updatedAt DATETIME NOT NULL,\
                        PRIMARY KEY (id, deviceTime) )'
        
    connection = sqlite3.connect('vehicle_data.db')
    cursor = connection.cursor()
    cursor.execute(vecicle_table)
    cursor.execute(location_table)
    cursor.execute(devices_table)
    cursor.execute(raw_table)
    cursor.execute(positions_table)
    connection.commit()
    connection.close()


