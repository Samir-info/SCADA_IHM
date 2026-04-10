import tkinter as tk
import serial
import time

from main2 import requete

PORT = "COM6"
BAUDRATE = 9600

def EnvoyerRequete():
    #reponse = "01 03 00 00 00 05 85 00 31 00 02 00 02 6a 3c"
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    ser.write(requete)
    time.sleep(0.1)
    reponse = ser.read(15)
    print("Réponse HEX :", reponse.hex())
    ser.close()
    entry_reponse.delete(0, tk.END)
    entry_reponse.insert(0, reponse.hex())

fenetre = tk.Tk()
fenetre.title("IHM SCADA - BTS CIEL")
fenetre.geometry("600x400")

label_titre = tk.Label(fenetre,text="Supervision de la salle T/H/P",font=("Arial", 16))
label_titre.pack(pady=10)

frame_config = tk.LabelFrame(fenetre, text="Configuration", padx=10, pady=10)
frame_config.pack(fill="x", padx=10, pady=5)

label_ras = tk.Label(frame_config, text="RAS", bg="green", fg="white", width=5)
label_ras.pack(side="left", padx=5)

label_vitesse = tk.Label(frame_config, text="Vitesse de transmission")
label_vitesse.pack(side="left", padx=5)

entry_vitesse = tk.Entry(frame_config, width=8)
# noinspection PyTypeChecker
entry_vitesse.insert(0, BAUDRATE)
entry_vitesse.pack(side="left", padx=5)

label_port = tk.Label(frame_config, text="Port")
label_port.pack(side="left", padx=5)

entry_port = tk.Entry(frame_config, width=8)
entry_port.insert(0, PORT)
entry_port.pack(side="left", padx=5)

frame_requete = tk.LabelFrame(fenetre, text="Requete Modbus", padx=10, pady=10)
frame_requete.pack(fill="x", padx=10, pady=5)

label_requete = tk.Label(frame_requete, text="Requête")
label_requete.pack(side="left", padx=5)

entry_requete = tk.Entry(frame_requete, width=30)
entry_requete.insert(0, "01 03 00 00 00 05 85 c9")
entry_requete.pack(side="left", padx=5)

button_envoyer = tk.Button(frame_requete, text="Envoyer", command=EnvoyerRequete)
button_envoyer.pack(side="left", padx=5)

frame_donnees = tk.LabelFrame(fenetre, text="Données", padx=10, pady=10)
frame_donnees.pack(fill="x", padx=10, pady=5)

label_reponse = tk.Label(frame_donnees, text="Réponse")
label_reponse.pack(side="left", padx=5)

entry_reponse = tk.Entry(frame_donnees, width=40)
entry_reponse.pack(side="left", padx=5)

fenetre.mainloop()