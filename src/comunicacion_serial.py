import serial
import time

class MegaPiController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):

        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2) # Espera para que el Arduino resetee al conectar
            print(f"Conectado exitosamente a MegaPi en {port}")
        except Exception as e:
            print(f"Error crítico al conectar: {e}")
            exit()

    def _enviar_comando(self, accion, v1=0, v2=0):

        header = 0xFF
        tipo = 0x01
        package = bytearray([header, tipo, accion, v1, v2])
        self.ser.write(package)

    def avanzar(self, velocidad, duracion=None):
        print(f"Acción: Avanzar | Velocidad: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(1, v1=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def retroceder(self, velocidad, duracion=None):
        print(f"Acción: Retroceder | Velocidad: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(2, v1=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def girar_izquierda(self, angulo, velocidad, duracion=None):
        print(f"Acción: Girar Izq | Ángulo: {angulo} | Vel: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(3, v1=angulo, v2=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def girar_derecha(self, angulo, velocidad, duracion=None):
        print(f"Acción: Girar Der | Ángulo: {angulo} | Vel: {velocidad} | Tiempo: {duracion}s")
        self._enviar_comando(4, v1=angulo, v2=velocidad)
        if duracion:
            time.sleep(duracion)
            self.detenerse()

    def detenerse(self):
        print("Acción: Detenerse")
        self._enviar_comando(5)

    def cerrar(self):
        self.detenerse()
        self.ser.close()
        print("Conexión serial cerrada.")

# --- Ejemplo de ejecución basado en tu petición ---
if __name__ == "__main__":
# Asegúrate de que el puerto sea el correcto (/dev/ttyUSB0 o /dev/ttyACM0)
    carro = MegaPiController(port='/dev/ttyUSB0')

    try:
# Ejemplo: Girar a la derecha con un ángulo de 45°,
# a una velocidad de 100 durante 4 segundos.
        carro.girar_derecha(angulo=45, velocidad=100, duracion=4)

        time.sleep(1) # Pausa de 1 segundo antes de la siguiente acción

# Ejemplo: Avanzar a 150 de velocidad por 2 segundos
        carro.avanzar(velocidad=150, duracion=2)

        print("Secuencia completada con éxito.")

    except KeyboardInterrupt:
        carro.detenerse()
        print("\nControl interrumpido por el usuario (Ctrl+C).")
    finally:
        carro.cerrar()
