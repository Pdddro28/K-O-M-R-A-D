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

roi2 = ROI(0, 100, 320, 150)
roi = ROI(320, 100, 640, 150)

black_area_right = 0
black_area_left = 0
blackcnt_right = None
blackcnt_left = None
def obtener_areas():
    global black_area_right, black_area_left, blackcnt_right, blackcnt_left
    blackcnt_left = LNM.vision.find_contours(LNM.mask_black,roi2)
    blackcnt_right = LNM.vision.find_contours(LNM.mask_black,roi)
    black_area_right = LNM.vision.max_contour(blackcnt_right,roi)[0]
    black_area_left = LNM.vision.max_contour(blackcnt_left,roi2)[0]
    return [black_area_right, black_area_left]
def draw_rois():
    LNM.vision.draw_roi(roi)
    LNM.vision.draw_roi(roi2)
    LNM.vision.draw_contours(blackcnt_left, roi2, (0, 255, 255))
    LNM.vision.draw_contours(blackcnt_right, roi, (0, 255, 255))
# --- MAIN CONTROL LOOP ---
while running:
    try:
        # Sensors and data acquisition
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        black_areas = obtener_areas()
        print(f"Black Areas - Right: {black_areas[0]}, Left: {black_areas[1]}, Sum: {black_areas[0] + black_areas[1]}")
        draw_rois()

        cv2.imshow('Vision HD - Posicion Corregida', LNM.vision.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        #print(f"Turning: {LNM.turning_direction}, black_area: {LNM.black_area}, blue_area: {LNM.blue_area}, orange_area: {LNM.orange_area}")
        #print(f"Distances - Front: {front_dist:.2f} cm, Left: {left_dist:.2f} cm, Right: {right_dist:.2f} cm")

        
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()