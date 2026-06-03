import cv2
import time
from vision_controller import ROI, VisionController
from PID_class import PIDController
from mega_pi_controller import *
from constants import *

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)
picam2 = LNM.vision  # Instancia única de la cámara vinculada al controlador

# Configuración de la Región de Interés (ROI)
roi = ROI(100, 100, picam2.image_width - 100, picam2.image_height - 100)
print("System started. Press 'q' to quit.")

# --- PID CONTROLLER FOR WALL-CENTERING ---
TARGET_DIST = 30.0
Kp_wall, Ki_wall, Kd_wall = 1.5, 0.0, 0.8
prev_error_wall = 0.0
integral_wall = 0.0

# --- PID CONTROLLERS FOR OBSTACLES ---
set_point_red = (155, 120)
set_point_green = (516, 125)
pid_red = PIDController(kp=0.5, ki=0.00, kd=0.1)
pid_green = PIDController(kp=0.5, ki=0.00, kd=0.1)

# --- VARIABLES DE CONTROL GENERAL ---
SERVO_CENTER = 90
MIN_SERVO_LIMIT = 40
MAX_SERVO_LIMIT = 120
MIN_AREA_OBSTACLE = 1500  # Área mínima en píxeles para activar la evasión visual

running = True
loops = 0
girando = False
n = 0
orange_timer = time.time()

# --- MAIN CONTROL LOOP ---
try:
    while running:
        # 1. DATA ACQUISITION & PROCESSING
        picam2.receive_image()
        if picam2.frame is None:
            continue

        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        #LNM.debug_UI()
        
        # Avanzar por defecto, la dirección se corregirá abajo
        LNM.move_forward(speed=75) 
        front_dist, left_dist, right_dist = LNM.get_distances()

        # 2. TRACK TYPE DETECTION (Lógica Original)
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2
            elif LNM.upper_orange_area > 1200 and front_dist < 80:
                LNM.turning_direction = 1

        # 3. COMPUTER VISION: OBSTACLE DETECTION (Red & Green)
        red_ctn = picam2.find_contours(LNM.mask_red, roi) 
        green_ctn = picam2.find_contours(LNM.mask_green, roi)
        
        max_red = picam2.max_contour(red_ctn, roi)
        max_green = picam2.max_contour(green_ctn, roi)
        
        # Bandera para saber si el control visual toma el mando
        evading_obstacle = False
        servo_angle = SERVO_CENTER

        # Verificar si hay algún obstáculo válido y lo suficientemente grande cerca
        has_red = max_red[3] is not None and max_red[0] > MIN_AREA_OBSTACLE
        has_green = max_green[3] is not None and max_green[0] > MIN_AREA_OBSTACLE

        # 4. PRIORITIZATION & STEERING LOGIC
        if has_red and (not has_green or max_red[0] > max_green[0]):
            # --- EVASIÓN OBSTÁCULO ROJO ---
            evading_obstacle = True
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))  
            centroid_coords = picam2.draw_centroid_line(max_red, roi)
            
            if centroid_coords:
                current_x = centroid_coords[0]
                pid_output = pid_red.compute(set_point_red[0], current_x)
                
                # Inversión de signo corregida para tu lógica: 
                # Si el bloque rojo está a la derecha, el coche debe ir a la derecha (hacia 40°)
                servo_angle = SERVO_CENTER - pid_output 
                picam2.draw_parallel_lane_line(centroid_coords, roi, offset=200, avoid_right=True)
                print(f"[视觉 ROJO] X: {current_x} | Servo: {servo_angle:.2f}")

        elif has_green:
            # --- EVASIÓN OBSTÁCULO VERDE ---
            evading_obstacle = True
            picam2.draw_contours(green_ctn, roi, (0, 255, 0))  
            centroid_coords = picam2.draw_centroid_line(max_green, roi)
            
            if centroid_coords:
                current_x = centroid_coords[0]
                pid_output = pid_green.compute(set_point_green[0], current_x)
                
                # Si el bloque verde está a la izquierda, el coche debe ir a la izquierda (hacia 120°)
                servo_angle = SERVO_CENTER - pid_output
                picam2.draw_parallel_lane_line(centroid_coords, roi, offset=200, avoid_right=False)
                print(f"[视觉 VERDE] X: {current_x} | Servo: {servo_angle:.2f}")

        # Si la cámara está evadiendo, ejecutamos el giro visual de inmediato
        if evading_obstacle:
            servo_angle = max(MIN_SERVO_LIMIT, min(servo_angle, MAX_SERVO_LIMIT))
            LNM.turn_left(angle=int(servo_angle), speed=50)
            
        # 5. WALL CENTERING SYSTEM (Solo si NO hay obstáculos al frente)
        elif not girando and LNM.turning_direction == 2:
            current_dist = min(left_dist, 60.0)
            
            error_wall = TARGET_DIST - current_dist 
            integral_wall += error_wall
            derivative_wall = error_wall - prev_error_wall
            
            correction_wall = (Kp_wall * error_wall) + (Ki_wall * integral_wall) + (Kd_wall * derivative_wall)
            prev_error_wall = error_wall
            
            steering_angle = int(80 + correction_wall)
            steering_angle = max(MIN_SERVO_LIMIT, min(MAX_SERVO_LIMIT, steering_angle))
            
            if abs(error_wall) < 2:
                LNM.turn_center()
            elif steering_angle > 85:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 75:
                LNM.turn_left(angle=steering_angle, speed=50)

        # 6. CORNER LOGIC & LAP COUNTER (Lógica Original)
        current_time = time.time()

        if LNM.orange_area > 500 and n == 0: 
            orange_timer = current_time
            n = 1
            loops += 1

        if current_time - orange_timer > 3: 
            n = 0

        if front_dist < 80 and not girando and LNM.black_area > 9000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error_wall = 0.0
            integral_wall = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 100:
            LNM.turn_center()
            girando = False

        print(f"Loops: {loops} | Orange Area: {LNM.orange_area} | Front Dist: {front_dist}")

        if loops == 12:
            break

        # UI Rendering
        picam2.draw_roi(roi)  
        cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
except Exception as e:
    print("Exception occurred:", e)
finally:
    # --- SAFETY SHUTDOWN ---
    LNM.stop()
    cv2.destroyAllWindows()
