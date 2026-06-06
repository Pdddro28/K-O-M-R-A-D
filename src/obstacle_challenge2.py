import cv2
import time
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
pid_dist_izq = PIDController(kp=3, ki=0.0, kd=1.0) 
pid_dist_der = PIDController(kp=2.9, ki=0.0, kd=1.0) 

# Configuraciones de distancia objetivo
DIST_NORMAL = 20.0
DIST_PEGADO = 12.0  

# --- UMBRALES DE ÁREA CRÍTICOS (FILTROS) ---
MAX_AREA_ROJO = 14000   # Si el bloque rojo es más grande que esto, ya estamos al lado; ignorar
MAX_AREA_VERDE = 12000  # Si el bloque verde es más grande que esto, ya estamos al lado; ignorar

# --- CONFIGURACIÓN DE EMERGENCIA ---
DIST_MIN_CHOQUE = 20.0  # Distancia en cm para activar el retroceso de emergencia

girando = False
SERVO_CENTER = 80   

def get_color_signal():
    """ Analiza la cámara y retorna el color detectado aplicando filtros de cercanía """
    red_ctn = picam2.find_contours(LNM.mask_red, roi) 
    green_ctn = picam2.find_contours(LNM.mask_green, roi)
    
    max_red = picam2.max_contour(red_ctn, roi)
    max_green = picam2.max_contour(green_ctn, roi)

    
    # Evaluar Bloque Rojo
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        # Solo responde si está en el rango ideal (ni muy lejos ni excesivamente cerca)
        print(f"Área roja detectada: {max_red[0]}")
        if 1700 < max_red[0] < MAX_AREA_ROJO:
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))
            return "ROJO"
            
    # Evaluar Bloque Verde
    elif max_green[3] is not None:
        # Solo responde si está en el rango ideal 
        print(f"Área verde detectada: {max_green[0]}")
        if 200 < max_green[0] < MAX_AREA_VERDE:
            picam2.draw_contours(green_ctn, roi, (0, 255, 0))
            return "VERDE"
            
    return "NINGUNO"

steering_angle = 80  # Rastrea la última dirección calculada por el PID

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

        # Leer distancias de los sensores ToF
        front_dist, left_dist, right_dist = LNM.get_distances()

        # =========================================================================
        # MANIOBRA DE EMERGENCIA (Usando tu nuevo método move_backward)
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
            print(f"¡EMERGENCIA! Frente obstruido a {front_dist:.2f} cm.")
            
            # Calcular ángulo opuesto en espejo respecto al centro físico (80)
            angulo_escape_opuesto = 160 - steering_angle
            angulo_escape_opuesto = max(40, min(120, angulo_escape_opuesto))
            
            # Si el robot venía totalmente recto, forzamos un quiebre hacia la izquierda
            if angulo_escape_opuesto == 80:
                angulo_escape_opuesto = 60
                
            print(f"Ángulo previo: {steering_angle} | Escapando en reversa con ángulo: {angulo_escape_opuesto}")
            
            # Llamamos a tu método modificado: primero el ángulo, luego la velocidad (positiva para la marcha)
            LNM.move_backward(angle=angulo_escape_opuesto, speed=55)
            time.sleep(0.7)  # Tiempo de ejecución de la reversa para despejar espacio
            
            # Enderezar ruedas antes de reanudar la marcha adelante
            LNM.turn_center(log=False)
            time.sleep(0.1)
            
            continue  # Reinicia el ciclo, evaluando la pista desde la nueva posición

        # Si el camino está despejado, marcha adelante normal
        LNM.move_forward(65)

        # 1. Detección del sentido inicial de la pista si no se conoce
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  

        # 2. Obtener el estado del tráfico filtrado por la cámara
        color_detectado = get_color_signal()

        # 3. Control de giros en las esquinas de la pista
        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
            LNM.turn_center()
            girando = False

        # 4. --- NAVEGACIÓN EN RECTAS CON PID SEPARADOS ---
        if not girando and LNM.turning_direction != 0:
            
            target_dinamico = DIST_NORMAL
            
            if color_detectado == "ROJO":
                current_dist = min(right_dist, 60.0)
                target_dinamico = DIST_PEGADO
                lado_correccion = -1  
                pid_activo = pid_dist_der
                
            elif color_detectado == "VERDE":
                current_dist = min(left_dist, 60.0)
                target_dinamico = DIST_PEGADO
                lado_correccion = 1   
                pid_activo = pid_dist_izq
                
            else:
                if LNM.turning_direction == 2:
                    current_dist = min(left_dist, 60.0)
                    lado_correccion = 1
                    pid_activo = pid_dist_izq
                else:
                    current_dist = min(right_dist, 60.0)
                    lado_correccion = -1
                    pid_activo = pid_dist_der

            # Calcular la corrección y actualizar la variable para el escape inteligente
            correction = pid_activo.compute(target_dinamico, current_dist)
            steering_angle = int(80 + (correction * lado_correccion))
            steering_angle = max(40, min(120, steering_angle))
            
            if abs(pid_activo.error) < 1.5: 
                LNM.turn_center()
                steering_angle = 80  
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

finally:
    cv2.destroyAllWindows()