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

# --- PID CONTROLLER VARIABLES (Ajustados para mayor suavidad) ---
TARGET_DIST = 30.0  
Kp = 1.8    # Incrementado ligeramente para reaccionar más rápido
Ki = 0.01   # Se añade una pizca de integral para eliminar el error estático
Kd = 1.2    # Incrementado para amortiguar oscilaciones bruscas

prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 # Anti-windup para evitar que el robot se vuelva loco
girando = False
conteo = False

# --- TIMERS AND FLAGS ---
color_timer = time.time()
time_lap = time.time()
n = 0

# --- MAIN CONTROL LOOP ---
while running:
    try:
        # Sensors and data acquisition
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        LNM.debug_UI()
        LNM.move_forward(speed = 50)  
        
        # Emergency break condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        
        # 1. AUTOMATIC TRACK TYPE DETECTION
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  
                print("¡Pista NARANJA detectada! Configurando giros a la derecha.")
            elif LNM.blue_area > 900:
                LNM.turning_direction = 1  
                print("¡Pista AZUL detectada! Configurando giros a la izquierda.")

        # 2. DYNAMIC PID WALL-CENTERING SYSTEM
        if not girando and LNM.turning_direction != 0:
            
            # Pista Naranja: Sigue pared IZQUIERDA. 
            # Si se acerca a la pared (dist < 30), debe ir a la Derecha.
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                error = TARGET_DIST - current_dist  # Error (+) si está muy cerca
                lado_correccion = 1                 # (+) -> Derecha, (-) -> Izquierda
            
            # Pista Azul: Sigue pared DERECHA.
            # Si se acerca a la pared (dist < 30), debe ir a la Izquierda.
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                error = TARGET_DIST - current_dist  # Error (+) si está muy cerca
                lado_correccion = -1                # (+) -> Izquierda, (-) -> Derecha

            # PID Math calculations
            integral += error
            # Anti-windup: Limitamos la integral para que no sature los motores
            integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
            
            derivative = error - prev_error
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            # El centro físico o neutral del servo es 80
            # Aplicamos la corrección con la dirección correspondiente
            steering_angle = int(80 + (correction * lado_correccion))
            
            # Restringimos el ángulo entre los límites seguros de tu robot (40 y 120)
            steering_angle = max(40, min(120, steering_angle))
            
            # --- CORRECCIÓN MEJORADA EN AMBOS SENTIDOS ---
            # Si el error es mínimo, va recto.
            if abs(error) < 1.5: 
                LNM.turn_center()
            # Si el ángulo es mayor que el centro, físicamente cruza a la derecha
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            # Si el ángulo es menor que el centro, físicamente cruza a la izquierda
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

        # 3. CORNER LOGIC AND LAP COUNTER
        current_time = time.time()
        
        area_actual = LNM.orange_area if LNM.turning_direction == 2 else LNM.blue_area

        # Active track line detection filter
        if LNM.turning_direction != 0 and area_actual > 500 and n == 0: 
            color_timer = current_time
            n = 1
            loops += 1
            print(f"Línea detectada. Vueltas: {loops}")

        # Debounce timer reset (3 seconds lockout)
        if current_time - color_timer > 3: 
            n = 0

        # Cornering handling execution
        if front_dist < 80 and not girando and LNM.black_area > 9000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 100:
            LNM.turn_center()
            girando = False
            conteo = False

        # Race finish condition
        if loops == 18:
            print("¡Carrera terminada! 18 vueltas completadas.")
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()