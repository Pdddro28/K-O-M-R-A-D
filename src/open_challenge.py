from mega_pi_controller import *
from constants import *
import cv2 

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB0", 115200)

ROIS = [OPEN_ROI_CENTER, ROI_LINES]

states = {"straight": False, "girando": False}

running = True
loops = 0

orange_timer = time.time()
time_lap = time.time()
n = 0

# --- PID CONTROLLER VARIABLES (Ajustados para mayor suavidad) ---
TARGET_DIST = 30.0  
Kp = 2.9    # Incrementado ligeramente para reaccionar más rápido
Ki = 0.0   # Se añade una pizca de integral para eliminar el error estático
Kd = 1    # Incrementado para amortiguar oscilaciones bruscas

prev_error = 0.0
integral = 0.0
MAX_INTEGRAL = 15.0 # Anti-windup para evitar que el robot se vuelva loco
girando = False
conteo = False

# --- TIMERS AND FLAGS ---
color_timer = time.time()
time_lap = time.time()
n = 0

# --- MAIN CONTROL LOOP ---
while running:
    try:
        # Sensors and data acquisition
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()
        LNM.debug_UI()
        LNM.move_forward(speed = 85) 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        front_dist, left_dist, right_dist = LNM.get_distances()
        print(f"Turning: {LNM.turning_direction}, black_area: {LNM.black_area}, blue_area: {LNM.blue_area}, orange_area: {LNM.orange_area}")
        #print(f"Distances - Front: {front_dist:.2f} cm, Left: {left_dist:.2f} cm, Right: {right_dist:.2f} cm")
        # 1. TRACK TYPE DETECTION
        if LNM.turning_direction == 0: 
            if LNM.orange_area > 1200:
                 LNM.turning_direction = 2
                
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)
            elif LNM.blue_area > 1200:
                 LNM.turning_direction = 1
                 #LNM.configurar_PID_dis(Target_dist=30.0, Kp=1.5, Ki=0.0, Kd=0.8)


        if front_dist < 90 and not girando and LNM.black_area > 8000 and LNM.turning_direction != 0:
            LNM.turn_direction()
            girando = True
            prev_error = 0.0
            integral = 0.0
              
        if LNM.black_area < 8000 and girando and front_dist > 100:
           LNM.turn_center()
           girando = False
           conteo = False

        if not girando and LNM.turning_direction != 0:
            
            # Pista Naranja: Sigue pared IZQUIERDA. 
            # Si se acerca a la pared (dist < 30), debe ir a la Derecha.
            if LNM.turning_direction == 2:    
                current_dist = min(left_dist, 60.0)   
                error = TARGET_DIST - current_dist  # Error (+) si está muy cerca
                lado_correccion = 1                 # (+) -> Derecha, (-) -> Izquierda
            
            # Pista Azul: Sigue pared DERECHA.
            # Si se acerca a la pared (dist < 30), debe ir a la Izquierda.
            elif LNM.turning_direction == 1:  
                current_dist = min(right_dist, 60.0)  
                error = TARGET_DIST - current_dist  # Error (+) si está muy cerca
                lado_correccion = -1                # (+) -> Izquierda, (-) -> Derecha
            
            derivative = error - prev_error
            correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
            prev_error = error
            
            # El centro físico o neutral del servo es 80
            # Aplicamos la corrección con la dirección correspondiente
            steering_angle = int(80 + (correction * lado_correccion))
            
            # Restringimos el ángulo entre los límites seguros de tu robot (40 y 120)
            steering_angle = max(40, min(120, steering_angle))
            
            # --- CORRECCIÓN MEJORADA EN AMBOS SENTIDOS ---
            # Si el error es mínimo, va recto.
            if abs(error) < 1.5: 
                LNM.turn_center()
            # Si el ángulo es mayor que el centro, físicamente cruza a la derecha
            elif steering_angle > 80:
                LNM.turn_right(angle=steering_angle, speed=50)
            # Si el ángulo es menor que el centro, físicamente cruza a la izquierda
            elif steering_angle < 80:
                LNM.turn_left(angle=steering_angle, speed=50)


        # 3. CORNER LOGIC AND LAP COUNTER
        current_time = time.time()

        if LNM.orange_area > 500 and n == 0 and LNM.turning_direction == 2: 
            orange_timer = current_time
            n = 1
            loops += 1

        if current_time - orange_timer > 3: 
            n = 0
            print("Timer reset, ready for next orange line detection.")

        print("Loop count:", loops)

        if loops == 12:
            LNM.turn_direction()
            time.sleep(3)
            break
        
    except Exception as e:
        print("Exception:", e)
        LNM.stop()
        break

# --- SAFETY SHUTDOWN ---
LNM.stop()
