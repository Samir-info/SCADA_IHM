import serial
import time

PORT ="COM6"
BAUDRATE = 9600

requete = bytes([0x01,0x03,0x00,0x00,0x00,0x05,0x85,0xC9])

ser = serial.Serial(PORT, BAUDRATE, timeout=1)

ser.write(requete)

time.sleep(0.1)

reponse = ser.read(15)

print("Réponse HEX :", reponse.hex())

ser.close()
print("Adresse esclave :", reponse[0])
print("Code fonction :", reponse[1])
print("Nombre d'octets de données :", reponse[2])
print("----- ETAT SYTEME -----")
octet_fort = reponse[3]
octet_faible = reponse[4]
temperature_brute = (octet_fort << 8) | octet_faible
temperature_c = temperature_brute / 10
print("Température :", temperature_c, "°C")

octet_fort = reponse[5]
octet_faible = reponse[6]
pression_brute = (octet_fort << 8) | octet_faible
print("Pression :", pression_brute, "hPa")

octet_fort = reponse[7]
octet_faible = reponse[8]
humidite_brute = (octet_fort << 8) | octet_faible
print("Humidité :", humidite_brute, "%")

alarm_code = reponse[9]
if alarm_code == 0:
    etat_alarme = "NORMAL"
elif alarm_code == 1:
    etat_alarme = "ALARME"
elif alarm_code == 2:
    etat_alarme = "CRITIQUE"
else:
    etat_alarme = "INCONNU"
print("État de l'alarme :", etat_alarme)
print("-----------------------")
