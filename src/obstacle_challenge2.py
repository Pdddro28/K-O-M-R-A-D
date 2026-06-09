import cv2
import time
from vision_controller import ROI, VisionController
from PID_class import PIDController
from mega_pi_controller import *
from constants import *

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

picam2 = LNM.vision  
roi = ROI(0, 50, picam2.image_width, picam2.image_height - 100)
print("Camera started. Press 'q' to quit.")

# --- PID SEPARADOS POR LADO (Sensores ToF) ---
pid_dist_izq = PIDController(kp=3, ki=0.0, kd=1.0) 
pid_dist_der = PIDController(kp=2.9, ki=0.0, kd=1.0) 

# --- PID PARA CENTRADO VISUAL (Diferencia de áreas) ---
pid_vision = PIDController(kp=0.012, ki=0.0, kd=0.004)

# Configuraciones de distancia objetivo
DIST_NORMAL = 20.0
DIST_PEGADO = 12.0  

# --- UMBRALES DE ÁREA CRÍTICOS (FILTROS) ---
MAX_AREA_ROJO = 14000  
MAX_AREA_VERDE = 12000 
MIN_PARED_VALIDA = 350   # Si el área baja de esto, consideramos que la pared se "perdió"

# --- CONFIGURACIÓN DE EMERGENCIA Y TOLERANCIAS ---
DIST_MIN_CHOQUE = 20.0  
TOLERANCIA_ANGULO = 3    # Banda muerta para evitar que el servo tiemble en rectas

# --- CONFIGURACIÓN DE ROIS LATERALES PARA EL CENTRADO ---
roi_izq = ROI(0, 100, 320, 150)
roi_der = ROI(320, 100, 640, 150)

girando = False
SERVO_CENTER = 80   
steering_angle = 80  
color_detectado = "NINGUNO"  # Inicializada aquí para evitar NameError en la primera vuelta

def obtener_areas_negras():
    """ Devuelve el área de las paredes negras a la izquierda y derecha """
    cnt_izq = picam2.find_contours(LNM.mask_black, roi_izq)
    cnt_der = picam2.find_contours(LNM.mask_black, roi_der)
    
    area_izq = picam2.max_contour(cnt_izq, roi_izq)[0]
    area_der = picam2.max_contour(cnt_der, roi_der)[0]
    
    # Telemetría en pantalla
    picam2.draw_roi(roi_izq)
    picam2.draw_roi(roi_der)
    picam2.draw_contours(cnt_izq, roi_izq, (0, 255, 255))
    picam2.draw_contours(cnt_der, roi_der, (0, 255, 255))
    
    return area_izq, area_der

def get_color_signal():
    """ Analiza la cámara y retorna el color detectado aplicando filtros de cercanía """
    red_ctn = picam2.find_contours(LNM.mask_red, roi) 
    green_ctn = picam2.find_contours(LNM.mask_green, roi)
    
    max_red = picam2.max_contour(red_ctn, roi)
    max_green = picam2.max_contour(green_ctn, roi)
    
    # Evaluar Bloque Rojo
    if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
        if 1700 < max_red[0] < MAX_AREA_ROJO:
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))
            return "ROJO"
            
    # Evaluar Bloque Verde
    elif max_green[3] is not None:
        if 200 < max_green[0] < MAX_AREA_VERDE:
            picam2.draw_contours(green_ctn, roi, (0, 255, 0))
            return "VERDE"
            
    return "NINGUNO"

# --- MAIN CONTROL LOOP ---
try:
    while True:
        picam2.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        
        # 1. ACTUALIZAR SENSORES Y VISIÓN PRIMERO
        color_detectado = get_color_signal()
        area_izq, area_der = obtener_areas_negras()
        front_dist, left_dist, right_dist = LNM.get_distances()

        # cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

        # =========================================================================
        # MANIOBRA DE EMERGENCIA (Freno de mano + Reversa)
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0 and color_detectado == "NINGUNO":
            print(f"🚨 ¡FRENO DE MANO! Obstáculo frontal a {front_dist:.2f} cm.")
            LNM.stop(log=False)
            time.sleep(0.05)
            
            angulo_escape_opuesto = 160 - steering_angle
            angulo_escape_opuesto = max(40, min(120, angulo_escape_opuesto))
            
            if angulo_escape_opuesto == 80:
                angulo_escape_opuesto = 60
                
            LNM.move_backward(angle=angulo_escape_opuesto, speed=55)
            time.sleep(0.75)
            
            LNM.turn_center(log=False)
            time.sleep(0.1)
            continue  

        # MANTENER POTENCIA CONSTANTE: Evita caídas de velocidad en el bucle principal
        LNM.move_forward(80)

        # 2. DETECCIÓN DEL SENTIDO INICIAL DE LA PISTA
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                LNM.turning_direction = 2  
            elif LNM.blue_area > 1200:
                LNM.turning_direction = 1  

        # 3. CONTROL DE GIROS EN ESQUINAS CERRADAS
        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
              
        if LNM.black_area < 8000 and girando and front_dist > 80:
            LNM.turn_center()
            girando = False
            steering_angle = 80

        # =========================================================================
        # 4. --- NAVEGACIÓN EN RECTAS Y CURVAS ABIERTAS (Control Híbrido) ---
        # =========================================================================
        if not girando and LNM.turning_direction != 0:
            
            # CASO A: Hay tráfico (Esquivar bloques de colores prioritario mediante ToF)
            if color_detectado in ["ROJO", "VERDE"]:
                target_dinamico = DIST_PEGADO
                if color_detectado == "ROJO":
                    current_dist = min(right_dist, 60.0)
                    lado_correccion = -1  
                    pid_activo = pid_dist_der
                else:
                    current_dist = min(left_dist, 60.0)
                    lado_correccion = 1   
                    pid_activo = pid_dist_izq

                correction = pid_activo.compute(target_dinamico, current_dist)
                steering_angle = int(80 + (correction * lado_correccion))

            # CASO B: Curva/Ronda abierta (Se perdió una de las paredes en la cámara) -> Respaldo ToF
            elif area_izq < MIN_PARED_VALIDA or area_der < MIN_PARED_VALIDA:
                # Si estamos mapeando la pista, usamos el sensor de distancia físico del lado de la pista activo
                if LNM.turning_direction == 2:  # Sentido Naranja -> Seguir pared izquierda
                    current_dist = min(left_dist, 60.0)
                    lado_correccion = 1
                    pid_activo = pid_dist_izq
                else:                           # Sentido Azul -> Seguir pared derecha
                    current_dist = min(right_dist, 60.0)
                    lado_correccion = -1
                    pid_activo = pid_dist_der

                correction = pid_activo.compute(DIST_NORMAL, current_dist)
                steering_angle = int(80 + (correction * lado_correccion))
                
            # CASO C: Pista ideal centrada (Ambas paredes visibles en cámara) -> Control por Visión
            else:
                error_visual = area_izq - area_der
                # El setpoint es 0 para que busque tener las mismas áreas a ambos lados
                correction_visual = pid_vision.compute(0, -error_visual)
                steering_angle = int(80 + correction_visual)

            # --- CORRECCIÓN FINAL Y FILTRADO DE DIRECCIÓN ---
            steering_angle = max(40, min(120, steering_angle))
            
            # Filtro de histéresis: si el quiebre es mínimo, mantén recto para no perder inercia
            if abs(steering_angle - 80) <= TOLERANCIA_ANGULO:
                LNM.turn_center()
                steering_angle = 80  
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

except Exception as e:
    print("🚨 Excepción detectada en el bucle principal:", e)
    LNM.stop()

finally:
    cv2.destroyAllWindows()
    LNM.stop()
