from mega_pi_controller import *
from constants import *
import cv2 
import time

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

ROIS = [OPEN_ROI_CENTER, ROI_LINES]

states = {"straight": False, "girando": False}

running = True
loops = 0

orange_timer = time.time()
blue_timer = time.time()
time_lap = time.time()
n = 0

# --- PID CONTROLLER VARIABLES ---
TARGET_DIST = 22.0  
Kp = 3.1    
Ki = 0.0   
Kd = 0.2   

prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 
girando = False
conteo = False

# --- CONFIGURACIÓN DEL FRENO DE MANO DE EMERGENCIA ---
DIST_MIN_CHOQUE = 20.0  # Umbral de distancia frontal en cm para activar la reversa
steering_angle = 80     # Variable para recordar el último ángulo físico enviado por el PID

# --- TIMERS AND FLAGS ---
color_timer = time.time()

# --- MAIN CONTROL LOOP ---
while running:
    try:
        # Sensors and data acquisition
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        LNM.debug_UI()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        print(f"Turning: {LNM.turning_direction}, black_area: {LNM.black_area}, blue_area: {LNM.blue_area}, orange_area: {LNM.orange_area}")
        print(f"Distances - Front: {front_dist:.2f} cm, Left: {left_dist:.2f} cm, Right: {right_dist:.2f} cm")

        # =========================================================================
        # FRENO DE MANO DE EMERGENCIA (Si está a punto de chocar de frente)
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
            print(f"🚨 ¡FRENO DE MANO! Frente obstruido a {front_dist:.2f} cm.")
            
            # Detenemos de golpe los motores llamando al stop nativo
            LNM.stop(log=False)
            time.sleep(0.05) # Breve pausa inercial
            
            # Calcular ángulo opuesto en espejo respecto al centro físico (80)
            angulo_escape_opuesto = 160 - steering_angle
            angulo_escape_opuesto = max(40, min(120, angulo_escape_opuesto))
            
            # Si el robot iba completamente derecho, rompemos el eje hacia la izquierda por seguridad
            if angulo_escape_opuesto == 80:
                angulo_escape_opuesto = 60
                
            print(f"Ángulo previo: {steering_angle} | Pivotando hacia atrás con ángulo: {angulo_escape_opuesto}")
            
            # Usamos tu nuevo método modificado de la clase base
            LNM.move_backward(angle=angulo_escape_opuesto, speed=55)
            time.sleep(0.75)  # Tiempo de retroceso para limpiar la trompa del muro
            
            # Enderezamos ruedas y limpiamos las acumulaciones del PID para evitar arrancar torcido
            LNM.turn_center(log=False)
            prev_error = 0.0
            integral = 0.0
            time.sleep(0.1)
            
            continue  # Salta el ciclo actual para reiniciar la marcha adelante con espacio nuevo

        # Si el frente está despejado, marcha adelante normal
        LNM.move_forward(speed = 60) 

        # 1. TRACK TYPE DETECTION
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # 2. CORNER DETECTION (ESQUINAS)
        if front_dist < 55 and not girando and LNM.black_area > 11000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 100:
           LNM.turn_center()
           girando = False
           conteo = False
           steering_angle = 80

        # NAVEGACIÓN EN RECTAS MEDIANTE SEGUIMIENTO DE PAREDES (PID)
        if not girando and LNM.turning_direction != 0:
            
            # Pista Naranja: Sigue pared IZQUIERDA. 
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                error = TARGET_DIST - current_dist  
                lado_correccion = 1                 
            
            # Pista Azul: Sigue pared DERECHA.
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                error = TARGET_DIST - current_dist  
                lado_correccion = -1                
            
            # Cálculo de la parte integral con filtro anti-windup incorporado
            integral += error
            integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
            
            derivative = error - prev_error
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            # Modificación de dirección
            steering_angle = int(80 + (correction * lado_correccion))
            steering_angle = max(40, min(120, steering_angle))
            
            # --- ACTUACIÓN DE LOS MOTORES ---
            if abs(error) < 1.5: 
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)


        # 3. CORNER LOGIC AND LAP COUNTER
        current_time = time.time()

        if LNM.orange_area > 500 and n == 0 and LNM.turning_direction == 2: 
            orange_timer = current_time
            n = 1
            loops += 1

        if LNM.blue_area > 500 and n == 0 and LNM.turning_direction == 1: 
            blue_timer = current_time
            n = 1
            loops += 1

        if current_time - orange_timer > 4 and LNM.turning_direction == 2: 
            n = 0
            print("Timer reset, ready for next orange line detection.")

        if current_time - blue_timer > 4 and LNM.turning_direction == 1:
            n = 0
            print("Timer reset, ready for next blue line detection.")

        print("Loop count:", loops)

        if loops == 12:
            LNM.turn_direction()
            time.sleep(3)
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()