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

roi = ROI(0, 50, picam2.image_width , picam2.image_height - 100)
print("Camera started. Press 'q' to quit.")

set_point_red = (155, 120)
set_point_green = (490, 125)

# Asegúrate de que tu clase PID reciba los parámetros así, o adapta el constructor a como lo tengas escrito
pid_red = PIDController(kp=0.5, ki=0.0, kd=0.1)
pid_green = PIDController(kp=10, ki=0.0, kd=0.1)
pid_dist = PIDController(kp=2.9, ki=0.0, kd=1)

obstacle_detected = False
obstacle_detected_red = False
obstacle_detected_green = False
#LNM.vision.image_width = 1080
girando = False
TARGET_DIST = 20.0

SERVO_CENTER = 90
def obstacle_detection():
        global obstacle_detected, girando, running, obstacle_detected_red, obstacle_detected_green
                # 1. Buscar contornos para ambos colores
        red_ctn = picam2.find_contours(LNM.mask_red, roi) 
        green_ctn = picam2.find_contours(LNM.mask_green, roi)
        
        max_red = picam2.max_contour(red_ctn, roi)
        max_green = picam2.max_contour(green_ctn, roi)
        
        servo_angle = SERVO_CENTER  # Por defecto va recto si no ve nada
            # 2. Lógica de control por prioridades (Prioriza el bloque que tenga mayor área en pantalla)
        if max_red[3] is not None and (max_green[3] is None or max_red[0] > max_green[0]):
            # --- CASO OBSTÁCULO ROJO ---
            picam2.draw_contours(red_ctn, roi, (0, 0, 255))  
            centroid_coords = picam2.draw_centroid_line(max_red, roi)
            #print(max_red[0])
            
            if centroid_coords and max_red[0] > 1700:
                obstacle_detected = True
                obstacle_detected_red = True
                obstacle_detected_green = False
                girando = False
                current_x = centroid_coords[0]
                # Calcular PID (Pasamos Setpoint X y el X actual)
                pid_output = pid_red.compute(set_point_red[0], current_x)
                
                # Para el rojo: si el objeto está muy a la derecha, la salida es negativa. 
                # Restar la salida hace que el ángulo disminuya (gira a la derecha -> hacia 0°)
                # print(pid_red.error)

                if abs(pid_red.error) > 150:
                    servo_angle = SERVO_CENTER - pid_output
                
                picam2.draw_parallel_lane_line(centroid_coords, roi, offset=200, avoid_right=True)
                #print(f"[ROJO] Centroide X: {current_x} | Output PID: {pid_output:.2f}")
            else: 
                obstacle_detected = False

        elif max_green[3] is not None:
            # --- CASO OBSTÁCULO VERDE ---
            picam2.draw_contours(green_ctn, roi, (0, 255, 0))  
            centroid_coords = picam2.draw_centroid_line(max_green, roi)
            if centroid_coords and max_green[0] > 100:
                running = False
                current_x = picam2.image_width - centroid_coords[0]
                obstacle_detected = True
                obstacle_detected_green = True
                obstacle_detected_red = False
                girando = False

                

                pid_output = pid_green.compute(picam2.image_width - set_point_green[0], current_x)
                #print(f"[VERDE] Centroide X: {current_x} {centroid_coords[1]}")  # Debug: Imprime el output del PID para verde

                
                # Para el verde: si el objeto está muy a la izquierda, la salida es positiva.
                # Sumar la salida hace que el ángulo aumente (gira a la izquierda -> hacia 180°)
                print(pid_green.error)

                if abs(pid_green.error) > 110:
                    servo_angle = SERVO_CENTER + pid_output
                
                picam2.draw_parallel_lane_line(centroid_coords, roi, offset=200, avoid_right=False)
                #print(f"[VERDE] Centroide X: {current_x} | Output PID: {pid_output:.2f}")
            else:
                obstacle_detected = False
        
        # 3. Limitar físicamente el rango del servo (Anti-rompimiento estructural)
        if obstacle_detected:
            servo_angle = max(40, min(servo_angle, 120))
            LNM.turn_left(angle=int(servo_angle), speed=70)
        
try:
    while True:
        # Capture the current frame as a NumPy array
        picam2.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
            
        # Renderizar interfaz e imágenes
        picam2.draw_roi(roi) 
        LNM.vision.draw_roi(LNM.rois[0]) 
        LNM.vision.draw_roi(LNM.rois[1]) 
        cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

         # Wait for 1ms and check if 'q' is pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

        #print(f"Max Red Area: {max_red[0]} | Max Green Area: {max_green[0]}")  # Debug: Imprime áreas máximas para ambos colores
        LNM.move_forward(60)
        front_dist, left_dist, right_dist = LNM.get_distances()
        #print(f"Distances - Front: {front_dist:.2f} cm, Left: {left_dist:.2f} cm, Right: {right_dist:.2f} cm")

        if LNM.turning_direction == 0 and obstacle_detected == False: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)

            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)

        

        obstacle_detection()

        
        # Realizar vuelta

        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0 and obstacle_detected == False:
            LNM.turn_direction()
            girando = True
            print(girando)
              
        if LNM.black_area < 8000 and girando and front_dist > 80 and obstacle_detected == False:
           LNM.turn_center()
           girando = False
           conteo = False

        if not girando and LNM.turning_direction != 0:
            print("ERROR PID RECALCULANDO")
            # Pista Naranja: Sigue pared IZQUIERDA. 
            # Si se acerca a la pared (dist < 30), debe ir a la Derecha.
            current_dist = TARGET_DIST
            lado_correccion = 0
            if LNM.turning_direction == 2 or obstacle_detected_red:    
                current_dist = min(left_dist, 60.0)   
                lado_correccion = 1                 # (+) -> Derecha, (-) -> Izquierda
            
            # Pista Azul: Sigue pared DERECHA.
            # Si se acerca a la pared (dist < 30), debe ir a la Izquierda.
            elif LNM.turning_direction == 1 or obstacle_detected_green:  
                current_dist = min(right_dist, 60.0)  
                lado_correccion = -1                # (+) -> Izquierda, (-) -> Derecha
            
            correction = pid_dist.compute(TARGET_DIST, current_dist)
            
            # El centro físico o neutral del servo es 80
            # Aplicamos la corrección con la dirección correspondiente
            steering_angle = int(80 + (correction * lado_correccion))
            
            # Restringimos el ángulo entre los límites seguros de tu robot (40 y 120)
            steering_angle = max(40, min(120, steering_angle))
            
            # --- CORRECCIÓN MEJORADA EN AMBOS SENTIDOS ---
            # Si el error es mínimo, va recto.
            if abs(pid_dist.error) < 1.5: 
                LNM.turn_center()
            # Si el ángulo es mayor que el centro, físicamente cruza a la derecha
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            # Si el ángulo es menor que el centro, físicamente cruza a la izquierda
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)

finally:
    # 4. Clean up resources
    cv2.destroyAllWindows()