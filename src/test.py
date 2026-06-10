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

# =========================================================================
# 🎛️ PARÁMETROS PID PROPORCIONALES (AJUSTADOS PARA MATRIZ 1080p)
# =========================================================================
# Se dividen entre 2.85 porque el cálculo trabaja con áreas (escala al cuadrado)
Kp_vision = 0.007    
Ki_vision = 0.0
Kd_vision = 0.0018   
prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 
girando = False

# =========================================================================
# 🛠️ AJUSTES CRÍTICOS DE DIRECCIÓN Y VELOCIDAD
# =========================================================================
LIMIT_IZQ = 40      # Máximo giro permitido a la izquierda
LIMIT_DER = 105     # Máximo giro permitido a la derecha
TOLERANCIA_ANGULO = 3       

VEL_RECTA = 105     # Velocidad en tramos limpios
VEL_EVASION = 95    # Velocidad estable de esquive rápido

# --- CONFIGURACIÓN DE EVASIÓN DE OBSTÁCULOS (ESCALA LINEAL x1.6875) ---
MIN_ANCHO_DETECCION = 17   
UMBRAL_AREA_DETECCION = 855  # Escalado proporcional al cambio de resolución
primer_color_obstaculo = None  

# --- CONFIGURACIÓN DEL FRENO DE MANO DE EMERGENCIA ---
DIST_MIN_CHOQUE = 20.0  
steering_angle = 80     

# --- VARIABLES PARA FIN DE CARRERA NO BLOQUEANTE ---
end_game_triggered = False
end_game_timer = 0.0

# =========================================================================
# 📐 ROIS PROPORCIONALES (ANCHO HORIZONTAL TOTAL: 1080)
# =========================================================================
roi_izq = ROI(0, 169, 540, 253)  
roi_der = ROI(540, 169, 1080, 253) 
roi_obstaculo = ROI(0, 101, 1080, 608) # Cobertura total de extremo a extremo sin puntos ciegos

def obtener_areas_negras():
    cnt_left = LNM.vision.find_contours(LNM.mask_black, roi_izq)
    cnt_right = LNM.vision.find_contours(LNM.mask_black, roi_der)
    area_right = LNM.vision.max_contour(cnt_right, roi_der)[0]
    area_left = LNM.vision.max_contour(cnt_left, roi_izq)[0]
    return [area_right, area_left]

def procesar_obstaculos():
    """ Analiza la ROI completa buscando bloques con sensibilidad corregida. """
    red_ctn = LNM.vision.find_contours(LNM.mask_red, roi_obstaculo)
    green_ctn = LNM.vision.find_contours(LNM.mask_green, roi_obstaculo)
    
    max_red = LNM.vision.max_contour(red_ctn, roi_obstaculo)
    max_green = LNM.vision.max_contour(green_ctn, roi_obstaculo)
    
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if max_red[0] > UMBRAL_AREA_DETECCION: 
            x, y, w, h = cv2.boundingRect(max_red[3])
            if w > MIN_ANCHO_DETECCION:
                x_centro = x + (w // 2)
                cv2.rectangle(LNM.vision.frame[roi_obstaculo.y1:roi_obstaculo.y2, roi_obstaculo.x1:roi_obstaculo.x2], (x, y), (x+w, y+h), (0, 0, 255), 3)
                return "ROJO", x_centro, w
                
    elif max_green[3] is not None:
        if max_green[0] > UMBRAL_AREA_DETECCION:
            x, y, w, h = cv2.boundingRect(max_green[3])
            if w > MIN_ANCHO_DETECCION:
                x_centro = x + (w // 2)
                cv2.rectangle(LNM.vision.frame[roi_obstaculo.y1:roi_obstaculo.y2, roi_obstaculo.x1:roi_obstaculo.x2], (x, y), (x+w, y+h), (0, 255, 0), 3)
                return "VERDE", x_centro, w
                
    return "NINGUNO", 540, 0 # Centro óptico real en 1080p

# --- MAIN CONTROL LOOP ---
while running:
    try:
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        
        color_detectado, x_bloque, ancho_bloque = procesar_obstaculos()
        black_areas = obtener_areas_negras()

        if primer_color_obstaculo is None and color_detectado in ["ROJO", "VERDE"]:
            primer_color_obstaculo = color_detectado
            print(f"🎯 [CONFIG] Primer color de obstáculo registrado: {primer_color_obstaculo}")

        LNM.vision.draw_roi(roi_izq)
        LNM.vision.draw_roi(roi_der)
        LNM.vision.draw_roi(roi_obstaculo)

        cv2.imshow('Vision HD - Modo Competencia', LNM.vision.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()

        # =========================================================================
        # 🚨 FRENO DE MANO INTELIGENTE (RETROCESO DIRECCIONAL SEGÚN REQUISITOS)
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
            print(f"🚨 ¡OBSTRUCCIÓN! Frente a {front_dist:.2f} cm. Escapando...")
            LNM.stop(log=False)
            time.sleep(0.05)
            
            if color_detectado == "VERDE":
                angulo_retroceso = LIMIT_DER  
            elif color_detectado == "ROJO":
                angulo_retroceso = LIMIT_IZQ  
            else:
                angulo_retroceso = LIMIT_IZQ if left_dist < right_dist else LIMIT_DER
            
            LNM.move_backward(angle=angulo_retroceso, speed=75)
            time.sleep(0.85)
            
            LNM.turn_center(log=False)
            prev_error = 0.0
            integral = 0.0
            time.sleep(0.1)
            continue

        LNM.move_forward(speed=VEL_RECTA) 

        # 1. DETECCIÓN DEL SENTIDO DE LA PISTA
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 3420: # 1200 * 2.85
                 LNM.turning_direction = 2
            elif LNM.blue_area > 3420:
                 LNM.turning_direction = 1

        # 2. DETECCIÓN DE CURVAS CERRADAS (ÁREAS ESCALADAS x2.85)
        if front_dist < 55 and not girando and LNM.black_area > 31350 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 22800 and girando and front_dist > 80:
           LNM.turn_center()
           girando = False
           steering_angle = 80

        # =========================================================================
        # CONTROL DE NAVEGACIÓN HÍBRIDO (PAREDES VS EVASIÓN POR BOUNDING BOX)
        # =========================================================================
        if not girando and LNM.turning_direction != 0:
            
            # CASO A: EVASIÓN ACTIVA DE OBSTÁCULOS DE COLOR
            if color_detectado in ["ROJO", "VERDE"]:
                LNM.move_forward(speed=VEL_EVASION) # Baja velocidad para ganar precisión mecánica
                
                if color_detectado == "VERDE":
                    base_izq = 38 
                    factor_proximidad = int(ancho_bloque * 0.18) # Escalado lineal para 1080p
                    raw_angle = 80 - base_izq - factor_proximidad
                    steering_angle = max(LIMIT_IZQ, min(LIMIT_DER, raw_angle))
                
                elif color_detectado == "ROJO":
                    base_der = 38
                    factor_proximidad = int(ancho_bloque * 0.18)
                    raw_angle = 80 + base_der + factor_proximidad
                    steering_angle = max(LIMIT_IZQ, min(LIMIT_DER, raw_angle))

            # CASO B: PISTA LIBRE (Centrado clásico por diferencia de áreas negras)
            else:
                error = black_areas[1] - black_areas[0]
                integral += error
                integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
                derivative = error - prev_error
                correction = (Kp_vision * error) + (Ki_vision * integral) + (Kd_vision * derivative)
                prev_error = error
                
                raw_angle = int(80 + correction)
                steering_angle = max(LIMIT_IZQ, min(LIMIT_DER, raw_angle))

            # --- EJECUCIÓN FÍSICA DE LA DIRECCIÓN ACKERMANN ---
            if abs(steering_angle - 80) <= TOLERANCIA_ANGULO and color_detectado == "NINGUNO":
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=VEL_RECTA)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=VEL_RECTA)

        # =========================================================================
        # 3. CONTROL DE VUELTAS Y FIN DE CARRERA
        # =========================================================================
        current_time = time.time() 
        # ... (Tu control de tiempo de vueltas idéntico aquí abajo)
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

LNM.stop()
