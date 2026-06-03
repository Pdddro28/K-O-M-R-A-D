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
        print(LNM.turning_direction)
        #qprint(f"Distances - Front: {front_dist:.2f} cm, Left: {left_dist:.2f} cm, Right: {right_dist:.2f} cm")
        # 1. TRACK TYPE DETECTION
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
                
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)
            elif LNM.blue_area > 1200 :
                 LNM.turning_direction = 1
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)


        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
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

# --- SAFETY SHUTDOWN ---
LNM.stop()
