import cv2
from vision_controller import ROI, VisionController
from PID_class import PIDController
from mega_pi_controller import *
from constants import *

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

# Initialize Picamera2
picam2 = LNM.vision  
roi = ROI(0, 50, picam2.image_width, picam2.image_height - 100)
print("Camera started. Press 'q' to quit.")

# Eliminamos los PID individuales de los bloques. Solo necesitamos el de distancia.
# Ajusta Kp, Ki, Kd para que el cambio de carril sea suave y no un volantazo brusco.
pid_dist = PIDController(kp=2.5, ki=0.0, kd=0.8)

# Configuraciones de carril (Modifica estos valores según el ancho de tu pista)
DIST_CENTRO = 20.0   # Distancia normal cuando no hay bloques
DIST_CERCA = 12.0    # Distancia cuando debe pegarse a la pared
DIST_LEJOS = 42.0    # Distancia cuando debe alejarse de la pared (ir al carril contrario)

girando = False
SERVO_CENTER = 80    # Centralizado según tu lógica de abajo

def check_traffic_lights():
    """ 
    Esta función solo detecta qué color domina y define 
    el carril. Ya no controla el servo directamente.
    """
    red_ctn = picam2.find_contours(LNM.mask_red, roi) 
    green_ctn = picam2.find_contours(LNM.mask_green, roi)
    
    max_red = picam2.max_contour(red_ctn, roi)
    max_green = picam2.max_contour(green_ctn, roi)
    
    # Umbral de área para confirmar que el bloque es real y está lo suficientemente cerca
    UMBRAL_AREA_ROJO = 1700
    UMBRAL_AREA_VERDE = 1200 

    # Prioridad al bloque con mayor área visible
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if max_red[0] > UBRAL_AREA_ROJO:
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))
            return "ROJO"
            
    elif max_green[3] is not None:
        if max_green[0] > UMBRAL_AREA_VERDE:
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

        # 1. DETECCIÓN DE SENTIDO DE LA PISTA (Líneas del suelo)
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  # Pista Naranja (Sigue pared IZQUIERDA)
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  # Pista Azul (Sigue pared DERECHA)

        # 2. DETECCIÓN DE BLOQUES (SEÑALES DE TRÁFICO)
        bloque_detectado = check_traffic_lights()

        # 3. CONTROL DE GIRO EN ESQUINAS (Giro fijo prioritario)
        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
            LNM.turn_center()
            girando = False

        # 4. NAVEGACIÓN POR PID EN RECTAS (Mantener carril dinámico)
        if not girando and LNM.turning_direction != 0:
            
            # Inicializamos variables de control
            current_dist = 20.0
            lado_correccion = 1
            target_dinamico = DIST_CENTRO

            # --- CASO PISTA NARANJA (Sigue Pared Izquierda) ---
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                lado_correccion = 1  # (+) -> Derecha, (-) -> Izquierda
                
                if bloque_detectado == "VERDE":
                    target_dinamico = DIST_CERCA  # Carril Izquierdo: se pega a la izquierda
                elif bloque_detectado == "ROJO":
                    target_dinamico = DIST_LEJOS  # Carril Derecho: se aleja a la derecha
                else:
                    target_dinamico = DIST_CENTRO # Sin bloques: va al centro de su zona

            # --- CASO PISTA AZUL (Sigue Pared Derecha) ---
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                lado_correccion = -1 # (+) -> Izquierda, (-) -> Derecha
                
                if bloque_detectado == "VERDE":
                    target_dinamico = DIST_LEJOS  # Carril Izquierdo: se aleja a la izquierda
                elif bloque_detectado == "ROJO":
                    target_dinamico = DIST_CERCA  # Carril Derecho: se pega a la derecha
                else:
                    target_dinamico = DIST_CENTRO # Sin bloques: va al centro de su zona

            # Calcular la corrección basándonos en el Target Dinámico modificado por el bloque
            correction = pid_dist.compute(target_dinamico, current_dist)
            steering_angle = int(SERVO_CENTER + (correction * lado_correccion))
            
            # Limitación física por seguridad del servo
            steering_angle = max(40, min(120, steering_angle))
            
            # Ejecutar el movimiento
            if abs(pid_dist.error) < 1.5: 
                LNM.turn_center()
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

finally:
    cv2.destroyAllWindows()