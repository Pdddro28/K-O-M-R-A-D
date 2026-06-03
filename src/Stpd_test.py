from mega_pi_controller import *

from constants import *

import cv2 

import time



# --- INITIALIZATION AND CONFIGURATION ---

LNM = MegaPiController("/dev/ttyUSB0", 115200)



ROIS = [OPEN_ROI_CENTER, ROI_LINES]



states = {"straight": False, "girando": False}



running = True

loops = 0



# --- PID CONTROLLER VARIABLES (Ajustados para mayor suavidad) ---

TARGET_DIST = 30.0  

Kp = 1.8    # Incrementado ligeramente para reaccionar mÃ¡s rÃ¡pido

Ki = 0.01   # Se aÃ±ade una pizca de integral para eliminar el error estÃ¡tico

Kd = 1.2    # Incrementado para amortiguar oscilaciones bruscas



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

        # Sensors and data acquisition (Se mantienen activos pero no deciden la pista)

        LNM.vision.receive_image()

        LNM.obtener_linea_azul()

        LNM.obtener_linea_naranja()

        LNM.obtenerarea_frontal()

        LNM.debug_UI()

        LNM.move_forward(speed = 50)  

        

        # Emergency break condition

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break



        front_dist, left_dist, right_dist = LNM.get_distances()

        

        # 1. AUTOMATIC TRACK TYPE DETECTION (ANULADO: Se define dinÃ¡micamente en la primera curva)

        pass



        # 2. DYNAMIC PID WALL-CENTERING SYSTEM (Activo solo a partir del 2do Loop)

        if not girando and LNM.turning_direction != 0:

            

            if loops >= 2:

                # --- El PID se ejecuta normalmente a partir de la segunda vuelta ---

                # Pista Naranja / Modo 2: Sigue pared IZQUIERDA. 

                if LNM.turning_direction == 2:    

                    current_dist = min(left_dist, 60.0)   

                    error = TARGET_DIST - current_dist  

                    lado_correccion = 1                 

                

                # Pista Azul / Modo 1: Sigue pared DERECHA.

                elif LNM.turning_direction == 1:  

                    current_dist = min(right_dist, 60.0)  

                    error = TARGET_DIST - current_dist  

                    lado_correccion = -1                



                # PID Math calculations

                integral += error

                integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))

                

                derivative = error - prev_error

                correction = (Kp * error) + (Ki * integral) + (Kd * derivative)

                prev_error = error

                

                steering_angle = int(80 + (correction * lado_correccion))

                steering_angle = max(40, min(120, steering_angle))

                

                # Aplicar direcciÃ³n calculada por el PID

                if abs(error) < 1.5: 

                    LNM.turn_center()

                elif steering_angle > 80:

                    LNM.turn_right(angle=steering_angle, speed=50)

                elif steering_angle < 80:

                    LNM.turn_left(angle=steering_angle, speed=50)

            

            else:

                # --- Vuelta 0 y Vuelta 1: El robot va completamente recto sin corregir ---

                LNM.turn_center()



        # 3. CORNER LOGIC AND LAP COUNTER (Basado puramente en Distancia Frontal + Ãrea Negra + US Laterales)

        current_time = time.time()

        

        # CondiciÃ³n de curva: proximidad frontal y suficiente masa de obstÃ¡culo (Ã¡rea negra)

        if front_dist < 80 and not girando and LNM.black_area > 9000:

            

            # --- COMPENSACIÃ“N DE INVERSIÃ“N FÃSICA DE GIRO ---

            # Si el US Izquierdo ve mÃ¡s espacio libre -> Ejecutamos acciÃ³n contraria para corregir el hardware

            if left_dist > right_dist:

                LNM.turning_direction = 2  # Cambia la referencia de recta para adaptarse a la inversiÃ³n

                LNM.turn_right(angle=120, speed=50) # Forzamos giro fÃ­sico derecho

                print(f"Â¡Curva! Espacio en US Izq ({left_dist}) > US Der ({right_dist}). Corrigiendo inversiÃ³n fÃ­sica -> Girando a la DERECHA.")

                girando = True

            

            # Si el US Derecho ve mÃ¡s espacio libre -> Ejecutamos acciÃ³n contraria para corregir el hardware

            else:

                LNM.turning_direction = 1  # Cambia la referencia de recta para adaptarse a la inversiÃ³n

                LNM.turn_left(angle=40, speed=50) # Forzamos giro fÃ­sico izquierdo

                print(f"Â¡Curva! Espacio en US Der ({right_dist}) >= US Izq ({left_dist}). Corrigiendo inversiÃ³n fÃ­sica -> Girando a la IZQUIERDA.")

                girando = True

            

            # Reset de variables PID tras ejecutar el giro inmediato

            if girando:

                prev_error = 0.0

                integral = 0.0

                

                # Contador de vueltas preventivo basado en la ejecuciÃ³n del giro (Debounce de 3s)

                if n == 0:

                    color_timer = current_time

                    n = 1

                    loops += 1

                    print(f"Vuelta registrada por curva. Vueltas: {loops}")



        # Reset del debounce del contador

        if current_time - color_timer > 3: 

            n = 0



        # Salida de la curva (cuando el frente se libera)

        if LNM.black_area < 8000 and girando and front_dist > 100:

            LNM.turn_center()

            girando = False

            conteo = False



        # Race finish condition

        if loops == 13:

            print("Â¡Carrera terminada! 13 vueltas completadas.")

            break

        

    except Exception as e:

        print("Exception:", e)

        LNM.stop()

        break



# --- SAFETY SHUTDOWN ---

LNM.stop()

