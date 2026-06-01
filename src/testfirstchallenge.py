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
TARGET_DIST = 30.0
Kp = 1.5
Ki = 0.0
Kd = 0.8

prev_error = 0.0
integral = 0.0
girando = False
conteo = False
orange_timer = time.time()
time_lap = time.time()
n = 0
while running:
    try:
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        #LNM.debug_UI()
        LNM.move_forward(speed = 75)  # Avanza siempre
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

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
        if not girando and LNM.turning_direction == 2:
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
        current_time = time.time()
        print(LNM.orange_area)

        if LNM.orange_area > 500 and n == 0 :  # Evitamos múltiples detecciones de la misma línea naranja
            orange_timer = current_time
            n = 1
            loops += 1

        if current_time - orange_timer > 3:  # Reiniciamos el contador después de 1 segundo
            n = 0
            print("Timer reset, ready for next orange line detection.")

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


        if loops == 12:
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

LNM.stop()
