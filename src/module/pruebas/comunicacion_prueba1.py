import serial
import time

PUERTO = 'COM9' 

try:
    # Aumentamos el timeout a 0.1 para que no bloquee pero sea rápido
    arduino = serial.Serial(port=PUERTO, baudrate=115200, timeout=0.1)
    time.sleep(3) # Aumentamos a 3 segundos (algunas MegaPi tardan en reiniciar)
    
    # Limpiar buffer inicial (leer el "SISTEMA_LISTO")
    if arduino.in_waiting > 0:
        saludo = arduino.read_all().decode('utf-8', errors='ignore')
        print(f"Inicio Arduino: {saludo.strip()}")
        
    print(f"--- Conectado exitosamente a {PUERTO} ---")
except Exception as e:
    print(f"Error: {e}")
    exit()

def enviar_comando(texto):
    if texto.strip():
        # Enviamos y forzamos el vaciado del buffer de salida
        arduino.write(f"{texto}\n".encode('utf-8'))
        arduino.flush() 
        
        print(f"Saliendo hacia Arduino: {texto}")
        
        # Esperamos un poco más para que el hardware procese
        time.sleep(0.5) 
        
        # Intentamos leer varias líneas si las hay
        while arduino.in_waiting > 0:
            linea = arduino.readline().decode('utf-8', errors='ignore').strip()
            if linea:
                print(f"Arduino dice: {linea}")

print("--- Consola de Control ---")
while True:
    usuario = input("Escribe tu comando > ") 
    if usuario.lower() == 'salir':
        break
    enviar_comando(usuario)

arduino.close()