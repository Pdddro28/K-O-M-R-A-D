from megapi import MegaPi
import time

if __name__ == '__main__':
    print("Iniciando...")
    bot = MegaPi()
    bot.start("COM3")
    time.sleep(1)  # Espera a que la conexión se estabilice

    print("Enviando comando al motor 2A...")
    bot.motorRun("2", 100)
    print("Motor debería estar en marcha")
    time.sleep(3)

    bot.motorRun("2A", 0)
    print("Motor detenido")