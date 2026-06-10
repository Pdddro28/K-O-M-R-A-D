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

# --- PARAMÉTROS PID PARA CONTROL VISUAL DE PAREDES ---
Kp_vision = 0.020    
Ki_vision = 0.0
Kd_vision = 0.005   
prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 
girando = False

# =========================================================================
# 🛠️ AJUSTES CRÍTICOS DE DIRECCIÓN & CALIBRACIÓN
# =========================================================================
LIMIT_IZQ = 40              # Máximo giro permitido a la izquierda
LIMIT_DER = 105             # Máximo giro permitido a la derecha
TOLERANCIA_ANGULO = 3       

# --- CONFIGURACIÓN DE EVASIÓN DE OBSTÁCULOS (CÁMARA) ---
MIN_ANCHO_DETECCION = 20   
primer_color_obstaculo = None  # 📌 REQUISITO 4: Registro del primer color del reto

# --- CONFIGURACIÓN DE ULTRASONIDOS Y AJUSTES DE GIRO ---
DIST_MIN_CHOQUE = 15.0          # Freno de mano de emergencia frontal
DIST_CRITICA_CURVA = 11.0       # 📌 REQUISITO 1: Menor distancia = gira más cerca de la pared (antes era 15)
DIST_MIN_PARED_FALLBACK = 12.0  # 📌 REQUISITO 2: Distancia lateral límite para activar el guardarraíl
steering_angle = 80     

# --- VARIABLES PARA FIN DE CARRERA NO BLOQUEANTE ---
lap_time = 4.3
end_game_triggered = False
end_game_timer = 0.0

# --- ROIS LATERALES Y DE OBSTÁCULOS ---
roi_izq = ROI(0, 100,540, 150)  
roi_der = ROI(540, 100, 1080, 150) 
roi_obstaculo = ROI(00, 60, 1080, 360) 

def obtener_areas_negras():
    cnt_left = LNM.vision.find_contours(LNM.mask_black, roi_izq)
    cnt_right = LNM.vision.find_contours(LNM.mask_black, roi_der)
    area_right = LNM.vision.max_contour(cnt_right, roi_der)[0]
    area_left = LNM.vision.max_contour(cnt_left, roi_izq)[0]
    return [area_right, area_left]

def procesar_obstaculos():
    """ Analiza la ROI central buscando bloques. """
    red_ctn = LNM.vision.find_contours(LNM.mask_red, roi_obstaculo)
    green_ctn = LNM.vision.find_contours(LNM.mask_green, roi_obstaculo)
    
    max_red = LNM.vision.max_contour(red_ctn, roi_obstaculo)
    max_green = LNM.vision.max_contour(green_ctn, roi_obstaculo)
    
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if max_red[0] > 1500: 
            x, y, w, h = cv2.boundingRect(max_red[3])
            if w > MIN_ANCHO_DETECCION:
                x_centro = x + (w // 2)
                cv2.rectangle(LNM.vision.frame[roi_obstaculo.y1:roi_obstaculo.y2, roi_obstaculo.x1:roi_obstaculo.x2], (x, y), (x+w, y+h), (0, 0, 255), 3)
                return "ROJO", x_centro, w
                
    elif max_green[3] is not None:
        if max_green[0] > 1500:
            x, y, w, h = cv2.boundingRect(max_green[3])
            if w > MIN_ANCHO_DETECCION:
                x_centro = x + (w // 2)
                cv2.rectangle(LNM.vision.frame[roi_obstaculo.y1:roi_obstaculo.y2, roi_obstaculo.x1:roi_obstaculo.x2], (x, y), (x+w, y+h), (0, 255, 0), 3)
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

        # 📌 REQUISITO 4: Registrar de forma persistente el primer color detectado
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
        # 📌 REQUISITO 3: FRENO DE MANO CON RETROCESO EN CURVA SEGÚN OBSTÁCULO
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
            print(f"🚨 ¡OBSTRUCCIÓN! Frente a {front_dist:.2f} cm. Estatus Bloque: {color_detectado}. Escapando...")
            LNM.stop(log=False)
            time.sleep(0.05)
            
                # Fallback clásico si se activa por aproximación a paredes puras
            angulo_retroceso = LIMIT_IZQ if left_dist < right_dist else LIMIT_DER
            
            LNM.move_backward(angle=angulo_retroceso, speed=75)
            time.sleep(0.85)
            
            LNM.turn_center(log=False)
            prev_error = 0.0
            integral = 0.0
            time.sleep(0.1)
            continue

        # Tracción constante en pista libre
        LNM.move_forward(speed=65) 

        # 1. DETECCIÓN DEL SENTIDO DE LA PISTA
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # 2. DETECCIÓN DE CURVAS CERRADAS (📌 REQUISITO 1: Calibrado con DIST_CRITICA_CURVA)
        if front_dist < DIST_CRITICA_CURVA and not girando and LNM.black_area > 12800 and LNM.turning_direction != 0:
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
                if color_detectado == "VERDE":
                    base_izq = 38 
                    factor_proximidad = int(ancho_bloque * 0.30)
                    raw_angle = 80 - base_izq - factor_proximidad
                    steering_angle = max(LIMIT_IZQ, min(LIMIT_DER, raw_angle))
                
                elif color_detectado == "ROJO":
                    base_der = 38
                    factor_proximidad = int(ancho_bloque * 0.30)
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

            # =========================================================================
            # 📌 REQUISITO 2: GUARDARRAÍL DE FALLBACK ELECTRÓNICO (ULTRASONIDOS LATERALES)
            # =========================================================================
            if left_dist < DIST_MIN_PARED_FALLBACK and left_dist > 1.0:
                # Demasiado cerca de la izquierda: Forzar corrección inmediata a la derecha (suave/medio)
                steering_angle = max(steering_angle, 92) 
            elif right_dist < DIST_MIN_PARED_FALLBACK and right_dist > 1.0:
                # Demasiado cerca de la derecha: Forzar corrección inmediata a la izquierda
                steering_angle = min(steering_angle, 55)

            # --- EJECUCIÓN FÍSICA DE LA DIRECCIÓN ACKERMANN ---
            if abs(steering_angle - 80) <= TOLERANCIA_ANGULO and color_detectado == "NINGUNO":
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=75)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=75)

        # =========================================================================
        # 3. CONTROL DE VUELTAS Y FIN DE CARRERA
        # =========================================================================
        current_time = time.time() 

        if LNM.orange_area > 500 and n == 0 and LNM.turning_direction == 2: 
            orange_timer = current_time
            n = 1
            loops += 1
            print (f"🔶 VUELTA NARANJA DETECTADA - Total Vueltas: {loops}")

        if LNM.blue_area > 500 and n == 0 and LNM.turning_direction == 1: 
            blue_timer = current_time
            n = 1
            loops += 1
            print (f"🔵 VUELTA AZUL DETECTADA - Total Vueltas: {loops}")

        if current_time - orange_timer > lap_time and LNM.turning_direction == 2: 
            n = 0

        if current_time - blue_timer > lap_time and LNM.turning_direction == 1:
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
