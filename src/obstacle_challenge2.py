import cv2
from vision_controller import ROI, VisionController
from PID_class import PIDController
from mega_pi_controller import *
from constants import *

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

# Inicializar Picamera2
picam2 = LNM.vision  
roi = ROI(0, 50, picam2.image_width, picam2.image_height - 100)
print("Camera started. Press 'q' to quit.")

# UN SOLO PID CONTROLADOR DE DISTANCIA (Maneja las paredes)
# Ajusta tus constantes Kp y Kd aquí. Un Ki de 0 es ideal para evitar acumulación de error en rectas.
pid_dist = PIDController(kp=2.5, ki=0.0, kd=0.8)

# --- SETPOINTS REGLAMENTARIOS DE CARRIL (Modifica según el ancho real de tu pista) ---
DIST_CENTRO = 20.0   # Trayectoria base (Centro del carril asignado)
DIST_PEGADO = 12.0   # Desplazamiento hacia la pared (Carril correspondiente)
DIST_ALEJADO = 45.0  # Desplazamiento opuesto a la pared (Cambio de carril completo)

girando = False
SERVO_CENTER = 80    # Centro físico configurado en tu robot

def check_traffic_signals():
    """
    Analiza la cámara como un lector de señales de tráfico WRO.
    Retorna el color dominante si el bloque es real (área suficiente).
    """
    red_ctn = picam2.find_contours(LNM.mask_red, roi) 
    green_ctn = picam2.find_contours(LNM.mask_green, roi)
    
    max_red = picam2.max_contour(red_ctn, roi)
    max_green = picam2.max_contour(green_ctn, roi)
    
    # Umbrales para evitar falsos positivos con ruidos del fondo
    UMBRAL_ROJO = 1700
    UMBRAL_VERDE = 1200 

    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if max_red[0] > UMBRAL_ROJO:
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))
            return "ROJO"
            
    elif max_green[3] is not None:
        if max_green[0] > UMBRAL_VERDE:
            picam2.draw_contours(green_ctn, roi, (0, 255, 0))
            return "VERDE"
            
    return "NINGUNO"

try:
    while True:
        picam2.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
            
        picam2.draw_roi(roi) 
        LNM.vision.draw_roi(LNM.rois[0]) 
        LNM.vision.draw_roi(LNM.rois[1]) 
        cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        LNM.move_forward(65)
        front_dist, left_dist, right_dist = LNM.get_distances()

        # 1. DIRECCIÓN DEL SENTIDO DEL CIRCUITO (Líneas del suelo)
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  # Sentido horario (Sigue pared IZQUIERDA)
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  # Sentido antihorario (Sigue pared DERECHA)

        # 2. EVALUACIÓN DE SEÑALES (CÁMARA)
        bloque_actual = check_traffic_signals()

        # 3. CONTROL DE ESQUINAS (Prioridad absoluta para evitar choques frontales)
        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
            LNM.turn_center()
            girando = False

        # 4. TRATAMIENTO DE CARRILES CON PID (Navegación en rectas)
        if not girando and LNM.turning_direction != 0:
            
            # Variables de control por defecto
            current_dist = 20.0
            lado_correccion = 1
            target_dinamico = DIST_CENTRO

            # --- CASO A: SENTIDO HORARIO (Control basado en Pared Izquierda) ---
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                lado_correccion = 1  # (+) -> Gira a la derecha, (-) -> Gira a la izquierda
                
                if bloque_actual == "VERDE":
                    # Reglamento: Bloque verde se pasa por la DERECHA del bloque (Acercarse a la pared IZQUIERDA)
                    target_dinamico = DIST_PEGADO  
                elif bloque_actual == "ROJO":
                    # Reglamento: Bloque rojo se pasa por la IZQUIERDA del bloque (Alejarse de la pared IZQUIERDA)
                    target_dinamico = DIST_ALEJADO  
                else:
                    target_dinamico = DIST_CENTRO

            # --- CASO B: SENTIDO ANTIHORARIO (Control basado en Pared Derecha) ---
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                lado_correccion = -1 # Inversión geométrica para el servo
                
                if bloque_actual == "VERDE":
                    # Reglamento: Bloque verde se pasa por la IZQUIERDA del bloque (Alejarse de la pared DERECHA)
                    target_dinamico = DIST_ALEJADO  
                elif bloque_actual == "ROJO":
                    # Reglamento: Bloque rojo se pasa por la DERECHA del bloque (Acercarse a la pared DERECHA)
                    target_dinamico = DIST_PEGADO  
                else:
                    target_dinamico = DIST_CENTRO

            # Ejecución matemática del PID Único de Distancia
            correction = pid_dist.compute(target_dinamico, current_dist)
            steering_angle = int(SERVO_CENTER + (correction * lado_correccion))
            
            # Límites físicos de seguridad estructural de la dirección
            steering_angle = max(40, min(120, steering_angle))
            
            # Actuación sobre los motores del MegaPi
            if abs(pid_dist.error) < 1.5: 
                LNM.turn_center()
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

finally:
    cv2.destroyAllWindows()