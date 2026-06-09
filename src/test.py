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

# --- PARÁMETROS PID PARA CONTROL VISUAL DE PAREDES ---
Kp_vision = 0.015    
Ki_vision = 0.0
Kd_vision = 0.005   
prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 
girando = False

# --- CONFIGURACIÓN DE EVASIÓN DE OBSTÁCULOS (CÁMARA) ---
# Ganancia para el esquive: define qué tan agresivo se mueve al ver un bloque
Kp_obstaculo = 0.15  
MIN_ANCHO_DETECCION = 20   # Ignora ruidos visuales más pequeños que este ancho en píxeles

# --- CONFIGURACIÓN DEL FRENO DE MANO DE EMERGENCIA ---
DIST_MIN_CHOQUE = 20.0  
steering_angle = 80     

# --- VARIABLES DE TOLERANCIA ---
UMBRAL_PIXELES_MUERTO = 150  
TOLERANCIA_ANGULO = 3       

# --- VARIABLES PARA FIN DE CARRERA NO BLOQUEANTE ---
end_game_triggered = False
end_game_timer = 0.0

# --- ROIS LATERALES Y DE OBSTÁCULOS ---
roi_izq = ROI(0, 100, 320, 150)  
roi_der = ROI(320, 100, 640, 150) 
roi_obstaculo = ROI(40, 60, 600, 360) # ROI amplio para cazar bloques de frente

def obtener_areas_negras():
    cnt_left = LNM.vision.find_contours(LNM.mask_black, roi_izq)
    cnt_right = LNM.vision.find_contours(LNM.mask_black, roi_der)
    area_right = LNM.vision.max_contour(cnt_right, roi_der)[0]
    area_left = LNM.vision.max_contour(cnt_left, roi_izq)[0]
    return [area_right, area_left]

def procesar_obstaculos():
    """ 
    Analiza la ROI central buscando bloques.
    Retorna: color ("ROJO", "VERDE", "NINGUNO"), x_centro_bloque, ancho_bloque
    """
    red_ctn = LNM.vision.find_contours(LNM.mask_red, roi_obstaculo)
    green_ctn = LNM.vision.find_contours(LNM.mask_green, roi_obstaculo)
    
    max_red = LNM.vision.max_contour(red_ctn, roi_obstaculo)
    max_green = LNM.vision.max_contour(green_ctn, roi_obstaculo)
    
    # Validar Bloque Rojo
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if max_red[0] > 1500: # Filtro de área mínima
            x, y, w, h = cv2.boundingRect(max_red[3])
            if w > MIN_ANCHO_DETECCION:
                x_centro = x + (w // 2)
                # Dibujar Bounding Box en Rojo
                cv2.rectangle(LNM.vision.frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                return "ROJO", x_centro, w
                
    # Validar Bloque Verde
    elif max_green[3] is not None:
        if max_green[0] > 1500:
            x, y, w, h = cv2.boundingRect(max_green[3])
            if w > MIN_ANCHO_DETECCION:
                x_centro = x + (w // 2)
                # Dibujar Bounding Box en Verde
                cv2.rectangle(LNM.vision.frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                return "VERDE", x_centro, w
                
    return "NINGUNO", 320, 0

# --- MAIN CONTROL LOOP ---
while running:
    try:
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        
        color_detectado, x_bloque, ancho_bloque = procesar_obstaculos()
        black_areas = obtener_areas_negras()

        # Dibujar ROIs de referencia en la pantalla
        LNM.vision.draw_roi(roi_izq)
        LNM.vision.draw_roi(roi_der)
        LNM.vision.draw_roi(roi_obstaculo)

        cv2.imshow('Vision HD - Modo Competencia', LNM.vision.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()

        # =========================================================================
        # FRENO DE MANO INTELIGENTE CON CONTROL DE ORIENTACIÓN
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0 and color_detectado == "NINGUNO":
            print(f"🚨 ¡OBSTRUCCIÓN! Frente a {front_dist:.2f} cm. Calculando escape...")
            LNM.stop(log=False)
            time.sleep(0.05)
            
            # Escape dinámico basado en proximidad lateral real
            angulo_retroceso = 50 if left_dist < right_dist else 110
            LNM.move_backward(angle=angulo_retroceso, speed=75)
            time.sleep(0.85)
            
            LNM.turn_center(log=False)
            prev_error = 0.0
            integral = 0.0
            time.sleep(0.1)
            continue

        # Tracción constante establecida a tu velocidad ideal de control
        LNM.move_forward(speed=75) 

        # 1. DETECCIÓN DEL SENTIDO DE LA PISTA
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # 2. DETECCIÓN DE CURVAS CERRADAS
        if front_dist < 55 and not girando and LNM.black_area > 11000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
           LNM.turn_center()
           girando = False
           steering_angle = 80

        # =========================================================================
        # CONTROL DE NAVEGACIÓN HÍBRIDO (PAREDES VS EVASIÓN POR BOUNDING BOX)
        # =========================================================================
        if not girando and LNM.turning_direction != 0:
            
            # CASO A: EVASIÓN ACTIVA DE OBSTÁCULOS DE COLOR
            if color_detectado in ["ROJO", "VERDE"]:
                # Medimos qué tan lejos del centro horizontal (320) está el bloque
                error_obstaculo = 320 - x_bloque
                
                if color_detectado == "VERDE":
                    # Obstáculo Verde -> Tu regla manda ir al carril IZQUIERDO.
                    # Forzamos un bias base hacia la izquierda y le sumamos la evasión proporcional
                    base_izq = 30  # Fuerza de salida del carril
                    steering_angle = int(80 - base_izq + (error_obstaculo * Kp_obstaculo))
                    print(f"🟢 EVADIENDO VERDE -> Carril Izquierdo. Ángulo: {steering_angle}")
                
                elif color_detectado == "ROJO":
                    # Obstáculo Rojo -> Tu regla manda ir al carril DERECHO.
                    # Forzamos un bias base hacia la derecha y le restamos la evasión proporcional
                    base_der = 30
                    steering_angle = int(80 + base_der + (error_obstaculo * Kp_obstaculo))
                    print(f"🔴 EVADIENDO ROJO -> Carril Derecho. Ángulo: {steering_angle}")

            # CASO B: PISTA LIBRE (Centrado clásico por diferencia de áreas negras)
            else:
                error = black_areas[1] - black_areas[0]
                integral += error
                integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
                derivative = error - prev_error
                correction = (Kp_vision * error) + (Ki_vision * integral) + (Kd_vision * derivative)
                prev_error = error
                
                steering_angle = int(80 + correction)

            # --- ACOTAMIENTO FÍSICO Y FILTROS DE HISTÉRESIS ---
            steering_angle = max(40, min(120, steering_angle))
            
            if abs(steering_angle - 80) <= TOLERANCIA_ANGULO and color_detectado == "NINGUNO":
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

        # =========================================================================
        # 3. CONTROL DE VUELTAS Y FIN DE CARRERA
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

        if current_time - blue_timer > 1.7 and LNM.turning_direction == 1:
            n = 0

        if loops >= 12 and not end_game_triggered:
            end_game_timer = current_time
            end_game_triggered = True

        if end_game_triggered:
            if current_time - end_game_timer >= 1:
                break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
