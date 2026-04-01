def calcul_crc(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b 
        for _ in range(8):  
            if crc & 0x0001:  
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc

requete_sans_crc = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x05])
crc = calcul_crc(requete_sans_crc)
print("CRC calculé =", hex(crc))