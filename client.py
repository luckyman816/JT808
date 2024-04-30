import socket
import struct
from protocol import construct_message, parse_message
from utilities import bcd_encode

def send_message(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message)
        response = s.recv(1024)
    return response

def handle_recv_message(data):
    parsed_data = parse_message(data=data, private_key=None)
    if parsed_data['message_id'] == 0x8100:
        handle_registration_response(parsed_data['body'])
    elif parsed_data['message_id'] == 0x8300:
        handle_information_distribution(parsed_data['body'])
    elif parsed_data['message_id'] == 0x0102:
        handle_registration_response(parsed_data['body'])

def send_terminal_registration_message(vehicle_data):
    body = struct.pack('>HH5s20s7sB', vehicle_data.province_id, vehicle_data.city_id, vehicle_data.manufacturer_id.encode('ascii'), vehicle_data.terminal_model.encode('ascii'), vehicle_data.terminal_id.encode('ascii'), vehicle_data.license_plate_color)
    body += vehicle_data.plate_number.encode('GBK')
    message = construct_message(message_id = 0x0100, phone_number=bcd_encode(123), body=body, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)
    send_message(host='127.0.0.1', port='1234', message=message)

def construct_reg_body(provincial_id, area_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, plate_number):
   
    provincial_bytes = provincial_id.to_bytes(2, byteorder='big')
    area_bytes = area_id.to_bytes(2, byteorder='big')
    manufacturer_bytes = manufacturer_id.to_bytes(5, byteorder='big')
    terminal_model_bytes = terminal_model.encode('utf-8')
    terminal_id_bytes = terminal_id.encode('utf-8')
    license_plate_color_byte = license_plate_color.encode('utf-8')
    plate_number_bytes = plate_number.encode('utf-8')

    body = provincial_bytes + area_bytes + manufacturer_bytes + terminal_model_bytes + terminal_id_bytes + license_plate_color_byte + plate_number_bytes

    return body

def handle_registration_response(body):
    serial_number = body[0:2].decode('utf-8')
    bear_fruit = body[2:3].decode('utf-8')
    auth_code = body[3:17].decode('utf-8')
    return 

def handle_auth(body):
    serial_number = body[0:2].decode('utf-8')
    reply_id = body[0:2].decode('utf-8')
    auth_code = int.from_bytes(body[4:body.length-1], byteorder='big')
                               
def handle_information_distribution():
    message_id = 0x8300
    phone_number = ''
    sign = 0x0001
    text_info = 'this is text information!'
    response_data = sign.to_bytes(1, byteorder='big') + text_info.encode(1, "gbk")
    return construct_message(message_id, phone_number, response_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_location(deviceId, latitude, longitude, speed, direction, address, signal, door, mt2v_dc_volt):

    time_year = "24" # 24-04-12-15-20-33 date sample
    time_month = "04"
    time_day = "12"
    time_hour = "15"
    time_minute = "20"
    time_second = "33"
    deviceTime = (time_year + time_month + time_day + time_hour + time_minute + time_second).encode('utf-8')
    createAt = (time_year + time_month + time_day + time_hour + time_minute + time_second).encode('utf-8')
    updatedAt = (time_year + time_month + time_day + time_hour + time_minute + time_second).encode('utf-8')
    
    deviceId_bytes = deviceId.to_bytes(2, byteorder='little')
    latitude_bytes = struct.pack('<f', latitude)   # Pack latitude as 4-byte float
    longitude_bytes = struct.pack('<f', longitude) # Pack longitude as 4-byte float
    speed_bytes = speed.to_bytes(2, byteorder='little')
    direction_bytes = direction.to_bytes(1, byteorder='little')
    address_bytes = address.encode('utf-8')
    signal_bytes = signal.to_bytes(2, byteorder='little')
    door_bytes = door.to_bytes(2, byteorder='little')
    # Scale and convert decimal(10,1) to fit within 2-byte integer range
    mt2v_dc_volt_scaled = int(mt2v_dc_volt * 10)  # Scale by 10 to preserve 1 decimal place
    mt2v_dc_volt_bytes = mt2v_dc_volt_scaled.to_bytes(2, byteorder='little')
    
    data = deviceId_bytes + latitude_bytes + longitude_bytes + speed_bytes+ direction_bytes + address_bytes + signal_bytes + door_bytes + mt2v_dc_volt_bytes + deviceTime
    message_id = 0x0200
    # phone_number = ('1 625 521 4548').encode('utf-8')

    return construct_message(message_id, 16255214548, data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)
def handle_positions():
    
    alarm_std_bit = 0
    alarm_std_bit |= (1 << 7)
    alarm_flg = 1 # See the light alarm / remove the alarm
    alarm_std_bit &= (0xFF << alarm_flg)
    alarm_std_bit &= ~(0xFFFFFFFF << 9)
    warning_mark = alarm_std_bit

    acc_flag = 1 # 0 Acc Off 1 Acc On
    pos_flag = 1 # 0: Not positioned; 1: positioned
    status_flag = 0
    status_flag |= ( 1 << acc_flag)
    status_flag &= (0xFF << pos_flag)
    status_flag &= ~(0xFFFF << 30)

    latitude = 0xFFFF
    longitude = 0xFFFF
    altitude = 0xFFFF
    direction_value = 359 # 0 ~ 360'
    direction = direction_value & 0xFF
    time_year = "24" # 24-04-12-15-20-33 date sample
    time_month = "04"
    time_day = "12"
    time_hour = "15"
    time_minute = "20"
    time_second = "33"
    time = (time_year + time_month + time_day + time_hour + time_minute + time_second).encode('utf-8')
    response_data = warning_mark + status_flag + latitude + longitude+ altitude + direction + time
    message_id = 0x0200
    phone_number = ('1 625 521 4548').encode('utf-8')

    return construct_message(message_id, phone_number, response_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)
def handle_ad_voltage():

    default_pre = 0x0004
    instruction = 0x002D
    data = 12501

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = data.to_bytes(3, byteorder='little')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_battery_value():
    default_pre = 0x0004
    instruction = 0x002D
    data = 66.5 * 1500  # 66.5% battery

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = data.to_bytes(2, byteorder='little')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_version_information():
    data = bytes('59473032445F5436335F56302E373B',  'utf-8')
    default_pre = (len(data) + 2).to_bytes(2, byteorder='little')
    instruction = 0x002D
    
    shifted_instruction = instruction.to_bytes(2, byteorder='little')


    request_data = default_pre + shifted_instruction + data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_alarm_state():
    default_pre = 0x0006
    instruction = 0x0089
    data = bytes('FFFFFFFF', 'utf-8')

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')

    request_data = shifted_default_pre + shifted_instruction + data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_battery_value():
    default_pre = 0x0004
    instruction = 0x002D
    data = 12501

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = data.to_bytes(3, byteorder='little')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_base_station():
    default_pre = 0x0024
    instruction = 0x00A9
    country_num = (0x01CC).to_bytes(2, byteorder='little')
    operater_num = (0x00).to_bytes(1, byteorder='little')
    base_num = (0x01).to_bytes(1, byteorder='little')
    area_code = (0x262C).to_bytes(2, byteorder='little')
    tower_number = (0x04BA).to_bytes(2, byteorder='little')
    sign_intensity = (0x58).to_bytes(1, byteorder='little')

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')

    request_data = shifted_default_pre + shifted_instruction + country_num + operater_num + base_num + area_code + tower_number + sign_intensity 

    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_wifi_data():
    host_spot = 0x01
    wifi_format = '24:69:68:5d:2c:A5, -30'
    data = '12501'
    instruction = 0x00B9
    default_pre = (len(data) + 3 ).to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = host_spot.to_bytes(1, byteorder='little') + bytes(wifi_format, 'utf-8') + bytes(data, 'utf-8')

    request_data = default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_sim_iccid():
    default_pre = 0x000C
    instruction = 0x00B2
    data = '89860455161990868815' # 20 byte data

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = bytes(data, 'utf-8')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_location_status():
    default_pre = 0x0006
    instruction = 0x00C5
    data = '00001008'

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = bytes(data, 'utf-8')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_base_station():
    
    instruction = 0x0024
    data = '12501'
    default_pre = len(data) + 2

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = bytes(data, 'utf-8')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_base_station_4G():
    
    instruction = 0x00D8
    data = '12501'
    default_pre = len(data) + 2

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = bytes(data, 'utf-8')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_power_remain():
    default_pre = 0x0003    
    instruction = 0x00A8
    data = 0x64  # 100% charge

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = data.to_bytes(1, byteorder='little')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_voltage_value():
    default_pre = 0x0005
    instruction = 0x0004
    data = 292200  # means 2.92200 V

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')
    shifted_data = data.to_bytes(3, byteorder='little')

    request_data = shifted_default_pre + shifted_instruction + shifted_data 
    message_id = 0x0000
    phone_number = ''

    return construct_message(message_id, phone_number, request_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def startClient():
    messageID =  0x0100
    province_id = 1100
    city_id = 1201
    manu_id = '1D2A3'
    terminal_model = '0' * 20
    terminal_id = '0' * 7
    plate_color='0'
    plate_num = 'A-51-155'

    data = province_id.to_bytes(2,'little') + city_id.to_bytes(2,'little') + bytes(manu_id,'utf-8') +  bytes(terminal_model,'utf-8') + bytes(terminal_id,'utf-8') + bytes(plate_color,'utf-8') + bytes(plate_num,'utf-8')
    req_data = construct_message(messageID, 15856584, data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)
    # send_message("127.0.0.1", 1234, req_data)
    req_data_location = handle_location(1100, 24.4, 34.5, 1100, 10, 'aaaaa', 10, 10, 24);
    send_message("127.0.0.1", 5053, req_data_location);


startClient()