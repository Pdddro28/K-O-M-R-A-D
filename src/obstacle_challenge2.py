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

# --- PID SEPARADOS POR LADO ---
# Como al verde (lado izquierdo) le cuesta más, aumentamos su Kp a 3.5 (ajusta según pruebes)
pid_dist_izq = PIDController(kp=3, ki=0.0, kd=1.0) 
# Al rojo (lado derecho) lo dejamos con tus valores base que ya funcionaban bien
pid_dist_der = PIDController(kp=2.9, ki=0.0, kd=1.0) 

# Configuraciones de distancia objetivo
DIST_NORMAL = 20.0
DIST_PEGADO = 12.0  

girando = False
SERVO_CENTER = 80   

def get_color_signal():
    """ Analiza la cámara y retorna el color detectado """
    red_ctn = picam2.find_contours(LNM.mask_red, roi) 
    green_ctn = picam2.find_contours(LNM.mask_green, roi)
    
    max_red = picam2.max_contour(red_ctn, roi)
    max_green = picam2.max_contour(green_ctn, roi)
    
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if max_red[0] > 1700:
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))
            return "ROJO"
    elif max_green[3] is not None:
        if max_green[0] > 200:
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

        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  

        color_detectado = get_color_signal()

        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
            LNM.turn_center()
            girando = False

        # --- NAVEGACIÓN EN RECTAS CON PID SEPARADOS ---
        if not girando and LNM.turning_direction != 0:
            
            target_dinamico = DIST_NORMAL
            
            if color_detectado == "ROJO":
                # Regla Rojo: Pegarse a la derecha -> Usa PID Derecho
                current_dist = min(right_dist, 60.0)
                target_dinamico = DIST_PEGADO
                lado_correccion = -1  
                pid_activo = pid_dist_der
                
            elif color_detectado == "VERDE":
                # Regla Verde: Pegarse a la izquierda -> Usa PID Izquierdo
                current_dist = min(left_dist, 60.0)
                target_dinamico = DIST_PEGADO
                lado_correccion = 1   
                pid_activo = pid_dist_izq
                
            else:
                # Comportamiento por defecto según la línea detectada en el suelo
                if LNM.turning_direction == 2:  # Naranja -> Sigue izquierda
                    current_dist = min(left_dist, 60.0)
                    lado_correccion = 1
                    pid_activo = pid_dist_izq
                else:                           # Azul -> Sigue derecha
                    current_dist = min(right_dist, 60.0)
                    lado_correccion = -1
                    pid_activo = pid_dist_der

            # Calcular la corrección usando el objeto PID seleccionado dinámicamente
            correction = pid_activo.compute(target_dinamico, current_dist)
            steering_angle = int(80 + (correction * lado_correccion))
            
            steering_angle = max(40, min(120, steering_angle))
            
            if abs(pid_activo.error) < 1.5: 
                LNM.turn_center()
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

finally:
    cv2.destroyAllWindows()