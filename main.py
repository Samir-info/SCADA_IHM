from machine import Pin, UART
import time
import random

SLAVE_ID = 1
LED_PIN = 15

led = Pin(LED_PIN, Pin.OUT)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

temperature = 250      # 25.0 °C
pressure = 1013        # mbar
humidity = 50          # %

statusWord = 0
alarmCode = 0

coilLed = False
faultMode = False

# mémorisation de l'alarme
alarmLatched = False

# ===== CRC =====
def modbus_crc(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc

def send_frame(data):
    crc = modbus_crc(data)
    uart.write(data + bytes([crc & 0xFF, crc >> 8]))

# ===== SIMULATION =====
cycle = 0

def simulate_sensor():
    global temperature, pressure, humidity
    global statusWord, alarmCode, cycle
    global faultMode, alarmLatched

    cycle += 1

    # ===== PHASE 1 : fonctionnement normal =====
    if cycle < 60:
        temperature = 240 + random.randint(-5, 5)

    # ===== PHASE 2 : dérive thermique =====
    elif cycle < 120:
        temperature += 2

    # ===== PHASE 3 : refroidissement =====
    else:
        temperature -= 1
        if cycle > 180:
            cycle = 0

    # ===== Mode défaut forcé pour le TP =====
    if faultMode:
        temperature = 330   # 33.0 °C

    pressure = 1000 + random.randint(0, 20)
    humidity = 45 + random.randint(0, 15)

    # ===== Détection alarme mémorisée =====
    if temperature > 320:
        alarmCode = 2
        statusWord = 0x0002
        alarmLatched = True

    elif temperature > 300 and not alarmLatched:
        alarmCode = 1
        statusWord = 0x0001
        alarmLatched = True

# ===== REGISTRES =====
def get_register(addr):
    if addr == 0:
        return temperature
    if addr == 1:
        return pressure
    if addr == 2:
        return humidity
    if addr == 3:
        return statusWord
    if addr == 4:
        return alarmCode
    return 0

print("Capteur environnemental Modbus prêt")

while True:
    simulate_sensor()

    if uart.any():
        time.sleep_ms(10)
        frame = uart.read()

        if not frame or len(frame) < 8:
            continue

        if frame[0] != SLAVE_ID:
            continue

        function = frame[1]

        # ===== READ HOLDING REGISTERS (0x03) =====
        if function == 3:
            addr = (frame[2] << 8) | frame[3]
            qty = (frame[4] << 8) | frame[5]

            resp = bytearray()
            resp.append(SLAVE_ID)
            resp.append(3)
            resp.append(qty * 2)

            for i in range(qty):
                val = get_register(addr + i)
                resp.append(val >> 8)
                resp.append(val & 0xFF)

            send_frame(resp)

        # ===== WRITE SINGLE COIL (0x05) =====
        elif function == 5:
            addr = (frame[2] << 8) | frame[3]
            value = (frame[4] << 8) | frame[5]

            state = (value == 0xFF00)

            # Coil 0 : LED
            if addr == 0:
                coilLed = state
                led.value(coilLed)

            # Coil 1 : reset manuel de l'alarme
            if addr == 1 and state:
                alarmCode = 0
                statusWord = 0
                alarmLatched = False

            # Coil 2 : forçage d'un défaut thermique
            if addr == 2:
                faultMode = state

            # Echo de la trame d'écriture
            send_frame(frame[:6])

    time.sleep_ms(500)