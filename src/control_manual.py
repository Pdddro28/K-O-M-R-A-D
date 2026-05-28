import pygame
import sys
import time
import os
from megapi import MegaPi 

# --- WINDOW INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("K-O-M-R-A-D Control")

# --- MEGAPI CONNECTION CONFIGURATION ---
PORT = '/dev/ttyUSB0' 
SPEED = 100 

try:
    print(f"🔗 Conectando a MegaPi en {PORT}...")
    bot = MegaPi()
    bot.start(PORT) 
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    sys.exit()

# --- LOW-LEVEL LOCOMOTION ACTUATORS ---
def mover(izq, der):
    bot.motorRun(1, izq)
    bot.motorRun(2, der)

print("\n🚀 SISTEMA LISTO")
print("Usa WASD en la ventana de Pygame. ESC para salir.")

# --- TELEOPERATION CONTROL LOOP ---
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            print("  ⬆️  Adelante", end='\r')
            mover(SPEED, -SPEED) 
        elif keys[pygame.K_s]:
            print("  ⬇️  Atrás   ", end='\r')
            mover(-SPEED, SPEED)
        elif keys[pygame.K_a]:
            print("  ⬅️  Izquierda", end='\r')
            mover(0, -SPEED) 
        elif keys[pygame.K_d]:
            print("  ➡️  Derecha  ", end='\r')
            mover(SPEED, 0)
        elif keys[pygame.K_ESCAPE]:
            raise KeyboardInterrupt
        else:
            mover(0, 0)
            print("  🛑  Detenido ", end='\r')

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\n\nDeteniendo K-O-M-R-A-D...")
finally:
    # --- RESOURCE CLEANUP ---
    mover(0, 0)
    pygame.quit()
    sys.exit()
