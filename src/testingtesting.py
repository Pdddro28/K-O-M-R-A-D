from mega_pi_controller import *
from constants import *
import cv2 
import time

# LNMbi setup
LNM = MegaPiController("/dev/ttyUSB0", 115200)

ROIS = [OPEN_ROI_CENTER, ROI_LINES]

states = {"straight": False, "girando": False}

running = True
loops = 0

# ==========================================
# VARIABLES Y CONSTANTES PARA EL PID
# ==========================================
TARGET_DIST = 30.0  # Distancia ideal a la pared
Kp = 1.5   
Ki = 0.0   
Kd = 0.8   

prev_error = 0.0
integral = 0.0
girando = False
conteo = False

# Temporizadores y banderas unificadas
color_timer = time.time()
time_lap = time.time()
n = 0

while running:
    try:
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        LNM.debug_UI()
        LNM.move_forward(speed = 75)  # Avanza siempre
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        
        # ==========================================
        # 1. DETECCIÓN AUTOMÁTICA DEL TIPO DE PISTA
        # ==========================================
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  # Pista Naranja (Gira a la derecha)
                print("¡Pista NARANJA detectada! Configurando giros a la derecha.")
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  # Pista Azul (Gira a la izquierda)
                print("¡Pista AZUL detectada! Configurando giros a la izquierda.")

        # ==========================================
        # 2. SISTEMA DE CENTRADO PID DINÁMICO
        # ==========================================
        if not girando and LNM.turning_direction != 0:
            
            # ASIGNACIÓN DINÁMICA SEGÚN LA PISTA
            if LNM.turning_direction == 2:    # Caso Naranja (Derecha)
                current_dist = min(left_dist, 60.0)   # Mira pared izquierda
                error = TARGET_DIST - current_dist
                lado_correccion = 1                   # Signo positivo (+) para ir a la derecha
            
            elif LNM.turning_direction == 1:  # Caso Azul (Izquierda)
                current_dist = min(right_dist, 60.0)  # Mira pared derecha
                error = TARGET_DIST - current_dist
                lado_correccion = -1                  # Signo negativo (-) para ir a la izquierda

            # Cálculo general del PID
            integral += error
            derivative = error - prev_error
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            # Aplicamos la corrección (sumando o restando dinámicamente)
            steering_angle = int(80 + (correction * lado_correccion))
            
            # Limitamos el ángulo del servo
            steering_angle = max(40, min(120, steering_angle))
            
            # Ejecución de movimiento
            if abs(error) < 2:
                LNM.turn_center()
            elif steering_angle > 85:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 75:
                LNM.turn_left(angle=steering_angle, speed=50)

        # ==========================================
        # 3. LÓGICA DE ESQUINAS Y CONTEO DE VUELTAS
        # ==========================================
        current_time = time.time()
        
        # Seleccionamos el área actual que nos interesa monitorear
        area_actual = LNM.orange_area if LNM.turning_direction == 2 else LNM.blue_area

        # Filtro para evitar múltiples detecciones en la línea de la pista activa
        if LNM.turning_direction != 0 and area_actual > 500 and n == 0: 
            color_timer = current_time
            n = 1
            loops += 1
            print(f"Línea detectada. Vueltas: {loops}")

        # Reset del temporizador de bloqueo (3 segundos)
        if current_time - color_timer > 3: 
            n = 0

        # Control de curvas (Funciona igual para ambos lados usando LNM.turn_direction())
        if front_dist < 80 and not girando and LNM.black_area > 9000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 100:
            LNM.turn_center()
            girando = False
            conteo = False

        if loops == 12:
            print("¡Carrera terminada! 12 vueltas completadas.")
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

LNM.stop()
