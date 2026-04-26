import serial
from time import sleep

# 0 - dot
# 1 - bottom right
# 2 - bottom
# 3 - bottom left
# 4 - center
# 5 - top left
# 6 - top
# 7 - top right
#
# #666#
# 5   7
# 5   7
# #444#
# 3   1
# 3   1
# #222#
#        0

seven_segment_data = {
    0: 0b00010001,
    1: 0b01111101,
    2: 0b00100011,
    3: 0b11010111,
    4: 0b01001101,
    5: 0b10001001,
    6: 0b10000001,
    7: 0b00111101,
    8: 0b00000001,
    9: 0b00001001
}

def write_byte_raw(ser: serial.Serial, addr: int, data: int):
    data_bytes = f"{str(addr)} {str(data)}\n".encode()
    ser.write(data_bytes)

def wait(ser: serial.Serial):
    while True:
        msg = ser.readline().decode(errors="ignore").strip()

        if not msg:
            ser.close()
            raise IOError("Timed out")

        if "Enter address and data:" in msg:
            break

def write_byte(ser: serial.Serial, addr: int, data: int):
    sleep(0.1)
    wait(ser)
    write_byte_raw(ser, addr, data)
    wait(ser)
    write_byte_raw(ser, addr, data)

def write(data: dict[int, int], port="COM5"):
    with serial.Serial(port, 115200, timeout=3) as ser:
        if not ser.is_open:
            ser.open()

        sleep(1)

        print("[PY] Opened: ", ser)

        l = len(data.keys())
        i = 0

        for byte in data.keys():
            i += 1
            print(f"[PY] Writing... [{i}/{l}]")
            write_byte(ser, byte, data[byte])

        print("[PY] Finished!")

if __name__ == "__main__":
    write(seven_segment_data)
