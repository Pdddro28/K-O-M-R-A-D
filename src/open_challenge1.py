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

# --- CONFIGURACIÓN DEL FRENO DE MANO DE EMBENCIA ---
DIST_MIN_CHOQUE = 25.0  

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

        # =========================================================================
        # FRENO DE MANO Y RETROCESO CONTROLADO EN ÁNGULO POR PD
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
            print(f"🚨 ¡OBSTÁCULO! Retroceso por tiempo fijo (0.75s) con dirección asistida por PD.")
            LNM.stop(log=False)
            time.sleep(0.05)
            
            start_reverse = time.time()
            # El bucle se ejecuta estrictamente durante 0.75 segundos a velocidad fija de 85
            while (time.time() - start_reverse) < 0.75:
                LNM.vision.receive_image()
                black_areas = obtener_areas()
                _, left_dist, right_dist = LNM.get_distances()
                
                area_izq_rev = black_areas[1]
                area_der_rev = black_areas[0]
                
                # Mismo cálculo de error híbrido (Cámara o Ultrasonidos si falta visión)
                if area_izq_rev > MIN_PARED_VALIDA and area_der_rev > MIN_PARED_VALIDA:
                    error_rev = area_izq_rev - area_der_rev
                else:
                    error_rev = (right_dist - left_dist) * 350
                
                # Ejecución del algoritmo PD para ajustar el ángulo de las ruedas
                derivative_rev = error_rev - prev_error
                correction_rev = (Kp_hybrid * error_rev) + (Kd_hybrid * derivative_rev)
                prev_error = error_rev
                
                # [INVERSIÓN CINEMÁTICA]: Al ir marcha atrás, restamos la corrección para 
                # que el giro del coche respecto a las paredes sea el correcto.
                steering_angle_rev = int(80 - correction_rev)
                steering_angle_rev = max(40, min(120, steering_angle_rev))
                
                # Ejecuta el movimiento hacia atrás actualizando el ángulo dinámicamente
                LNM.move_backward(angle=steering_angle_rev, speed=85)
                time.sleep(0.02)
            
            LNM.turn_center(log=False)
            prev_error = 0.0
            time.sleep(0.1)
            continue  # Volver al inicio del bucle principal (marcha adelante)

        # Avance continuo con la potencia establecida para el Open Challenge
        LNM.move_forward(speed=130) 

        # Detección del sentido inicial de la pista
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # =========================================================================
        # SISTEMA DE NAVEGACIÓN PD HÍBRIDO (Con activación retardada)
        # =========================================================================
        if tiempo_primer_loop is not None and (current_time - tiempo_primer_loop) > 0.5:
            area_izq = black_areas[1]
            area_der = black_areas[0]

            if area_izq > MIN_PARED_VALIDA and area_der > MIN_PARED_VALIDA:
                error = area_izq - area_der
            else:
                error = (right_dist - left_dist) * 350

            derivative = error - prev_error
            correction = (Kp_hybrid * error) + (Kd_hybrid * derivative)
            prev_error = error
            
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
        else:
            # Modo salida pasiva: Forzamos dirección recta y reseteamos históricos
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
                print("⏱️ ¡Primer loop contado! Activando cuenta regresiva de 0.5s para el PD.")

        if LNM.blue_area > 500 and n == 0 and LNM.turning_direction == 1: 
            blue_timer = current_time
            n = 1
            loops += 1
            if loops == 1 and tiempo_primer_loop is None:
                tiempo_primer_loop = current_time
                print("⏱️ ¡Primer loop contado! Activando cuenta regresiva de 0.5s para el PD.")

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
