import serial
import time
import threading

class KomradAutonomous:
    def __init__(self, port='/dev/ttyUSB9', baudrate=115200):
        try:
            # Configuración Serial
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            time.sleep(2)  # Espera a que Arduino reinicie
            
            # Variables de estado
            self.dist_front = 400
            self.dist_left = 400
            self.dist_right = 400
            self.button_pressed = False
            self.running = True
            
            # Iniciar hilo de telemetría
            self.reader_thread = threading.Thread(target=self._read_telemetry, daemon=True)
            self.reader_thread.start()
            print(f"Conectado a MegaPi en {port}")

        except Exception as e:
            print(f"Error de conexión: {e}")
            exit()

    def _read_telemetry(self):
        """Lee y sincroniza los datos del Arduino (Header 0xAA + 5 bytes)"""
        while self.running:
            if self.ser.in_waiting >= 6:
                header = self.ser.read(1)
                if header == b'\xaa':
                    payload = self.ser.read(5)
                    self.dist_front = payload[0]
                    self.dist_left = payload[1]
                    self.dist_right = payload[2]
                    self.button_pressed = (payload[3] == 1)
            time.sleep(0.01)

    def _send(self, action, v1=0, v2=0):
        """Protocolo [0xFF, 0x01, Acción, Val1, Val2]"""
        package = bytearray([0xFF, 0x01, action, v1, v2])
        self.ser.write(package)

    # --- Comandos de Movimiento ---
    def avanzar(self, velocidad):
        self._send(1, velocidad)

    def detener(self):
        self._send(5)

    def girar_izquierda(self, angulo, velocidad):
        self._send(3, angulo, velocidad)

    def girar_derecha(self, angulo, velocidad):
        self._send(4, angulo, velocidad)

    def centrar_direccion(self):
        self._send(6)

    def cerrar(self):
        self.running = False
        self.detener()
        self.ser.close()

# --- Lógica de Control ---
def loop_principal():
    robot = KomradAutonomous(port='COM9') # Cambiar a /dev/ttyUSB0 en Raspberry

    # Umbrales de distancia (en cm)
    PARE_FRONTAL = 30    # Distancia para detenerse y buscar salida
    ALERTA_LATERAL = 15  # Distancia para corregir rumbo
    VEL_BASE = 120    # Velocidad normal
    VEL_GIRO = 100       # Velocidad al rotar

    try:
        print("\n Esperando pulsación del botón para iniciar...")
        while not robot.button_pressed:
            time.sleep(0.1)

        print("Navegación autónoma activada.")
        
        while True:
            f, l, r = robot.dist_front, robot.dist_left, robot.dist_right
            print(f"Sensores -> F:{f:3} | L:{l:3} | R:{r:3}", end='\r')

            # 1. Obstáculo de frente: Decisión de giro
            if f < PARE_FRONTAL:
                robot.detener()
                time.sleep(0.3)
                
                # Decidir hacia dónde girar basándose en el lado con más espacio
                if l > r:
                    print("\nObstáculo detectado: Girando a la IZQUIERDA")
                    robot.girar_izquierda(45, VEL_GIRO)
                else:
                    print("\nObstáculo detectado: Girando a la DERECHA")
                    robot.girar_derecha(45, VEL_GIRO)
                
                time.sleep(0.6) # Tiempo para completar la rotación
                robot.centrar_direccion()

            # 2. Corrección lateral izquierda (se está pegando mucho a la pared izq)
            elif l < ALERTA_LATERAL:
                robot.girar_derecha(15, VEL_BASE)
            
            # 3. Corrección lateral derecha (se está pegando mucho a la pared der)
            elif r < ALERTA_LATERAL:
                robot.girar_izquierda(15, VEL_BASE)

            # 4. Camino despejado
            else:
                robot.avanzar(VEL_BASE)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n Deteniendo sistema...")
    finally:
        robot.cerrar()

if __name__ == "__main__":
    loop_principal()
