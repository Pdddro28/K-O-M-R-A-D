# --------------------libraries------------------------
import serial  # Manejo de comunicación serial
import time    # Gestión de retardos y tiempos de ejecución
# --------------------libraries------------------------

class MegaPiController:
    """
    Clase para el control remoto de MegaPi desde Raspberry Pi.
    Gestiona el empaquetado de datos y la temporización de movimientos.
    """

    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        """
        Constructor de la clase.
        Establece la conexión serial y aplica un retardo de seguridad.
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            # El Arduino suele reiniciarse al abrir la conexión serial
            time.sleep(2) 
            print(f"Conectado exitosamente a MegaPi en {port}")
        except Exception as e:
            print(f"Error crítico al conectar: {e}")
            exit()

    def _enviar_comando(self, accion, v1=0, v2=0):
        """
        Método privado para la construcción del paquete de protocolo.
        Paquete de 5 bytes: [Header, Tipo, Acción, Valor1, Valor2]
        """
        header = 0xFF
        tipo = 0x01
        package = bytearray([header, tipo, accion, v1, v2])
        self.ser.write(package)

    def avanzar(self, velocidad, duracion=None):
        """
        Envía comando para movimiento frontal.
        Si se define 'duracion', detiene el motor automáticamente tras n segundos.
        """
        print(f"Acción: Avanzar | Velocidad: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(1, v1=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def retroceder(self, velocidad, duracion=None):
        """
        Envía comando para movimiento hacia atrás.
        """
        print(f"Acción: Retroceder | Velocidad: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(2, v1=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def girar_izquierda(self, angulo, velocidad, duracion=None):
        """
        Ajusta el servo a la izquierda y activa motor de tracción.
        v1 = ángulo de dirección, v2 = velocidad del motor.
        """
        print(f"Acción: Girar Izq | Ángulo: {angulo} | Vel: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(3, v1=angulo, v2=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def girar_derecha(self, angulo, velocidad, duracion=None):
        """
        Ajusta el servo a la derecha y activa motor de tracción.
        """
        print(f"Acción: Girar Der | Ángulo: {angulo} | Vel: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(4, v1=angulo, v2=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def detenerse(self):
        """
        Detiene inmediatamente el motor y centra la dirección.
        """
        print("Acción: Detenerse")
        self._enviar_comando(5)

    def cerrar(self):
        """
        Cierra el puerto serial de forma segura.
        """
        if hasattr(self, 'ser') and self.ser.is_open:
            self.detenerse()
            self.ser.close()
            print("Conexión serial cerrada.")

# --------------------Main Execution--------------------
if __name__ == "__main__":
    # Inicialización del controlador
    # Nota: Verificar si el puerto es /dev/ttyUSB0 o /dev/ttyACM0
    carro = MegaPiController(port='/dev/ttyUSB0')

    try:
        # Ejemplo de secuencia: Giro programado de 4 segundos a 100 PWM
        carro.girar_derecha(angulo=45, velocidad=100, duracion=4)

        time.sleep(1) # Pausa de estabilización

        # Avance frontal por 2 segundos a velocidad media
        carro.avanzar(velocidad=150, duracion=2)

        print("Secuencia completada con éxito.")

    except KeyboardInterrupt:
        # Manejo de parada de emergencia con Ctrl+C
        if carro:
            carro.detenerse()
        print("\nControl interrumpido por el usuario.")
    
    finally:
        # Asegurar el cierre del puerto al finalizar
        if carro:
            carro.cerrar()
# --------------------Main Execution--------------------
