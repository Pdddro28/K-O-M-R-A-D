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

# --- PID CONTROLLER VARIABLES ---
TARGET_DIST = 30.0  
Kp = 1.5   
Ki = 0.0   
Kd = 0.8   

prev_error = 0.0
integral = 0.0
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
            elif LNM.upper_orange_area > 900:
                LNM.turning_direction = 1  
                print("¡Pista AZUL detectada! Configurando giros a la izquierda.")

        # 2. DYNAMIC PID WALL-CENTERING SYSTEM
        if not girando and LNM.turning_direction != 0:
            
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

        # 3. CORNER LOGIC AND LAP COUNTER
        current_time = time.time()
        
        area_actual = LNM.orange_area if LNM.turning_direction == 2 else LNM.upper_orange_area

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
        if loops == 13:
            print("¡Carrera terminada! 18 vueltas completadas.")
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
