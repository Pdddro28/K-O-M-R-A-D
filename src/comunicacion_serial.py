import serial
import time

ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2) 

header = 0xFF   
tipo_de_comando = 0x01 
accion = 0x02   
arg1 = 100      
arg2 = 100      

comando = bytes([header, tipo_de_comando, accion, arg1, arg2])

ser.write(comando)
print("Comando:", comando.hex())
ser.close()
