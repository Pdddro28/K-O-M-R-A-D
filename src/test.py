import cv2
import numpy as np
import time
from mega_pi_controller import *
from constants import *

LNM = MegaPiController("/dev/ttyUSB0", 115200)

# --- CONFIGURACIÓN DE ROIS PARA EL SUELO ---
# Colocamos los ROIs más abajo en la pantalla para ver el suelo inmediatamente frente al coche
roi_suelo_izq = ROI(0, 200, 320, 320)   # Mitad izquierda inferior
roi_suelo_der = ROI(320, 200, 640, 320) # Mitad derecha inferior

# --- PARÁMETROS PID PARA DENSIDAD BLANCA ---
# Como los números de píxeles son grandes, el Kp suele ser más pequeño
Kp_suelo = 0.0002  
Kd_suelo = 0.00005
prev_error_suelo = 0.0

# Rango HSV típico para la lona blanca de la WRO (Ajusta según tu iluminación)
LOWER_WHITE = np.array([0, 0, 180])
UPPER_WHITE = np.array([180, 40, 255])

def obtener_densidad_blanco(frame):
    """ Filtra el color blanco y cuenta cuántos píxeles hay en cada lado """
    # 1. Pasar a HSV y crear la máscara blanca
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_white = cv2.inRange(hsv, LOWER_WHITE, UPPER_WHITE)
    
    # 2. Recortar la máscara en los dos lados del suelo
    crop_izq = mask_white[roi_suelo_izq.y_min:roi_suelo_izq.y_max, roi_suelo_izq.x_min:roi_suelo_izq.x_max]
    crop_der = mask_white[roi_suelo_der.y_min:roi_suelo_der.y_max, roi_suelo_der.x_min:roi_suelo_der.x_max]
    
    # 3. Contar píxeles blancos (¡Ultra rápido!)
    pixels_izq = cv2.countNonZero(crop_izq)
    pixels_der = cv2.countNonZero(crop_der)
    
    # Dibujar los recuadros en pantalla para telemetría
    LNM.vision.draw_roi(roi_suelo_izq)
    LNM.vision.draw_roi(roi_suelo_der)
    
    return pixels_izq, pixels_der, mask_white

# --- MAIN LOOP DE PRUEBA ---
while True:
    LNM.vision.receive_image()
    frame = LNM.vision.frame
    
    # Obtener el conteo de píxeles
    pixels_izq, pixels_der, mask_white = obtener_densidad_blanco(frame)
    
    # =========================================================================
    # CÁLCULO DEL ERROR POR DENSIDAD
    # =========================================================================
    # Si pixels_izq > pixels_der -> Error es positivo -> El coche debe ir a la izquierda
    error = pixels_izq - pixels_der
    
    # PD Control
    derivative = error - prev_error_suelo
    correction = (Kp_suelo * error) + (Kd_suelo * derivative)
    prev_error_suelo = error
    
    # Aplicar corrección al servo (80 es tu centro)
    # Si el error es positivo (mucho blanco a la izquierda), restamos la corrección para girar a la izquierda (ej. 65)
    steering_angle = int(80 - correction)
    steering_angle = max(40, min(120, steering_angle))
    
    print(f"Píxeles L: {pixels_izq} | R: {pixels_der} | Error: {error} -> Ángulo: {steering_angle}")
    
    # Acción de los motores a tu velocidad estable de 75
    LNM.move_forward(speed=75)
    
    if steering_angle > 83:
        LNM.turn_right(angle=steering_angle, speed=50)
    elif steering_angle < 77:
        LNM.turn_left(angle=steering_angle, speed=50)
    else:
        LNM.turn_center()

    # Mostrar máscaras para calibrar en tiempo real
    cv2.imshow('Mascara Blanca', mask_white)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

LNM.stop()
