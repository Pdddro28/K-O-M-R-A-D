from mega_pi_controller import *
from constants import *
import cv2 

# LNMbi setup
LNM = MegaPiController("/dev/ttyUSB0", 115200)

ROIS = [OPEN_ROI_CENTER, ROI_LINES]

states = {"straight": False, "girando": False}

running = True
loops = 0

# ==========================================
# VARIABLES Y CONSTANTES PARA EL PID
# ==========================================
TARGET_DIST = 30.0  # La distancia ideal que queremos mantener de la pared
Kp = 1.5   # Proporcional: Que tan fuerte reacciona al error actual
Ki = 0.0   # Integral: Corrige desviaciones constantes (dejalo en 0 por ahora)
Kd = 0.8   # Derivativo: Predice y suaviza el movimiento (evita el zig-zag)

prev_error = 0.0
integral = 0.0

conteo = False

while running:
    try:
        LNM.move_forward(speed = 75)  # Avanza siempre
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()

        front_dist, left_dist, right_dist = LNM.get_distances()

        # 1. Obtener direcci�n general de giro de la pista
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # ==========================================
        # 2. SISTEMA DE CENTRADO PID (Solo en rectas)
        # ==========================================
        if not states["girando"] and LNM.turning_direction == 2:
            # Calculamos el error. 
            # Si left_dist < 25 (ej. 15): error es +10 (muy cerca, hay que alejarse)
            # Si left_dist > 25 (ej. 35): error es -10 (muy lejos, hay que acercarse)
            # Limitamos la lectura m�xima a 60 para evitar que el sensor se vuelva loco si no hay pared
            current_dist = min(left_dist, 60.0)
            
            error = TARGET_DIST - current_dist 
            integral += error
            derivative = error - prev_error
            
            # Ecuaci�n PID
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            # Asumiendo que 80 es el centro del servo, 120 es derecha m�xima, 40 izquierda m�xima.
            # Si error es positivo (+), sumamos al centro para que gire a la derecha.
            steering_angle = int(80 + correction)
            
            # Limitamos el �ngulo para no forzar la direcci�n
            steering_angle = max(40, min(120, steering_angle))
            
            # Zona muerta (Deadband): Si el error es m�nimo (�2 cm), mantenemos el centro
            if abs(error) < 2:
                LNM.turn_center()
            elif steering_angle > 85:
                # Gira a la derecha suavemente
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 75:
                # Gira a la izquierda suavemente
                LNM.turn_left(angle=steering_angle, speed=50)

        # ==========================================
        # 3. LOGICA DE ESQUINAS Y VUELTAS
        # ==========================================
        if right_dist > 100 and girando and conteo == False:
            loops += 1
            conteo = True

        if front_dist < 80 and not girando and LNM.black_area > 9000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            # Reset de las variables PID al entrar a una curva para evitar latigazos en la siguiente recta
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 100:
           LNM.turn_center()
           girando = False
           conteo = False

        print("Loop count:", loops)

            
        if loops == 13 and LNM.black_area < 6000 and front_dist  < 100 :
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

LNM.stop()