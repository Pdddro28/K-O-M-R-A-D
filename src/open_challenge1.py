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

# --- CONFIGURACIÓN DE VELOCIDAD DINÁMICA ---
VEL_MIN = 50
VEL_MAX = 155
# Referencias físicas de pista dadas por el usuario (suma de ambos lados)
DIST_SUM_MIN = 40.0   # 20cm + 20cm (Caso más cerrado)
DIST_SUM_MAX = 84.0   # 42cm + 42cm (Caso más amplio)
# Referencias estimadas para el área combinada de las ROIs laterales (320x150 cada una)
AREA_SUM_MIN = 800    
AREA_SUM_MAX = 24000  

# --- CONFIGURACIÓN DE EMERGENCIA Y TOLERANCIAS ---
DIST_MIN_CHOQUE = 20.0  
TOLERANCIA_ANGULO = 3    # Banda muerta para evitar que el servo tiemble en rectas

# --- CONFIGURACIÓN DE ROIS LATERALES PARA EL CENTRADO ---
roi_izq = ROI(0, 100, 320, 150)
roi_der = ROI(320, 100, 640, 150)

girando = False
SERVO_CENTER = 80   
steering_angle = 80  
color_detectado = "NINGUNO"  

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

def calcular_velocidad_dinamica(area_i, area_d, ToF_i, ToF_d, ToF_f, en_curva):
    """ Calcula la velocidad óptima entre 50 y 155 basándose en el ancho de la pista """
    # Si estamos ejecutando un giro de esquina forzado, reducimos al mínimo para no derrapar
    if en_curva:
        return VEL_MIN

    # 1. Factor basado en distancia física (ToF)
    # Acotamos los sensores a rangos reales para evitar lecturas infinitas de ruido
    dist_izq_clamped = max(10.0, min(45.0, ToF_i))
    dist_der_clamped = max(10.0, min(45.0, ToF_d))
    suma_dist = dist_izq_clamped + dist_der_clamped
    
    # Normalización del factor ToF (0.0 cerrado, 1.0 completamente abierto)
    factor_tof = (suma_dist - DIST_SUM_MIN) / (DIST_SUM_MAX - DIST_SUM_MIN)
    factor_tof = max(0.0, min(1.0, factor_tof))
    
    # 2. Factor basado en Visión (Área Negra Lateral)
    suma_areas = area_i + area_d
    factor_vision = (suma_areas - AREA_SUM_MIN) / (AREA_SUM_MAX - AREA_SUM_MIN)
    factor_vision = max(0.0, min(1.0, factor_vision))
    
    # Fusionamos ambos factores (60% peso a los sensores de distancia, 40% a la visión)
    factor_pista = (factor_tof * 0.6) + (factor_vision * 0.4)
    
    # Calcular velocidad base interpolada
    velocidad = int(VEL_MIN + (VEL_MAX - VEL_MIN) * factor_pista)
    
    # 3. Atenuación por proximidad frontal (Filtro de seguridad proactivo)
    # Si nos acercamos a una pared de frente (entre 55cm y 120cm), reducimos linealmente la velocidad
    if 55.0 < ToF_f < 120.0:
        factor_freno = (ToF_f - 55.0) / (120.0 - 55.0)
        velocidad = int(VEL_MIN + (velocidad - VEL_MIN) * factor_freno)
        
    return max(VEL_MIN, min(VEL_MAX, velocidad))

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

        # =========================================================================
        # CÁLCULO Y APLICACIÓN DE VELOCIDAD DINÁMICA
        # =========================================================================
        velocidad_calculada = calcular_velocidad_dinamica(
            area_izq, area_der, left_dist, right_dist, front_dist, girando
        )
        LNM.move_forward(velocidad_calculada)

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
