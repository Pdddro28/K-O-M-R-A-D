from mega_pi_controller import *
from constants import *
import cv2 
import time

# --- INITIALIZATION AND CONFIGURATION ---
LNM = ("/dev/ttyUSB0", 115200)

ROIS = [OPEN_ROI_CENTER, ROI_LINES]

states = {"straight": False, "girando": False}

running = True
loops = 0

# --- PID CONTROLLER VARIABLES (WALL CENTERING) ---
TARGET_DIST = 30.0  
Kp = 1.5   
Ki = 0.0   
Kd = 0.8   

prev_error = 0.0
integral = 0.0
girando = False
conteo = False

# --- OBSTACLE EVASION CONFIGURATION ---
# Umbral de área para considerar que un obstáculo está lo suficientemente cerca para esquivarlo
UMBRAL_OBSTACULO = 1500  
tiempo_esquiva = 0.0
esquivando = False

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
        
        # --- NUEVAS DETECCIONES PARA OBSTÁCULOS ---
        # Se asume que tu controlador tiene implementadas estas funciones de visión
        LNM.obtener_obstaculo_rojo()    
        LNM.obtener_obstaculo_verde()   
        
        LNM.debug_UI()
        
        # Velocidad base por defecto (si no está esquivando o girando fuerte)
        velocidad_actual = 75
        LNM.move_forward(speed = velocidad_actual)  
        
        # Emergency break condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        
        # 1. AUTOMATIC TRACK TYPE DETECTION (Líneas de salida/meta)
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  
                print("¡Pista NARANJA detectada! Configurando giros a la derecha.")
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  
                print("¡Pista AZUL detectada! Configurando giros a la izquierda.")

        # 2. OBSTACLE DETECT AND EVADE (PRIORIDAD ALTA)
        # Si estamos esquivando, mantenemos la maniobra por un breve instante (ej. 0.6 segundos)
        if esquivando:
            if time.time() - tiempo_esquiva > 0.6:
                esquivando = False
                print("Maniobra de esquiva completada. Volviendo a centrado.")
                LNM.turn_center()
            else:
                # Continúa ejecutando la evasión sin evaluar el PID de las paredes
                continue

        # Si no estamos esquivando activamente, buscamos nuevos obstáculos en el frente
        if not girando and not esquivando:
            # OBSTÁCULO ROJO -> Esquivar por la DERECHA
            if LNM.red_area > UMBRAL_OBSTACULO:
                print(f"¡Obstáculo ROJO detectado! (Área: {LNM.red_area}). Esquivando por la DERECHA.")
                LNM.turn_right(angle=110, speed=55) # Ángulo pronunciado a la derecha
                esquivando = True
                tiempo_esquiva = time.time()
                continue
            
            # OBSTÁCULO VERDE -> Esquivar por la IZQUIERDA
            elif LNM.green_area > UMBRAL_OBSTACULO:
                print(f"¡Obstáculo VERDE detectado! (Área: {LNM.green_area}). Esquivando por la IZQUIERDA.")
                LNM.turn_left(angle=50, speed=55)  # Ángulo pronunciado a la izquierda
                esquivando = True
                tiempo_esquiva = time.time()
                continue

        # 3. DYNAMIC PID WALL-CENTERING SYSTEM
        # Solo se ejecuta si no estamos girando en una esquina y no estamos esquivando un pilar
        if not girando and not esquivando and LNM.turning_direction != 0:
            
            # Dynamic wall assignment based on track type
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                error = TARGET_DIST - current_dist
                lado_correccion = 1                    
            
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                error = TARGET_DIST - current_dist
                lado_correccion = -1

            # PID Math calculations
            integral += error
            derivative = error - prev_error
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            # Steering angle execution and limits
            steering_angle = int(80 + (correction * lado_correccion))
            steering_angle = max(40, min(120, steering_angle))
            
            if abs(error) < 2:
                LNM.turn_center()
            elif steering_angle > 85:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 75:
                LNM.turn_left(angle=steering_angle, speed=50)

        # 4. CORNER LOGIC AND LAP COUNTER
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

        # Cornering handling execution (Curvas cerradas)
        # Se añade "not esquivando" para evitar que confunda una esquina con la maniobra de un pilar
        if front_dist < 80 and not girando and not esquivando and LNM.black_area > 9000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 100:
            LNM.turn_center()
            girando = False
            conteo = False

        # Race finish condition (En el reto 2 suelen ser menos vueltas, ajusta según necesites, ej: 3 vueltas)
        if loops == 3:
            print("¡Reto de obstáculos terminado! Vueltas completadas.")
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
