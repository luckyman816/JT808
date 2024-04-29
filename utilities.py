import struct

def bcd_encode(number, length=6):
    bcd_str = ''
    while number > 0:
        digit = number % 10
        number //= 10
        bcd_str = f"{digit:01x}" + bcd_str
    bcd_str = bcd_str.zfill(length)
    if len(bcd_str) % 2 != 0:
        bcd_str = '0' + bcd_str  # Pad to ensure even length for byte conversion
    return bytes.fromhex(bcd_str)


def bcd_decode(bcd_bytes):
    number = 0
    for byte in bcd_bytes:
        number = number * 100 + ((byte >> 4) * 10) + (byte & 0x0F)
    return number

def escape(data):
    escaped_data = bytearray()
    for byte in data:
        if byte == 0x7e:
            escaped_data.extend(b'\x7d\x02')
        elif byte == 0x7d:
            escaped_data.extend(b'\x7d\x01')
        else:
            escaped_data.append(byte)
    return bytes(escaped_data)

def unescape(data):
    unescaped_data = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0x7d:
            if i + 1 < len(data):  # Ensure there is a byte to follow the escape character
                if data[i + 1] == 0x01:
                    unescaped_data.append(0x7d)
                elif data[i + 1] == 0x02:
                    unescaped_data.append(0x7e)
                i += 2
            else:
                i += 2
                print("Warning: Data ends with an incomplete escape sequence.")
        else:
            unescaped_data.append(data[i])
            i += 1
    return bytes(unescaped_data)



def calculate_check_code(data):
    check_code = 0
    for byte in data:
        check_code ^= byte
    return check_code