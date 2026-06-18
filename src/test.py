from mega_pi_controller import *
from constants import *
import cv2 
import time

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

# Sobrescribimos/Añadimos las ROIs necesarias para obstáculos en este archivo
OPEN_ROI_CENTER = ROI(200, 20, 430, 200) # Tu ROI frontal original
ROI_LINES = ROI(200, 300, 440, 350)       # Tu ROI de líneas original

# NUEVA ROI: Enfocada en el carril central medio para detectar pilares a tiempo
# Evita los bordes de la pista (X de 140 a 500) y el parachoques bajo (Y de 130 a 290)
ROI_OBSTACULOS = ROI(30, 30, 610, 320)

while not LNM.start():
    pass
running = True

# --- TIMERS Y CONTADORES ---
orange_timer = time.time()
blue_timer = time.time()
loops = 0
n = 0

# --- PARÁMETROS PID PARA CENTRADO DE LÍNEAS (Ronda Abierta) ---
Kp_vision = 0.015    
Ki_vision = 0.0
Kd_vision = 0.005   
prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 

# --- PARÁMETROS PID EXCLUSIVOS PARA EVITAR OBSTÁCULOS ---
Kp_obstaculo = 0.52   # Más agresivo porque el rango de error en píxeles es menor
Kd_obstaculo = 0.08   # Amortigua el giro para evitar que la cola derrape y toque el pilar

# --- MÁQUINA DE ESTADOS PARA OBSTÁCULOS ---
# Estados: "LINEAL" (Centrado de líneas), "ESQUIVANDO" (Viendo pilar), "REBASANDO" (Memoria ultrasonido)
estado_carrera = "LINEAL"
memoria_lado = None  # Guardará "IZQUIERDA" o "DERECHA"

# --- CONFIGURACIÓN DE VELOCIDAD Y AJUSTES (MODERADA A 85) ---
VELOCIDAD_BASE = 70
DIST_MIN_CHOQUE = 12.0  
steering_angle = 80     

UMBRAL_PIXELES_MUERTO = 150  
TOLERANCIA_ANGULO = 3       

# --- FIN DE CARRERA ---
end_game_triggered = False
end_game_timer = 0.0

# --- ROIs LATERALES (Para centrado lineal) ---
roi_izq = ROI(0, 100, 320, 150)  
roi_der = ROI(320, 100, 640, 150)  

# --- HELPERS LOCALES (Para no modificar MegaPiController ni VisionController) ---
def obtener_areas_lineas():
    blackcnt_left = LNM.vision.find_contours(LNM.mask_black, roi_izq)
    blackcnt_right = LNM.vision.find_contours(LNM.mask_black, roi_der)
    area_right = LNM.vision.max_contour(blackcnt_right, roi_der)[0]
    area_left = LNM.vision.max_contour(blackcnt_left, roi_izq)[0]
    return [area_right, area_left]

def procesar_obstaculos():
    """Busca pilares rojos y verdes en la nueva ROI_OBSTACULOS"""
    cnt_rojo = LNM.vision.find_contours(LNM.mask_red, ROI_OBSTACULOS)
    cnt_verde = LNM.vision.find_contours(LNM.mask_green, ROI_OBSTACULOS)
    
    # max_contour devuelve [area, x, y, contorno]
    datos_rojo = LNM.vision.max_contour(cnt_rojo, ROI_OBSTACULOS)
    datos_verde = LNM.vision.max_contour(cnt_verde, ROI_OBSTACULOS)
    print(f"🔴 Rojo: Área={datos_rojo[0]}, X={datos_rojo[1]}, Y={datos_rojo[2]}")
    print(f"🟢 Verde: Área={datos_verde[0]}, X={datos_verde[1]}, Y={datos_verde[2]}")
    
    return datos_rojo, datos_verde

def draw_all_rois(datos_rojo, datos_verde):
    """Dibuja en pantalla para telemetría visual"""
    LNM.vision.draw_roi(roi_izq)
    LNM.vision.draw_roi(roi_der)
    LNM.vision.draw_roi(ROI_OBSTACULOS)
    
    # Si hay pilares, dibuja sus contornos en la pantalla de debug
    if datos_rojo[3] is not None:
        LNM.vision.draw_contours([datos_rojo[3]], ROI_OBSTACULOS, (0, 0, 255)) # Rojo
    if datos_verde[3] is not None:
        LNM.vision.draw_contours([datos_verde[3]], ROI_OBSTACULOS, (0, 255, 0)) # Verde

# --- MAIN CONTROL LOOP ---
while running:
    try:
        # 1. Adquisición de imágenes y telemetría de sensores estándar
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        # Distancias físicas de los ultrasonidos
        front_dist, left_dist, right_dist = LNM.get_distances()
        
        # Procesar datos de visión localizados
        black_areas = obtener_areas_lineas()
        datos_rojo, datos_verde = procesar_obstaculos()
        
        # Dibujar elementos en el frame
        draw_all_rois(datos_rojo, datos_verde)
        cv2.imshow('Vision HD - Obstacle Challenge', LNM.vision.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # cv2.imshow('Vision HD - Obstacle Challenge', LNM.vision.frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'): break

        # =========================================================================
        # FRENO DE MANO DE EMERGENCIA
        # =========================================================================
        if front_dist < DIST_MIN_CHOQUE and front_dist > 1.0:
            print(f"🚨 ¡FRENO DE MANO! Frente obstruido a {front_dist:.2f} cm.")
            LNM.stop(log=False)
            time.sleep(0.05)
            
            angulo_escape_opuesto = 160 - steering_angle
            angulo_escape_opuesto = max(40, min(120, angulo_escape_opuesto))
            if angulo_escape_opuesto == 80:
                angulo_escape_opuesto = 60
                
            LNM.move_backward(angle=angulo_escape_opuesto, speed=85)
            time.sleep(0.75)
            LNM.turn_center(log=False)
            prev_error = 0.0
            integral = 0.0
            estado_carrera = "LINEAL" # Resetear estado por seguridad
            time.sleep(0.1)
            continue

        # Mantenemos la velocidad constante y moderada recomendada para este reto
        LNM.move_forward(speed=VELOCIDAD_BASE) 

        # Detección del sentido de la pista (Líneas de las esquinas)
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1

        # =========================================================================
        # MÁQUINA DE ESTADOS: NAVEGACIÓN Y EVASIÓN DE OBSTÁCULOS
        # =========================================================================
        
        # --- ESTADO 1: LINEAL (Centrado mediante diferencia de áreas de líneas) ---
        if estado_carrera == "LINEAL":
            # Verificar si entra un obstáculo en el radar visual (Umbral de área > 250 píxeles)
            if datos_verde[0] > 250 and datos_verde[0] >= datos_rojo[0]:
                estado_carrera = "ESQUIVANDO"
                memoria_lado = "IZQUIERDA" # El verde se esquiva por la izquierda
                prev_error = 0.0
            elif datos_rojo[0] > 250 and datos_rojo[0] > datos_verde[0]:
                estado_carrera = "ESQUIVANDO"
                memoria_lado = "DERECHA"   # El rojo se esquiva por la derecha
                prev_error = 0.0
            
            # Si no hay obstáculos a la vista, ejecuta el PID Lineal original
            else:
                error = black_areas[1] - black_areas[0]
                integral += error
                integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
                derivative = error - prev_error
                correction = (Kp_vision * error) + (Ki_vision * integral) + (Kd_vision * derivative)
                prev_error = error
                
                steering_angle = int(80 + correction)
                steering_angle = max(40, min(120, steering_angle))
                
                if abs(error) < UMBRAL_PIXELES_MUERTO or abs(steering_angle - 80) <= TOLERANCIA_ANGULO:
                    LNM.turn_center()
                    steering_angle = 80
                elif steering_angle > 80:
                    LNM.turn_right(angle=steering_angle, speed=VELOCIDAD_BASE)
                elif steering_angle < 80:
                    LNM.turn_left(angle=steering_angle, speed=VELOCIDAD_BASE)

        # --- ESTADO 2: ESQUIVANDO (El PID se enfoca en el pilar detectado) ---
        elif estado_carrera == "ESQUIVANDO":
            print(f"🔄 [MODO ESQUIVA]: Evadiendo pilar por la {memoria_lado}")
            
            # Centro real de tu nueva ROI ampliada en el eje X: (30 + 610) / 2 = 320
            CENTRO_ROI_X = 320 
            
            if memoria_lado == "IZQUIERDA":
                if datos_verde[0] == 0:
                    estado_carrera = "REBASANDO"
                    continue
                
                # Para esquivar el VERDE, queremos que el coche pase por la IZQUIERDA del pilar.
                # Definimos un Target dinámico: la posición del pilar desplazada a la derecha de nuestro centro.
                # Al restarle la posición del pilar, si el pilar se acerca al centro, el error se vuelve negativo,
                # obligando al coche a girar a la izquierda.
                target_x = datos_verde[1] - 140  
                error_obs = target_x - CENTRO_ROI_X
                
            else: # DERECHA (Pilar Rojo)
                if datos_rojo[0] == 0:
                    estado_carrera = "REBASANDO"
                    continue
                
                # Para esquivar el ROJO, queremos pasar por la DERECHA del pilar.
                # Si el pilar aparece en nuestro camino, calculamos la desviación hacia la derecha
                # generando un error positivo para que el chasis rompa la dirección en sentido horario.
                target_x = datos_rojo[1] + 140  
                error_obs = target_x - CENTRO_ROI_X
            
            # --- CÁLCULO DE CONTROL PID AMORTIGUADO ---
            derivative_obs = error_obs - prev_error
            correction_obs = (Kp_obstaculo * error_obs) + (Kd_obstaculo * derivative_obs)
            prev_error = error_obs
            
            # El signo de la corrección ahora se aplica de manera uniforme
            steering_angle = int(80 + correction_obs)
            steering_angle = max(40, min(120, steering_angle))
            
            print(f"📊 Obs Error: {error_obs} | Correction: {correction_obs:.2f} | Steering: {steering_angle}")
            
            if steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=VELOCIDAD_BASE)
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=VELOCIDAD_BASE)
        # --- ESTADO 3: REBASANDO (Memoria ultrasónica lateral para no cerrar el giro antes de tiempo) ---
        elif estado_carrera == "REBASANDO":
            print(f"⏱️ [MODO REBASE]: Esperando liberación lateral. L:{left_dist}cm | R:{right_dist}cm")
            
            if memoria_lado == "IZQUIERDA":
                # El pilar está pasando por nuestro costado derecho. Mantener ruedas ligeramente a la izquierda (72°)
                LNM.turn_left(angle=72, speed=VELOCIDAD_BASE)
                
                # Si el ultrasonido derecho lee libre (> 40cm), el chasis superó físicamente la masa del pilar
                if right_dist > 40:
                    print("✅ Pilar rebasado con éxito por la derecha.")
                    estado_carrera = "LINEAL"
                    prev_error = 0.0
            
            elif memoria_lado == "DERECHA":
                # El pilar está pasando por nuestro costado izquierdo. Mantener ruedas ligeramente a la derecha (88°)
                LNM.turn_right(angle=88, speed=VELOCIDAD_BASE)
                
                # Si el ultrasonido izquierdo lee libre (> 40cm), el chasis superó físicamente la masa del pilar
                if left_dist > 40:
                    print("✅ Pilar rebasado con éxito por la izquierda.")
                    estado_carrera = "LINEAL"
                    prev_error = 0.0

        # =========================================================================
        # CONTEO DE VUELTAS Y CRONÓMETRO DE CIERRE
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

        if current_time - orange_timer > 1.1 and LNM.turning_direction == 2: 
            n = 0

        if current_time - blue_timer > 1.1 and LNM.turning_direction == 1:
            n = 0

        if loops >= 12 and not end_game_triggered:
            print("🏁 ¡Vuelta 12 alcanzada! Iniciando cronómetro de gracia...")
            end_game_timer = current_time
            end_game_triggered = True

        if end_game_triggered:
            if current_time - end_game_timer >= 1.0:
                print("⏱️ Tiempo completado. Deteniendo robot.")
                break
        
    except Exception as e:
        print("Exception en el bucle principal:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
