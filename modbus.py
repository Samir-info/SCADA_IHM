import serial
import time

requete = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x05, 0x85, 0xC9])

def envoyer_trame(port, baudrate, requete):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)

        ser.write(requete)
        time.sleep(0.1)

        reponse = ser.read(15)

        ser.close()

        return True, reponse

    except Exception as e:
        return False, e

def extraction_alarme(reponse):
    code = reponse[9]

    if code == 0:
        alarme = "NORMAL"
    elif code == 1:
        alarme = "ALARME"
    elif code == 2:
        alarme = "CRITIQUE"
    else:
        alarme = "INCONNU"

    return alarme

def extraction_critique(reponse):
    code = reponse[9]