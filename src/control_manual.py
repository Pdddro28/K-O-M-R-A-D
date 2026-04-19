import pygame
import sys
import time
import os
from megapi import MegaPi  # Asegúrate de instalarla con: pip install megapi

# Inicializar Pygame y su ventana
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("K-O-M-R-A-D Control")

# --- CONFIGURACIÓN DE PUERTOS ---
# En Raspberry Pi 4, el USB suele ser /dev/ttyUSB0
PORT = '/dev/ttyUSB0' 
SPEED = 100  # Rango 0 a 255

try:
    print(f"🔗 Conectando a MegaPi en {PORT}...")
    bot = MegaPi()
    bot.start(PORT) 
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    sys.exit()

def mover(izq, der):
    bot.motorRun(1, izq)
    bot.motorRun(2, der)

print("\n🚀 SISTEMA LISTO")
print("Usa WASD en la ventana de Pygame. ESC para salir.")

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        keys = pygame.key.get_pressed()
        
        # Lógica de Control WASD
        if keys[pygame.K_w]:
            print("  ⬆️  Adelante", end='\r')
            mover(SPEED, -SPEED) # Uno invertido dependiendo de la posición del motor
        elif keys[pygame.K_s]:
            print("  ⬇️  Atrás   ", end='\r')
            mover(-SPEED, SPEED)
        elif keys[pygame.K_a]:
            print("  ⬅️  Izquierda", end='\r')
            mover(-SPEED, -SPEED)
        elif keys[pygame.K_d]:
            print("  ➡️  Derecha  ", end='\r')
            mover(SPEED, SPEED)
        elif keys[pygame.K_ESCAPE]:
            raise KeyboardInterrupt
        else:
            mover(0, 0)
            print("  🛑  Detenido ", end='\r')

        time.sleep(0.02) # Respuesta rápida

except KeyboardInterrupt:
    print("\n\nDeteniendo K-O-M-R-A-D...")
finally:
    mover(0, 0)
    pygame.quit()
    sys.exit()