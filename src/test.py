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
n = 0

# =========================================================================
# 🎛️ CONTROLADOR PD (PURA DIFERENCIA DE ÁREAS EN 1080p)
# =========================================================================
Kp_vision = 0.007    
Kd_vision = 0.0068   

prev_error = 0.0
girando = False

while not LNM.start():
    pass
# =========================================================================
# 🛠️ CALIBRACIÓN MECÁNICA DE DIRECCIÓN Y CONFIGURACIÓN CRÍTICA
# =========================================================================
LIMIT_IZQ = 40                  # Límite máximo de giro físico izquierdo
LIMIT_DER = 105                 # Límite máximo de giro físico derecho
TOLERANCIA_ANGULO = 3           # Banda muerta para forzar el centro directo (80)
steering_angle = 80             

# --- AJUSTES DE SEGURIDAD POR ULTRASONIDOS ---
DIST_MIN_CHOQUE = 10.0          # Freno de mano de emergencia frontal (cm)
DIST_CRITICA_CURVA = 85.0       # Gatillo de proximidad frontal para forzar cruce
DIST_MIN_PARED_FALLBACK = 20.0  # Límite lateral seguro (Guardarraíl electrónico)

# --- FIN DE CARRERA (12 VUELTAS) ---
lap_time = 1
end_game_triggered = False
end_game_timer = 0.0

# =========================================================================
# 📐 ROIS SIMÉTRICAS SIN PUNTOS CIEGOS (RESOLUCIÓN EXACTA: 1080 x 370)
# =========================================================================
roi_izq = ROI(0, 100, 540, 150)  
roi_der = ROI(540, 100, 1080, 150) 
roi_frontal = ROI(200, 20, 880, 200)  # Perfectamente ubicado en tu escala Y de 370
roi_lineas = ROI(200, 400, 880, 450)  # Para detección de líneas de pista

black_area_right = 0
black_area_left = 0
black_area_front = 0
blue_area = 0
orange_area = 0
cnt_right = None
cnt_left = None
cnt_front = None
cnt_orange = None
cnt_blue = None

def obtener_areas_negras():
    global black_area_right, black_area_left, black_area_front, cnt_right, cnt_left, cnt_front, orange_area, blue_area, cnt_orange, cnt_blue
    cnt_left = LNM.vision.find_contours(LNM.mask_black, roi_izq)
    cnt_right = LNM.vision.find_contours(LNM.mask_black, roi_der)
    black_area_right = LNM.vision.max_contour(cnt_right, roi_der)[0]
    black_area_left = LNM.vision.max_contour(cnt_left, roi_izq)[0]

    cnt_front = LNM.vision.find_contours(LNM.mask_black, roi_frontal)
    black_area_front = LNM.vision.max_contour(cnt_front, roi_frontal)[0]
    
    cnt_orange = LNM.vision.find_contours(LNM.mask_orange, roi_lineas)
    orange_area = LNM.vision.max_contour(cnt_orange, roi_lineas)[0]
    cnt_blue = LNM.vision.find_contours(LNM.mask_blue, roi_lineas)
    blue_area = LNM.vision.max_contour(cnt_blue, roi_lineas)[0]

    return [black_area_right, black_area_left, black_area_front]


def draw_rois():
    LNM.vision.draw_roi(roi_izq)
    LNM.vision.draw_roi(roi_der)
    LNM.vision.draw_roi(roi_frontal)
    LNM.vision.draw_roi(roi_lineas)
    LNM.vision.draw_contours(cnt_left, roi_izq, (0, 255, 255))
    LNM.vision.draw_contours(cnt_right, roi_der, (0, 255, 255))
    LNM.vision.draw_contours(cnt_front, roi_frontal, (0, 255, 255))
    LNM.vision.draw_contours(cnt_orange, roi_lineas, (0, 255, 255))
    LNM.vision.draw_contours(cnt_blue, roi_lineas, (0, 255, 255))

# --- MAIN CONTROL LOOP ---
while running:
    try:
        # Adquisición de imágenes y telemetría de líneas de la pista
        LNM.vision.receive_image()
        
        # Extracción síncrona de los datos en cada ciclo
        black_areas = obtener_areas_negras()
        draw_rois()
        
        # Telemetría en consola para depuración rápida de umbrales
        #print(f"📊 Áreas -> Izq: {black_areas[1]} | Der: {black_areas[0]} | Frente: {black_areas[2]}")

        cv2.imshow('Vision HD - Modo Desarrollo Basico', LNM.vision.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Lectura síncrona de los sensores ultrasónicos
        front_dist, left_dist, right_dist = LNM.get_distances()
        print(f"📏 Distancias -> Frente: {front_dist:.2f} cm | Izq: {left_dist:.2f} cm | Der: {right_dist:.2f} cm")

        # =========================================================================
        # 🚨 FRENO DE MANO DE EMERGENCIA (Evasión ante colisión frontal inminente)
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
            print(f"🚨 FRENO DE MANO! Colisión frontal inminente a {front_dist:.2f} cm.")
            LNM.stop(log=False)
            time.sleep(0.05)
            
            angulo_retroceso = LIMIT_IZQ if left_dist > right_dist else LIMIT_DER
            
            LNM.move_backward(angle=angulo_retroceso, speed=65)
            time.sleep(0.85)
            
            LNM.turn_center(log=False)
            prev_error = 0.0
            time.sleep(0.1)
            continue

        # Inyección de velocidad constante en el avance libre
        LNM.move_forward(speed=75) 

        # 1. DETECCIÓN DEL SENTIDO DE GIRO DE LA PISTA (Azul = Horario / Naranja = Antihorario)
        if LNM.turning_direction == 0: 
            if orange_area > 3000:
                LNM.turning_direction = 2
                print("🏁 Dirección de pista establecida: ANTIHORARIO (Línea Naranja)")
            elif blue_area > 3000:
                LNM.turning_direction = 1
                print("🏁 Dirección de pista establecida: HORARIO (Línea Azul)")

        # =========================================================================
        # 2. DETECCIÓN Y EJECUCIÓN EN ESQUINAS CORREGIDA (Lectura real de la lista)
        # =========================================================================
        if front_dist < DIST_CRITICA_CURVA and not girando and black_areas[2] > 30480 and LNM.turning_direction != 0:
            print("↪️ Esquina detectada visualmente. Activando giro forzado.")
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
              
        if black_areas[2] < 22800 and girando and front_dist > 80:
            print("➡️ Recta recuperada. Centrando chasis.")
            LNM.turn_center()
            girando = False
            steering_angle = 80

        # =========================================================================
        # 🛠️ NAVEGACIÓN BASADA EN ÁREAS LATERALES (CONTROL PD) Y GUARDARRAÍL
        # =========================================================================
        if not girando and LNM.turning_direction != 0:
            
            # Algoritmo PD de centrado
            error = black_areas[1] - black_areas[0]  # Izquierda - Derecha
            derivative = error - prev_error
            correction = (Kp_vision * error) + (Kd_vision * derivative)
            prev_error = error
            
            raw_angle = int(80 + correction)
            steering_angle = max(LIMIT_IZQ, min(LIMIT_DER, raw_angle))

            # --- GUARDARRAÍL ELECTRÓNICO POR ULTRASONIDOS ---
            # if left_dist < DIST_MIN_PARED_FALLBACK and left_dist > 1.0:
            #     steering_angle = max(steering_angle, 92) 
            # elif right_dist < DIST_MIN_PARED_FALLBACK and right_dist > 1.0:
            #     steering_angle = min(steering_angle, 55)

            # --- EJECUCIÓN FÍSICA EN LA DIRECCIÓN ACKERMANN ---
            if abs(steering_angle - 80) <= TOLERANCIA_ANGULO:
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=95)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=95)

        # =========================================================================
        # ⏱️ CONTROL DE VUELTAS Y CRONÓMETRO DE FINALIZACIÓN
        # =========================================================================
        current_time = time.time() 

        if LNM.orange_area > 1425 and n == 0 and LNM.turning_direction == 2: 
            orange_timer = current_time
            n = 1
            loops += 1
            print(f"🔶 VUELTA NARANJA REGISTRADA - Conteo Actual: {loops}")

        if LNM.blue_area > 1425 and n == 0 and LNM.turning_direction == 1: 
            blue_timer = current_time
            n = 1
            loops += 1
            print(f"🔵 VUELTA AZUL REGISTRADA - Conteo Actual: {loops}")

        if current_time - orange_timer > lap_time and LNM.turning_direction == 2: 
            n = 0

        if current_time - blue_timer > lap_time and LNM.turning_direction == 1:
            n = 0

        if loops >= 12 and not end_game_triggered:
            end_game_timer = current_time
            end_game_triggered = True

        if end_game_triggered:
            if current_time - end_game_timer >= 1.0:
                print("🏁 Reto completado con éxito tras 12 vueltas limpias. Deteniendo...")
                break
        
    except Exception as e:
        print("Exception en el ciclo principal:", e.with_traceback())
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
