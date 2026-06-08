from mega_pi_controller import *
from constants import *
import cv2 
import time

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

ROIS = [OPEN_ROI_CENTER, ROI_LINES]

running = True
loops = 0

orange_timer = time.time()
blue_timer = time.time()
time_lap = time.time()
n = 0

# --- PARÁMETROS DEL CONTROLADOR PD HÍBRIDO ---
Kp_hybrid = 0.015    
Kd_hybrid = 0.005   

prev_error = 0.0
steering_angle = 80     

# --- CONFIGURACIÓN DEL FRENO DE MANO DE EMERGENCIA ---
DIST_MIN_CHOQUE = 25.0  

# --- VARIABLES DE TOLERANCIA Y FILTRADO ---
UMBRAL_PIXELES_MUERTO = 150  # Ignora variaciones de área insignificantes
TOLERANCIA_ANGULO = 3        # Banda muerta del servo para tramos rectos
MIN_PARED_VALIDA = 350       # Límite por debajo del cual se considera pared perdida en cámara

# --- VARIABLES PARA FIN DE CARRERA NO BLOQUEANTE ---
end_game_triggered = False
end_game_timer = 0.0

# --- CONFIGURACIÓN DE ROIS LATERALES ---
roi2 = ROI(0, 100, 320, 150)  # ROI Izquierda
roi = ROI(320, 100, 640, 150)  # ROI Derecha

black_area_right = 0
black_area_left = 0
blackcnt_right = None
blackcnt_left = None

def obtener_areas():
    global black_area_right, black_area_left, blackcnt_right, blackcnt_left
    blackcnt_left = LNM.vision.find_contours(LNM.mask_black, roi2)
    blackcnt_right = LNM.vision.find_contours(LNM.mask_black, roi)
    black_area_right = LNM.vision.max_contour(blackcnt_right, roi)[0]
    black_area_left = LNM.vision.max_contour(blackcnt_left, roi2)[0]
    return [black_area_right, black_area_left]

# --- MAIN CONTROL LOOP ---
while running:
    try:
        # Adquisición de datos de sensores y vídeo
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        
        black_areas = obtener_areas()
        front_dist, left_dist, right_dist = LNM.get_distances()

        # =========================================================================
        # FRENO DE MANO DE EMERGENCIA (Seguridad física proactiva)
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
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
            time.sleep(0.1)
            continue

        # Avance continuo con la potencia establecida para el Open Challenge
        LNM.move_forward(speed=130) 

        # Detección del sentido inicial de la pista
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # =========================================================================
        # SISTEMA DE NAVEGACIÓN PD HÍBRIDO (Visión + Ultrasonidos Integrados)
        # =========================================================================
        area_izq = black_areas[1]
        area_der = black_areas[0]

        if area_izq > MIN_PARED_VALIDA and area_der > MIN_PARED_VALIDA:
            # CASO OPTIMAL: Ambas paredes detectadas en cámara -> Error por visión espacial
            error = area_izq - area_der
        else:
            # CASO DE RESPALDO / CURVA ABIERTA: Una pared sale de foco -> Control por ToF directo
            # Escalamos la diferencia de distancias (cm) al rango analógico del PD visual
            error = (right_dist - left_dist) * 350

        # Algoritmo de control Proporcional-Derivativo (PD) continuo
        derivative = error - prev_error
        correction = (Kp_hybrid * error) + (Kd_hybrid * derivative)
        prev_error = error
        
        # Mapeo directo sobre el servo de dirección
        steering_angle = int(80 + correction)
        steering_angle = max(40, min(120, steering_angle))
        
        # --- FILTROS DINÁMICOS DE ESTABILIZACIÓN (Anti-Zigzag) ---
        if abs(error) < UMBRAL_PIXELES_MUERTO and area_izq > MIN_PARED_VALIDA and area_der > MIN_PARED_VALIDA: 
            LNM.turn_center()
            steering_angle = 80
        elif abs(steering_angle - 80) <= TOLERANCIA_ANGULO:
            LNM.turn_center()
            steering_angle = 80
        elif steering_angle > 80:
            LNM.turn_right(angle=steering_angle, speed=75)
        elif steering_angle < 80:
            LNM.turn_left(angle=steering_angle, speed=75)

        # =========================================================================
        # CONTEO DE VUELTAS Y FIN DE CARRERA ASÍNCRONO
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

        if current_time - orange_timer > 3.7 and LNM.turning_direction == 2: 
            n = 0

        if current_time - blue_timer > 3.7 and LNM.turning_direction == 1:
            n = 0

        print("Loop count:", loops)

        if loops >= 12 and not end_game_triggered:
            print("🏁 ¡Vuelta 12 alcanzada! Activando tiempo de gracia...")
            end_game_timer = current_time
            end_game_triggered = True

        if end_game_triggered:
            if current_time - end_game_timer >= 1.0:
                print("⏱️ Tiempo de gracia completado. Deteniendo robot de forma segura.")
                break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
