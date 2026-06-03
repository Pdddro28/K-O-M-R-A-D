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
Kp = 1.8    
Ki = 0.01    
Kd = 1.2    

prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 # Anti-windup
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
        LNM.obtenerarea_frontal()
        LNM.debug_UI()
        LNM.move_forward(speed = 50)  
        
        # Emergency break condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        
        # --- 1. CORNER LOGIC (DISTANCE-BASED TURNING DIRECTION) ---
        # If a corner is detected ahead via black area
        if front_dist < 80 and not girando and LNM.black_area > 9000:
            
            # If the right side has significantly more space than the left side -> TURN RIGHT
            if right_dist > left_dist + 20: # 20cm threshold, adjust as needed
                LNM.turning_direction = 2  # Configures wall-following for right-hand loops
                LNM.turn_right(angle=120, speed=50) # Force immediate sharp turn right
                print("¡Obstáculo detectado! El lado derecho está libre. Girando a la DERECHA.")
                girando = True
                
            # If the left side has significantly more space than the right side -> TURN LEFT
            elif left_dist > right_dist + 20:
                LNM.turning_direction = 1  # Configures wall-following for left-hand loops
                LNM.turn_left(angle=40, speed=50) # Force immediate sharp turn left
                print("¡Obstáculo detectado! El lado izquierdo está libre. Girando a la IZQUIERDA.")
                girando = True
                
            if girando:
                prev_error = 0.0
                integral = 0.0
                loops += 1
                print(f"Vuelta registrada: {loops}")

        # Exit cornering mode once the path ahead opens up
        if LNM.black_area < 8000 and girando and front_dist > 100:
            LNM.turn_center()
            girando = False

        # --- 2. DYNAMIC PID WALL-CENTERING SYSTEM ---
        # This only runs when going down straights (not actively hard-turning)
        if not girando and LNM.turning_direction != 0:
            
            # Sigue pared IZQUIERDA (Pista con giros a la Derecha)
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                error = TARGET_DIST - current_dist  
                lado_correccion = 1                 
            
            # Sigue pared DERECHA (Pista con giros a la Izquierda)
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                error = TARGET_DIST - current_dist  
                lado_correccion = -1                

            # PID Math calculations
            integral += error
            integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
            
            derivative = error - prev_error
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            # Servo neutral center is 80
            steering_angle = int(80 + (correction * lado_correccion))
            steering_angle = max(40, min(120, steering_angle))
            
            # Apply corrections
            if abs(error) < 1.5: 
                LNM.turn_center()
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

        # --- 3. RACE FINISH CONDITION ---
        if loops == 13:
            print("¡Carrera terminada! 13 vueltas completadas.")
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
