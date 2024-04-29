import struct

def pack_general_response(answer_serial_number, reply_id, result):
    return struct.pack('>HHB', answer_serial_number, reply_id, result)

def pack_terminal_heartbeat():
    return b''

def pack_terminal_registration(provincial_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, plate_number):
    manufacturer_id_encoded = manufacturer_id.encode('ascii').ljust(5, b'\x00')
    terminal_model_encoded = terminal_model.encode('ascii').ljust(20, b'\x00')
    terminal_id_encoded = terminal_id.encode('ascii').ljust(7, b'\x00')

    body = struct.pack('>HH', provincial_id, city_id)
    body += manufacturer_id_encoded + terminal_model_encoded + terminal_id_encoded
    body += struct.pack('>B', license_plate_color)

    if license_plate_color == 0:
        body += plate_number.encode('GBK')
    else:
        body += plate_number.encode('GBK')

    return body

def pack_terminal_registration_response(answer_serial_number, result, auth_code=''):
    body = struct.pack('>HHB', answer_serial_number, result, len(auth_code))
    body += auth_code.encode('ascii')
    return body

def pack_terminal_cancellation():
    return b''

def pack_terminal_authentication(auth_code):
    return auth_code.encode('ascii')

def pack_location_info_report(warning_mark, status_flag, latitude, longitude, altitude, velocity, direction, timestamp):
    body = struct.pack('>IIIIHHH6s', warning_mark, status_flag, latitude, longitude, altitude, velocity, direction, timestamp)
    return body

def pack_single_base_station(country_code, operator_number, base_station_number, area_code, tower_number, signal_strength):
    body = struct.pack('>HHBHHB', country_code, operator_number, base_station_number, area_code, tower_number, signal_strength)
    return body