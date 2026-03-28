import pygame
import sys
import time
from mega_pi_controller import MegaPiController

# Inicializar Pygame
pygame.init()
pygame.display.set_mode((400, 400))
pygame.display.set_caption("🎮 Control Manual - MegaPi Car")
print("🎮 Control Manual Iniciado. Usa W,A,S,D para mover. ESC para salir.")

try:
    car = MegaPiController(port='COM5')
except Exception as e:
    print(f"❌ Error conectando al carro: {e}")
    sys.exit()

KEY_FORWARD = pygame.K_w
KEY_BACKWARD = pygame.K_s
KEY_LEFT = pygame.K_a
KEY_RIGHT = pygame.K_d

SPEED = 100
STEERING_ANGLE = 45

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise KeyboardInterrupt

        keys = pygame.key.get_pressed()

        if keys[KEY_LEFT]:
            print("   ⬅️  Turn Left", end='\r')
            car.turn_left(angle=STEERING_ANGLE, speed=SPEED, log=False)
        elif keys[KEY_RIGHT]:
            print("   ➡️  Turn Right", end='\r')
            car.turn_right(angle=STEERING_ANGLE, speed=SPEED, log=False)

        if keys[KEY_FORWARD]:
            print("   ⬆️  Forward   ", end='\r')
            car.move_forward(speed=SPEED, log=False)
        elif keys[KEY_BACKWARD]:
            print("   ⬇️  Backward  ", end='\r')
            car.move_backward(speed=SPEED, log=False)
        else:
            car.stop(log=False)
            print("   🛑  Stopped   ", end='\r')

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\n⛔ Control terminado por el usuario.")
finally:
    car.close()
    pygame.quit()
    sys.exit()