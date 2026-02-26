import serial
import time

ser = serial.Serial('COM3', 115200, timeout = 1)
time.sleep(2) 

header = 0xFF   
tipo_de_comando = 1 
accion = 1   
arg1 = 100      
arg2 = 100      


#comando_txt = f"{tipo_de_comando}{accion}{arg1}{arg2}\n"
comando = bytes([header, tipo_de_comando, accion, arg1, arg2])

ser.write(comando)
print("Comando:", comando.hex())
#ser.write(comando_txt.encode('utf-8'))
#print(f"Enviado: {comando_txt.strip()}")

ser.close()
