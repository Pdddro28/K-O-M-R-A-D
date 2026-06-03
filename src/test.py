import cv2
from vision_controller import ROI, VisionController
from PID_class import PIDController
from mega_pi_controller import *
from constants import *
import cv2 

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)


# 1. Initialize Picamera2
picam2 = LNM.vision  # This will initialize the camera and set it up for OpenCV processing

roi = ROI(100, 100, picam2.image_width - 100, picam2.image_height - 100)
print("Camera started. Press 'q' to quit.")

set_point_red = (155, 120)
set_point_green = (516, 125)

# Asegúrate de que tu clase PID reciba los parámetros así, o adapta el constructor a como lo tengas escrito
pid_red = PIDController(kp=0.5, ki=0.00, kd=0.1)
pid_green = PIDController(kp=0.5, ki=0.00, kd=0.1)

SERVO_CENTER = 90

try:
    while True:
        # Capture the current frame as a NumPy array
        picam2.receive_image()
        if picam2.frame is None:
            continue
            
        # 1. Buscar contornos para ambos colores
        red_ctn = picam2.find_contours(LNM.mask_red, roi) 
        green_ctn = picam2.find_contours(LNM.mask_green, roi)
        
        max_red = picam2.max_contour(red_ctn, roi)
        max_green = picam2.max_contour(green_ctn, roi)
        
        servo_angle = SERVO_CENTER  # Por defecto va recto si no ve nada
        #print(f"Max Red Area: {max_red[0]} | Max Green Area: {max_green[0]}")  # Debug: Imprime áreas máximas para ambos colores
        
        # 2. Lógica de control por prioridades (Prioriza el bloque que tenga mayor área en pantalla)
        if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
            # --- CASO OBSTÁCULO ROJO ---
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))  
            centroid_coords = picam2.draw_centroid_line(max_red, roi)
            
            if centroid_coords:
                current_x = centroid_coords[0]
                # Calcular PID (Pasamos Setpoint X y el X actual)
                pid_output = pid_red.compute(set_point_red[0], current_x)
                print(f"[ROJO] Centroide X: {current_x} {centroid_coords[1]}")  # Debug: Imprime el output del PID para rojo
                
                # Para el rojo: si el objeto está muy a la derecha, la salida es negativa. 
                # Restar la salida hace que el ángulo disminuya (gira a la derecha -> hacia 0°)
                servo_angle = SERVO_CENTER - pid_output 
                
                picam2.draw_parallel_lane_line(centroid_coords, roi, offset=200, avoid_right=True)
                #print(f"[ROJO] Centroide X: {current_x} | Output PID: {pid_output:.2f}")

        elif max_green[3] is not None:
            # --- CASO OBSTÁCULO VERDE ---
            picam2.draw_contours(green_ctn, roi, (0, 255, 0))  
            centroid_coords = picam2.draw_centroid_line(max_green, roi)
            
            if centroid_coords:
                current_x = centroid_coords[0]
                pid_output = pid_green.compute(set_point_green[0], current_x)
                print(f"[VERDE] Centroide X: {current_x} {centroid_coords[1]}")  # Debug: Imprime el output del PID para verde

                
                # Para el verde: si el objeto está muy a la izquierda, la salida es positiva.
                # Sumar la salida hace que el ángulo aumente (gira a la izquierda -> hacia 180°)
                servo_angle = SERVO_CENTER - pid_output
                
                picam2.draw_parallel_lane_line(centroid_coords, roi, offset=200, avoid_right=False)
                #print(f"[VERDE] Centroide X: {current_x} | Output PID: {pid_output:.2f}")
        
        # 3. Limitar físicamente el rango del servo (Anti-rompimiento estructural)
        servo_angle = max(40, min(servo_angle, 120))
        LNM.turn_left(angle=int(servo_angle), speed=50)  # Aquí mandas el comando de giro a tu robot
        
        # Imprimir el ángulo final calculado para tu actuador
        #print(f"--> ÁNGULO DEL SERVO: {servo_angle:.2f}°")
        # robot.set_servo_angle(servo_angle) # <- Aquí mandas el ángulo a tu hardware

        # Renderizar interfaz e imágenes
        picam2.draw_roi(roi)  
        cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

        # Wait for 1ms and check if 'q' is pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 4. Clean up resources
    cv2.destroyAllWindows()