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

# --- NUEVOS PARÁMETROS PID PARA CONTROL VISUAL ---
Kp_vision = 0.015    
Ki_vision = 0.0
Kd_vision = 0.005   

prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 
girando = False
conteo = False

# --- PARÁMETROS PD PARA OBSTÁCULOS (SENSORES ToF) ---
Kp_tof = 3.0
Kd_tof = 1.0
prev_error_tof = 0.0
DIST_NORMAL = 20.0
DIST_PEGADO = 12.0  # Distancia objetivo para esquivar el bloque

# --- UMBRALES DE ÁREA CRÍTICOS PARA OBSTÁCULOS ---
MAX_AREA_ROJO = 14000  
MAX_AREA_VERDE = 12000 
MIN_PARED_VALIDA = 350   # Si el área negra baja de esto, se perdió la pared

# --- CONFIGURACIÓN DEL FRENO DE MANO DE EMERGENCIA ---
DIST_MIN_CHOQUE = 20.0  
steering_angle = 80     

# --- VARIABLES DE TOLERANCIA (EVITAR ZIGZAGUEO) ---
UMBRAL_PIXELES_MUERTO = 150  
TOLERANCIA_ANGULO = 3       

# --- VARIABLES PARA FIN DE CARRERA NO BLOQUEANTE ---
end_game_triggered = False
end_game_timer = 0.0

# --- CONFIGURACIÓN DE ROIS LATERALES Y CÁMARA ---
roi_izq = ROI(0, 100, 320, 150)  # ROI Izquierda Pared
roi_der = ROI(320, 100, 640, 150) # ROI Derecha Pared
roi_obstaculo = ROI(0, 50, 640, 380) # ROI Central Obstáculos

black_area_right = 0
black_area_left = 0
blackcnt_right = None
blackcnt_left = None

def obtener_areas():
    global black_area_right, black_area_left, blackcnt_right, blackcnt_left
    blackcnt_left = LNM.vision.find_contours(LNM.mask_black, roi_izq)
    blackcnt_right = LNM.vision.find_contours(LNM.mask_black, roi_der)
    black_area_right = LNM.vision.max_contour(blackcnt_right, roi_der)[0]
    black_area_left = LNM.vision.max_contour(blackcnt_left, roi_izq)[0]
    return [black_area_right, black_area_left]

def draw_rois():
    LNM.vision.draw_roi(roi_izq)
    LNM.vision.draw_roi(roi_der)
    LNM.vision.draw_roi(roi_obstaculo)
    LNM.vision.draw_contours(blackcnt_left, roi_izq, (0, 255, 255))
    LNM.vision.draw_contours(blackcnt_right, roi_der, (0, 255, 255))

def get_color_signal():
    """ Analiza la cámara y retorna el color detectado aplicando filtros de cercanía """
    red_ctn = LNM.vision.find_contours(LNM.mask_red, roi_obstaculo) 
    green_ctn = LNM.vision.find_contours(LNM.mask_green, roi_obstaculo)
    
    max_red = LNM.vision.max_contour(red_ctn, roi_obstaculo)
    max_green = LNM.vision.max_contour(green_ctn, roi_obstaculo)
    
    # Evaluar Bloque Rojo
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if 1700 < max_red[0] < MAX_AREA_ROJO:
            LNM.vision.draw_contours(red_ctn, roi_obstaculo, (0, 0, 255))
            return "ROJO"
            
    # Evaluar Bloque Verde
    elif max_green[3] is not None:
        if 200 < max_green[0] < MAX_AREA_VERDE:
            LNM.vision.draw_contours(green_ctn, roi_obstaculo, (0, 255, 0))
            return "VERDE"
            
    return "NINGUNO"

# --- MAIN CONTROL LOOP ---
while running:
    try:
        # Sensors and data acquisition
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        
        color_detectado = get_color_signal()
        black_areas = obtener_areas()
        draw_rois()

        cv2.imshow('Vision HD - Posicion Corregida', LNM.vision.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()

        # =========================================================================
        # FRENO DE MANO DE EMERGENCIA (Solo si no estamos esquivando un bloque)
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0 and color_detectado == "NINGUNO":
            print(f"🚨 ¡FRENO DE MANO! Frente obstruido a {front_dist:.2f} cm.")
            LNM.stop(log=False)
            time.sleep(0.05)
            
            angulo_escape_opuesto = 160 - steering_angle
            angulo_escape_opuesto = max(40, min(120, angulo_escape_opuesto))
            
            if angulo_escape_opuesto == 80:
                angulo_escape_opuesto = 60
                
            LNM.move_backward(angle=angulo_escape_opuesto, speed=85)
            time.sleep(0.75)
            
            LNM.turn_center(log=False)
            prev_error = 0.0
            integral = 0.0
            time.sleep(0.1)
            continue

        # Avanzamos dinámicamente con la velocidad normal del Open Challenge
        LNM.move_forward(speed=120) 

        # 1. TRACK TYPE DETECTION
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # 2. CORNER DETECTION (Detección de Esquinas para Cruzar)
        if front_dist < 55 and not girando and LNM.black_area > 11000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
           LNM.turn_center()
           girando = False
           conteo = False
           steering_angle = 80

        # =========================================================================
        # CONTROL NAVEGACIÓN HÍBRIDO (PID VISUAL + CONTROL DE OBSTÁCULOS)
        # =========================================================================
        if not girando and LNM.turning_direction != 0:
            
            # CASO A: DETECCIÓN DE TRÁFICO (Esquivar bloques de colores mediante ToF)
            if color_detectado in ["ROJO", "VERDE"]:
                if color_detectado == "ROJO":
                    # Obstáculo Rojo -> Pegarse a la derecha usando sensor derecho
                    current_dist = min(right_dist, 60.0)
                    error_tof = DIST_PEGADO - current_dist
                    correction_tof = (Kp_tof * error_tof) + Kd_tof * (error_tof - prev_error_tof)
                    steering_angle = int(80 - correction_tof) # Resta para ir a la derecha
                else:
                    # Obstáculo Verde -> Pegarse a la izquierda usando sensor izquierdo
                    current_dist = min(left_dist, 60.0)
                    error_tof = DIST_PEGADO - current_dist
                    correction_tof = (Kp_tof * error_tof) + Kd_tof * (error_tof - prev_error_tof)
                    steering_angle = int(80 + correction_tof) # Suma para ir a la izquierda
                
                prev_error_tof = error_tof
                print(f"🚧 ESQUIVANDO OBSTÁCULO {color_detectado} | Ángulo ToF: {steering_angle}")

            # CASO B: RESPALDO ToF (Se perdió una de las paredes negras en la cámara)
            elif black_areas[0] < MIN_PARED_VALIDA or black_areas[1] < MIN_PARED_VALIDA:
                if LNM.turning_direction == 2:  # Sentido Naranja -> Seguir pared izquierda
                    current_dist = min(left_dist, 60.0)
                    error_tof = DIST_NORMAL - current_dist
                    correction_tof = (Kp_tof * error_tof) + Kd_tof * (error_tof - prev_error_tof)
                    steering_angle = int(80 + correction_tof)
                else:                           # Sentido Azul -> Seguir pared derecha
                    current_dist = min(right_dist, 60.0)
                    error_tof = DIST_NORMAL - current_dist
                    correction_tof = (Kp_tof * error_tof) + Kd_tof * (error_tof - prev_error_tof)
                    steering_angle = int(80 - correction_tof)
                
                prev_error_tof = error_tof
                print(f"⚠️ PARED PERDIDA EN CÁMARA | Respaldo ToF -> Ángulo: {steering_angle}")

            # CASO C: PISTA IDEAL (Centrado estándar por diferencia de áreas visuales)
            else:
                error = black_areas[1] - black_areas[0]
                
                integral += error
                integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
                
                derivative = error - prev_error
                correction = (Kp_vision * error) + (Ki_vision * integral) + (Kd_vision * derivative)
                prev_error = error
                
                steering_angle = int(80 + correction)
                print(f"Visual Error: {error}, Steering Angle: {steering_angle}")

            # --- FILTROS DE TOLERANCIA Y EJECUCIÓN DE DIRECCIÓN ---
            steering_angle = max(40, min(120, steering_angle))
            
            if abs(steering_angle - 80) <= TOLERANCIA_ANGULO and color_detectado == "NINGUNO":
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

        # =========================================================================
        # 3. LOGIC AND LAP COUNTER & CRONÓMETRO DINÁMICO DE CIERRE
        # =========================================================================
        current_time = time.time()

        if LNM.orange_area > 500 and n == 0 and LNM.turning_direction == 2: 
            orange_timer = current_time
            n = 1
            loops += 1

        if LNM.blue_area > 500 and n == 0 and LNM.turning_direction == 1: 
            blue_timer = current_time
            n = 1
            loops += 1

        if current_time - orange_timer > 1.7 and LNM.turning_direction == 2: 
            n = 0
            print("Timer reset, ready for next orange line detection.")

        if current_time - blue_timer > 1.7 and LNM.turning_direction == 1:
            n = 0
            print("Timer reset, ready for next blue line detection.")

        if loops >= 12 and not end_game_triggered:
            print("🏁 ¡Vuelta 12 alcanzada! Iniciando cronómetro de gracia...")
            end_game_timer = current_time
            end_game_triggered = True

        if end_game_triggered:
            if current_time - end_game_timer >= 1:
                print("⏱️ Tiempo de gracia completado. Deteniendo robot.")
                break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
