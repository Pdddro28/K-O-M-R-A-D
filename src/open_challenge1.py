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

# --- CONFIGURACIÓN DE APAGADO / ASIMETRÍA DE PAREDES (WALL HUGGING) ---
# Incrementa estos valores si quieres que se pegue MÁS a la pared exterior
OFFSET_VISION = 600      # Desviación objetivo en píxeles para la cámara
OFFSET_TOF = 12          # Desviación objetivo en centímetros para los ultrasonidos

# --- VARIABLES DE TOLERANCIA Y FILTRADO ---
UMBRAL_PIXELES_MUERTO = 150  # Ignora variaciones de área insignificantes
TOLERANCIA_ANGULO = 3        # Banda muerta del servo para tramos rectos
MIN_PARED_VALIDA = 350       # Límite por debajo del cual se considera pared perdida en cámara

# --- CONTROL DE ACTIVACIÓN RETARDADA DEL PD ---
tiempo_primer_loop = None    # Almacenará el timestamp exacto del primer cruce

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
        # Adquisición de datos de sensores, vídeo y tiempo actual del ciclo
        current_time = time.time()
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        
        black_areas = obtener_areas()
        front_dist, left_dist, right_dist = LNM.get_distances()

        # Avance continuo con la potencia establecida para el Open Challenge
        LNM.move_forward(speed=130) 

        # Detección del sentido inicial de la pista
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # =========================================================================
        # SISTEMA DE NAVEGACIÓN PD HÍBRIDO ASIMÉTRICO (Apego a Pared Exterior)
        # =========================================================================
        if tiempo_primer_loop is not None and (current_time - tiempo_primer_loop) > 0.5:
            area_izq = black_areas[1]
            area_der = black_areas[0]

            # Inicializamos desfases (por defecto 0 si no se ha detectado sentido)
            target_offset_vision = 0
            target_offset_tof = 0

            # Asignación de offsets según el sentido de la pista
            if LNM.turning_direction == 2:    # Naranja primero -> Pegarse a la IZQUIERDA
                target_offset_vision = OFFSET_VISION
                target_offset_tof = OFFSET_TOF
            elif LNM.turning_direction == 1:  # Azul primero -> Pegarse a la DERECHA
                target_offset_vision = -OFFSET_VISION
                target_offset_tof = -OFFSET_TOF

            # Cálculo del Error aplicando la desviación del objetivo (Offset)
            if area_izq > MIN_PARED_VALIDA and area_der > MIN_PARED_VALIDA:
                # El PD se estabiliza cuando la diferencia de píxeles iguala al offset
                error = (area_izq - area_der) - target_offset_vision
            else:
                # El PD se estabiliza cuando la diferencia de distancia en cm iguala al offset
                error = ((right_dist - left_dist) - target_offset_tof) * 350

            # Algoritmo de control Proporcional-Derivativo
            derivative = error - prev_error
            correction = (Kp_hybrid * error) + (Kd_hybrid * derivative)
            prev_error = error
            
            steering_angle = int(80 + correction)
            steering_angle = max(40, min(120, steering_angle))
            
            # --- FILTROS DINÁMICOS DE ESTABILIZACIÓN ---
            # Solo aplicamos el centrado total si no hay un sentido de pista bloqueado (dirección = 0)
            if LNM.turning_direction == 0 and abs(error) < UMBRAL_PIXELES_MUERTO:
                LNM.turn_center()
                steering_angle = 80
            elif abs(steering_angle - 80) <= TOLERANCIA_ANGULO:
                LNM.turn_center()
                steering_angle = 80
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=75)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=75)
        else:
            # Modo salida pasiva: Forzamos dirección recta durante la primera recta de largada
            LNM.turn_center()
            steering_angle = 80
            prev_error = 0.0

        # =========================================================================
        # CONTEO DE VUELTAS Y FIN DE CARRERA ASÍNCRONO
        # =========================================================================
        if LNM.orange_area > 500 and n == 0 and LNM.turning_direction == 2: 
            orange_timer = current_time
            n = 1
            loops += 1
            if loops == 1 and tiempo_primer_loop is None:
                tiempo_primer_loop = current_time
                print("⏱️ ¡Primer loop contado! Activando cuenta regresiva de 0.5s para el PD Asimétrico (Izquierda).")

        if LNM.blue_area > 500 and n == 0 and L
