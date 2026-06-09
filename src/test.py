from mega_pi_controller import *
from constants import *
import cv2
import numpy as np
import time

# --- INITIALIZATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

# --- PARÁMETROS AJUSTABLES DE LA SCANLINE ---
SCAN_Y = 280         # Fila horizontal para el radar (más abajo = reacciona más cerca del parachoques)
WIDTH = 640          # Ancho estándar de la cámara
CENTER_X = 320       # Centro ideal de la cámara

# --- SINTONIZACIÓN PD (Píxeles a Ángulo) ---
# Como el error máximo en píxeles puede ser ~320, un Kp de 0.12 da una corrección máxima de ~38 grados
Kp_scan = 0.12       
Kd_scan = 0.04       
prev_error_scan = 0.0

# --- RANGO HSV PARA FILTRAR EL SUELO BLANCO ---
# Ajusta el último valor (180) si tu pista tiene sombras o mucha luz
LOWER_WHITE = np.array([0, 0, 180])
UPPER_WHITE = np.array([180, 40, 255])

running = True

print("🚀 Script de prueba Scanline iniciado. Presiona 'q' en la ventana de video para salir.")

while running:
    try:
        # 1. Captura de imagen
        LNM.vision.receive_image()
        frame = LNM.vision.frame
        
        if frame is None:
            continue

        # 2. Procesamiento de color (Máscara Blanca)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_white = cv2.inRange(hsv, LOWER_WHITE, UPPER_WHITE)
        
        # 3. FILTRO DE SEGURIDAD (¿El centro está en zona blanca?)
        # Si el coche ya está muy cruzado y ve negro en el centro, busca el píxel blanco más cercano
        if mask_white[SCAN_Y, CENTER_X] == 0:
            # Buscar hacia los lados un punto blanco de rescate
            rescate_encontrado = False
            for offset in range(1, 150):
                if CENTER_X - offset > 0 and mask_white[SCAN_Y, CENTER_X - offset] == 255:
                    ponto_inicio_x = CENTER_X - offset
                    rescate_encontrado = True
                    break
                if CENTER_X + offset < WIDTH and mask_white[SCAN_Y, CENTER_X + offset] == 255:
                    ponto_inicio_x = CENTER_X + offset
                    rescate_encontrado = True
                    break
            if not rescate_encontrado:
                ponto_inicio_x = CENTER_X # Failsafe
        else:
            ponto_inicio_x = CENTER_X

        # 4. LANZAR RADAR HACIA LA IZQUIERDA
        left_x = ponto_inicio_x
        while left_x > 0 and mask_white[SCAN_Y, left_x] == 255:
            left_x -= 1
        dist_izquierda = ponto_inicio_x - left_x

        # 5. LANZAR RADAR HACIA LA DERECHA
        right_x = ponto_inicio_x
        while right_x < WIDTH - 1 and mask_white[SCAN_Y, right_x] == 255:
            right_x += 1
        dist_derecha = right_x - ponto_inicio_x

        # 6. CÁLCULO PROPORCIONAL DEL ERROR
        # Si dist_izquierda > dist_derecha -> Estamos muy a la derecha -> Error positivo
        error = dist_izquierda - dist_derecha
        
        # Control PD
        derivative = error - prev_error_scan
        correction = (Kp_scan * error) + (Kd_scan * derivative)
        prev_error_scan = error
        
        # El centro del servo es 80. Si el error es positivo (ir a la izquierda), restamos corrección.
        steering_angle = int(80 - correction)
        steering_angle = max(40, min(120, steering_angle))

        # 7. TELEMETRÍA GRÁFICA (Pintar el radar en el feed en vivo)
        # Línea del radar (Verde)
        cv2.line(frame, (left_x, SCAN_Y), (right_x, SCAN_Y), (0, 255, 0), 2)
        # Centro del radar (Azul)
        cv2.circle(frame, (ponto_inicio_x, SCAN_Y), 5, (255, 0, 0), -1)
        # Límites encontrados (Rojo)
        cv2.circle(frame, (left_x, SCAN_Y), 5, (0, 0, 255), -1)
        cv2.circle(frame, (right_x, SCAN_Y), 5, (0, 0, 255), -1)
        
        # Desplegar datos clave en la terminal
        print(f"Dist L: {dist_izquierda}px | Dist R: {dist_derecha}px | Error: {error} | Servo Target: {steering_angle}")

        # 8. ACCIÓN FÍSICA EN MOTORES
        LNM.move_forward(speed=75) # Tu velocidad dulce y estable
        
        if steering_angle > 83:
            LNM.turn_right(angle=steering_angle, speed=50)
        elif steering_angle < 77:
            LNM.turn_left(angle=steering_angle, speed=50)
        else:
            LNM.turn_center()

        # Mostrar las ventanas de calibración
        cv2.imshow('Radar Scanline en Vivo', frame)
        cv2.imshow('Mascara Blanca Filtrada', mask_white)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print("🚨 Error en el bucle de prueba:", e)
        break

# --- SHUTDOWN ---
LNM.stop()
cv2.destroyAllWindows()
