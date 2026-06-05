import cv2
from vision_controller import ROI, VisionController
from PID_class import PIDController
from mega_pi_controller import *
from constants import *

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

picam2 = LNM.vision  
roi = ROI(0, 50, picam2.image_width , picam2.image_height - 100)
print("Camera started. Press 'q' to quit.")

# UN SOLO PID PARA LAS PAREDES (Optimizado)
pid_dist = PIDController(kp=2.9, ki=0.0, kd=1.0)

# Configuraciones de distancia objetivo
DIST_NORMAL = 20.0
DIST_PEGADO = 12.0  # Distancia corta cuando quiere arrimarse a una pared

girando = False
SERVO_CENTER = 80   # Centro neutral físico de tu robot de acuerdo a tus funciones

def get_color_signal():
    """ Analiza la cámara y retorna el color detectado si pasa el umbral """
    red_ctn = picam2.find_contours(LNM.mask_red, roi) 
    green_ctn = picam2.find_contours(LNM.mask_green, roi)
    
    max_red = picam2.max_contour(red_ctn, roi)
    max_green = picam2.max_contour(green_ctn, roi)
    
    # Prioridad por tamaño de área
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if max_red[0] > 1700:
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))
            return "ROJO"
    elif max_green[3] is not None:
        if max_green[0] > 100:
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

        # 1. Detección del sentido inicial de la pista si no se conoce
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  # Pista naranja
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  # Pista azul

        # 2. Leer señal actual de los bloques
        color_detectado = get_color_signal()

        # 3. Control de esquinas (Prioridad de seguridad ante curvas)
        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
            LNM.turn_center()
            girando = False

        # 4. Control de Navegación en Rectas (PID dinámico basado en tu petición)
        if not girando and LNM.turning_direction != 0:
            
            # Valores por defecto (Seguimiento estándar en el medio)
            target_dinamico = DIST_NORMAL
            
            if color_detectado == "ROJO":
                # REGLA: Pegarse a la pared DERECHA
                current_dist = min(right_dist, 60.0)
                target_dinamico = DIST_PEGADO
                lado_correccion = -1  # Geometría del servo para pared derecha
                
            elif color_detectado == "VERDE":
                # REGLA: Pegarse a la pared IZQUIERDA
                current_dist = min(left_dist, 60.0)
                target_dinamico = DIST_PEGADO
                lado_correccion = 1   # Geometría del servo para pared izquierda
                
            else:
                # Si no ve bloques, conserva el comportamiento original de la pista
                if LNM.turning_direction == 2:  # Naranja -> Sigue izquierda
                    current_dist = min(left_dist, 60.0)
                    lado_correccion = 1
                else:                           # Azul -> Sigue derecha
                    current_dist = min(right_dist, 60.0)
                    lado_correccion = -1

            # Calcular el PID con el objetivo ajustado en tiempo real
            correction = pid_dist.compute(target_dinamico, current_dist)
            steering_angle = int(80 + (correction * lado_correccion))
            
            # Límites de seguridad mecánica del servo
            steering_angle = max(40, min(120, steering_angle))
            
            # Actuación de movimiento directo
            if abs(pid_dist.error) < 1.5: 
                LNM.turn_center()
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

finally:
    cv2.destroyAllWindows()