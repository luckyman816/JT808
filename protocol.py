import struct
from utilities import bcd_encode, escape, unescape, calculate_check_code, bcd_decode
from encryption import rsa_encrypt, rsa_decrypt

def parse_message(data, private_key=None):
    realdata = data[2:-1]
    print(realdata)
    data = unescape(realdata)
    header_format = '>HH6sH'
    header_basic_length = struct.calcsize(header_format)
    
    header = data[:header_basic_length]
    body = data[header_basic_length:-1]
    check_code = data[-1]

    # Verify the check code
    print(calculate_check_code(data))

    # Unpack the basic header
    message_id, body_props, phone_number_bcd, serial_number = struct.unpack(header_format, header)
    phone_number = bcd_decode(phone_number_bcd)

    if check_code != calculate_check_code(data[:-1]):
        raise ValueError("Invalid check code")

    return {
        'message_id': message_id,
        'phone_number': phone_number,
        'body': body,
        'serial_number': serial_number
    }

def construct_message(message_id, phone_number, body, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1):
    if encryption_method and public_key:
        body = rsa_encrypt(public_key, body)
    # else:
    #     body = body.encode('utf-8')
    body_length = len(body)

    body_props = (encryption_method << 10) | (len(body) & 0x3FF)

    phone_number_bcd = bcd_encode(phone_number)
    header_format = '>HH6sH'
    if is_subpackage:
        header_format += 'HH'
    header = struct.pack(header_format, message_id, body_props, phone_number_bcd, serial_number)
    message = header + body
    check_code = calculate_check_code(message)
    print(check_code)
    print(escape(message + struct.pack('B', check_code)))
    return escape(b'\x7e' + message + struct.pack('B', check_code) + b'\x7e')
