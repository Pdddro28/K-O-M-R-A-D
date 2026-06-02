import serial
import time

# --- CONFIGURATION ---
PORT = 'COM9' 
BAUDRATE = 115200

# --- SERIAL INTERFACE INITIALIZATION ---
try:
    arduino = serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=0.1)
    time.sleep(3) 
    
    if arduino.in_waiting > 0:
        greeting = arduino.read_all().decode('utf-8', errors='ignore')
        print(f"Arduino Boot Message: {greeting.strip()}")
        
    print(f"--- Successfully connected to {PORT} ---")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    exit()

# --- TRANSMISSION AND RECEPTION PROTOCOL ---
def send_command(text):
    if text.strip():
        arduino.write(f"{text}\n".encode('utf-8'))
        arduino.flush() 
        
        print(f"Tx -> Arduino: {text}")
        time.sleep(0.5) 
        
        while arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Rx <- Arduino: {line}")

# --- USER COMMAND INTERACTION ---
print("--- Control Console ---")
while True:
    user_input = input("Enter command > ") 
    if user_input.lower() == 'exit':
        break
    send_command(user_input)

# --- RESOURCE CLEANUP ---
arduino.close()
