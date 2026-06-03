from mega_pi_controller import *
from constants import *
import cv2 

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
orange_timer = time.time()
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
        LNM.move_forward(speed = 75) 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        print(LNM.black_area)
        #qprint(f"Distances - Front: {front_dist:.2f} cm, Left: {left_dist:.2f} cm, Right: {right_dist:.2f} cm")
        # 1. TRACK TYPE DETECTION
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
                
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)
            elif LNM.blue_area > 1200 :
                 LNM.turning_direction = 1
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)


        if front_dist < 90 and not girando and LNM.black_area > 9000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 9000 and girando and front_dist > 100:
           LNM.turn_center()
           girando = False
           conteo = False

        # 2. PID WALL-CENTERING SYSTEM
        if not girando and LNM.turning_direction == 2 and loops > 1:
            current_dist = min(left_dist, 60.0)
            
            error = TARGET_DIST - current_dist 
            integral += error
            derivative = error - prev_error
            
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            steering_angle = int(80 + correction)
            steering_angle = max(40, min(120, steering_angle))
            
            if abs(error) < 2:
                LNM.turn_center()
            elif steering_angle > 85:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 75:
                LNM.turn_left(angle=steering_angle, speed=50)

        # 3. CORNER LOGIC AND LAP COUNTER
        current_time = time.time()

        if LNM.orange_area > 500 and n == 0: 
            orange_timer = current_time
            n = 1
            loops += 1

        if current_time - orange_timer > 3: 
            n = 0
            print("Timer reset, ready for next orange line detection.")


        print("Loop count:", loops)

        if loops == 12:
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
