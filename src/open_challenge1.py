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

# --- CONFIGURACIÓN DE BIAS DINÁMICO POR ULTRASONIDO ---
DIST_DESEADA_PARED_OPUESTA = 15.0  # El coche intentará mantener estos cm con la pared externa
Kp_pared = 1.2                     # Qué tan fuerte va a corregir para alejarse de la pared incorrecta
DIST_MIN_PARA_PERMITIR_GIRO = 16.0 # Candado: Si está más cerca de esto de la pared interior, NO gira

steering_angle = 80     

# --- VARIABLES DE TOLERANCIA (EVITAR ZIGZAGUEO) ---
UMBRAL_PIXELES_MUERTO = 150  
TOLERANCIA_ANGULO = 3        

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
        draw_rois()

        cv2.imshow('Vision HD - Posicion Corregida', LNM.vision.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()

        # Avanzamos a velocidad de competencia
        LNM.move_forward(speed=130) 

        # 1. TRACK TYPE DETECTION
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # 2. CORNER DETECTION (Detección de Esquinas para Cruzar)
        # Se añade el CANDADO DE SEGURIDAD LATERAL para evitar que gire si está ahogado contra la pared
        puede_girar = True
        if LNM.turning_direction == 1 and left_dist < DIST_MIN_PARA_PERMITIR_GIRO:  # Vuelta Izquierda
            puede_girar = False
        print(f"LNM.turning_direction: {LNM.turning_direction}")
        if LNM.turning_direction == 2 and right_dist < DIST_MIN_PARA_PERMITIR_GIRO: # Vuelta Derecha
            print("Pone puede_girar en False")
            puede_girar = False

        if front_dist < 55 and not girando and LNM.black_area > 11000 and LNM.turning_direction != 0 and puede_girar:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
        elif front_dist < 55 and not girando and LNM.black_area > 11000 and LNM.turning_direction != 0 and not puede_girar:
            print("⚠️ Intento de giro bloqueado: Demasiado cerca de la pared interna. Corrigiendo posición...")
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
           LNM.turn_center()
           girando = False
           conteo = False
           steering_angle = 80

        # =========================================================================
        # ESTRATEGIA DE CENTRADO CON RECHAZO DINÁMICO DE PAREDES (HUGGING OPUESTO)
        # =========================================================================
        if not girando and LNM.turning_direction != 0:
            # Error puro de la cámara
            error = black_areas[1] - black_areas[0]
            
            # Control PID Visual base
            integral += error
            integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
            derivative = error - prev_error
            correction = (Kp_vision * error) + (Ki_vision * integral) + (Kd_vision * derivative)
            prev_error = error
            
            # Ángulo base dictado por la cámara
            steering_angle = int(80 + correction)
            
            # --- INYECCIÓN DE BIAS PROPORCIONAL POR ULTRASONIDO ---
            if LNM.turning_direction == 1:  # Sentido Izquierdo -> Pegarse a la DERECHA (Alejarse de la izquierda)
                if left_dist < 35.0 and left_dist > 1.0:
                    # Si se acerca a la pared izquierda, sumamos un empuje hacia la derecha
                    empuje_derecha = (35.0 - left_dist) * Kp_pared
                    steering_angle += int(empuje_derecha)
                    
            elif LNM.turning_direction == 2:  # Sentido Derecho -> Pegarse a la IZQUIERDA (Alejarse de la derecha)
                if right_dist < 35.0 and right_dist > 1.0:
                    # Si se acerca a la pared derecha, restamos un empuje para ir a la izquierda
                    empuje_izquierda = (35.0 - right_dist) * Kp_pared
                    steering_angle -= int(empuje_izquierda)

            # Acotamos los límites físicos del servo
            steering_angle = max(40, min(120, steering_angle))
            print(f"Distancias -> L: {left_dist:.1f}, R: {right_dist:.1f} | Ángulo Final: {steering_angle}")
            
            # --- FILTROS DE TOLERANCIA ---
            if abs(error) < UMBRAL_PIXELES_MUERTO and (left_dist >= 30 and right_dist >= 30): 
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

        # =========================================================================
        # 3. LOGIC AND LAP COUNTER
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
