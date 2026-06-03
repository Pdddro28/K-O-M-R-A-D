import cv2
import time
from mega_pi_controller import *
from constants import *
from vision_controller import ROI, VisionController
from PID_class import PIDController

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)
picam2 = LNM.vision  # Instancia única de la cámara integrada en tu controlador

# Configuración de ROIs
roi_obstaculos = ROI(100, 100, picam2.image_width - 100, picam2.image_height - 100)

states = {"straight": False, "girando": False}
running = True
loops = 0
BASE_SPEED = 50

# --- PID 1: SEGUIDOR DE PAREDES (Variables del código 1) ---
TARGET_DIST = 30.0  
Kp_wall = 1.8    
Ki_wall = 0.01   
Kd_wall = 1.2    
prev_error_wall = 0.0
integral_wall = 0.0
MAX_INTEGRAL_WALL = 15.0

girando = False
n = 0
color_timer = time.time()

# --- PID 2: EVASIÓN DE OBSTÁCULOS (Variables del código 2) ---
SET_POINT_RED_X = 155
SET_POINT_GREEN_X = 516

pid_red = PIDController(kp=0.5, ki=0.00, kd=0.1)
pid_green = PIDController(kp=0.5, ki=0.00, kd=0.1)

# Umbral mínimo de pixeles para ignorar ruido de fondo de los bloques
MIN_BLOB_AREA = 300 

SERVO_CENTER = 80  # Tu código 1 define 80 como el centro neutral físico del servo
print("Sistema Iniciado. Presiona 'q' en la ventana de video para salir.")

# --- MAIN CONTROL LOOP ---
try:
    while running:
        # 1. ACQUISITION AND PROCESSING
        picam2.receive_image()
        if picam2.frame is None:
            continue
            
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        LNM.debug_UI()
        
        front_dist, left_dist, right_dist = LNM.get_distances()
        current_time = time.time()

        # Emergency break condition via window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 2. AUTOMATIC TRACK TYPE DETECTION (Líneas de la pista)
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  
                print("¡Pista NARANJA detectada! Configurando giros a la derecha.")
            elif LNM.upper_orange_area > 900:
                LNM.turning_direction = 1  
                print("¡Pista AZUL detectada! Configurando giros a la izquierda.")

        # 3. DETECCIÓN DE OBSTÁCULOS POR COLOR (CÁMARA)
        red_ctn = picam2.find_contours(LNM.mask_red, roi_obstaculos) 
        green_ctn = picam2.find_contours(LNM.mask_green, roi_obstaculos)
        
        max_red = picam2.max_contour(red_ctn, roi_obstaculos)
        max_green = picam2.max_contour(green_ctn, roi_obstaculos)

        # Variables bandera para determinar qué acción tomar
        obstaculo_detectado = False
        steering_angle = SERVO_CENTER

        # Verificar si hay obstáculos válidos basados en el tamaño de su área
        rojo_valido = max_red[3] is not None and max_red[0] > MIN_BLOB_AREA
        verde_valido = max_green[3] is not None and max_green[0] > MIN_BLOB_AREA

        # --- LÓGICA DE CONTROL DE CONDUCCIÓN (Prioridades) ---
        
        # PRIORIDAD 1: Esquivar Esquinas Críticas de la pista (Código 1)
        if front_dist < 80 and not girando and LNM.black_area > 9000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error_wall = 0.0
            integral_wall = 0.0
            
        elif LNM.black_area < 8000 and girando and front_dist > 100:
            LNM.turn_center()
            girando = False

        # PRIORIDAD 2: Evasión Activa de Bloques (Código 2) si no está en un giro forzado de esquina
        elif not girando and (rojo_valido or verde_valido):
            obstaculo_detectado = True
            
            # Decidir qué bloque evadir (el que tenga mayor área visible en pantalla)
            if rojo_valido and (not verde_valido or max_red[0] > max_green[0]):
                # --- EVADIR ROJO ---
                picam2.draw_contours(red_ctn, roi_obstaculos, (0, 0, 255))  
                centroid_coords = picam2.draw_centroid_line(max_red, roi_obstaculos)
                
                if centroid_coords:
                    current_x = centroid_coords[0]
                    pid_output = pid_red.compute(SET_POINT_RED_X, current_x)
                    
                    # Inversión de dirección matemática para esquivar adecuadamente
                    steering_angle = SERVO_CENTER - pid_output 
                    picam2.draw_parallel_lane_line(centroid_coords, roi_obstaculos, offset=200, avoid_right=True)
                    print(f"[OBSTÁCULO ROJO] Área: {max_red[0]} | X: {current_x} | Servo Target: {steering_angle:.1f}")
                    
            elif verde_valido:
                # --- EVADIR VERDE ---
                picam2.draw_contours(green_ctn, roi_obstaculos, (0, 255, 0))  
                centroid_coords = picam2.draw_centroid_line(max_green, roi_obstaculos)
                
                if centroid_coords:
                    current_x = centroid_coords[0]
                    pid_output = pid_green.compute(SET_POINT_GREEN_X, current_x)
                    
                    steering_angle = SERVO_CENTER - pid_output
                    picam2.draw_parallel_lane_line(centroid_coords, roi_obstaculos, offset=200, avoid_right=False)
                    print(f"[OBSTÁCULO VERDE] Área: {max_green[0]} | X: {current_x} | Servo Target: {steering_angle:.1f}")

            # Ajustar límites físicos de seguridad del carro (Límites 40 a 120 de tu MegaPi)
            steering_angle = max(40, min(120, int(steering_angle)))
            
            # Enviar comando de ejecución de movimiento basado en el ángulo calculado
            if steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=BASE_SPEED)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=BASE_SPEED)
            else:
                LNM.turn_center()

        # PRIORIDAD 3: Centrado de Paredes Dinámico con Sensores Ultrasonido (Código 1)
        elif not girando and LNM.turning_direction != 0:
            
            # Pista Naranja: Sigue pared IZQUIERDA
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                error_wall = TARGET_DIST - current_dist  
                lado_correccion = 1                   
            
            # Pista Azul: Sigue pared DERECHA
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                error_wall = TARGET_DIST - current_dist  
                lado_correccion = -1                  

            # Cálculos del PID de las Paredes
            integral_wall += error_wall
            integral_wall = max(-MAX_INTEGRAL_WALL, min(MAX_INTEGRAL_WALL, integral_wall))
            derivative_wall = error_wall - prev_error_wall
            
            correction_wall = (Kp_wall * error_wall) + (Ki_wall * integral_wall) + (Kd_wall * derivative_wall)
            prev_error_wall = error_wall
            
            steering_angle = int(SERVO_CENTER + (correction_wall * lado_correccion))
            steering_angle = max(40, min(120, steering_angle))
            
            # Ejecución del movimiento de paredes
            if abs(error_wall) < 1.5: 
                LNM.turn_center()
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=BASE_SPEED)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=BASE_SPEED)

        # Si el robot no está bajo ninguna condición de las anteriores, avanza recto por seguridad
        else:
            LNM.move_forward(speed=BASE_SPEED)

        # 4. CONTADOR DE VUELTAS (LAP COUNTER - Código 1)
        area_actual = LNM.orange_area if LNM.turning_direction == 2 else LNM.upper_orange_area
        
        if LNM.turning_direction != 0 and area_actual > 500 and n == 0: 
            color_timer = current_time
            n = 1
            loops += 1
            print(f"--> ¡Línea de Meta Detectada! Vueltas: {loops}/13")

        if current_time - color_timer > 3: 
            n = 0

        if loops == 13:
            print("¡Carrera terminada! 13 vueltas completadas con éxito.")
            break

        # Renderizado visual en tiempo real
        picam2.draw_roi(roi_obstaculos)  
        cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

except Exception as e:
    print("Ocurrió una excepción durante la ejecución:", e)

finally:
    # 5. CLEAN UP & SAFETY SHUTDOWN
    print("Deteniendo motores y limpiando recursos...")
    LNM.stop()
    cv2.destroyAllWindows()
