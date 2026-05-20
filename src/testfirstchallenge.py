from mega_pi_controller import *
from constants import *
import cv2 
# LNMbi setup
LNM = MegaPiController("/dev/ttyUSB0", 115200)

# Centering the directions
# LNM.turn_center()

# Saving the ROIs
ROIS = [OPEN_ROI_CENTER, ROI_LINES]

# Waiting to press the button
# while not LNM.start():
#     pass

running = True
loops = 0
line_detected = False

girando = False
#LNM.turning_direction = 2
#LNM.turn_direction()
#LNM.turn_center(log=False)

# Start moving

while running:
    try:
        LNM.move_forward(speed = 65)  #Avanza siempre
        LNM.vision.receive_image()
        LNM.obtener_linea_azul()
        LNM.obtener_linea_naranja()
        LNM.obtenerarea_frontal()

        front_dist, left_dist, right_dist = LNM.get_distances()

        # get areas and contours-----------------
        print(f"Distances - Front: {front_dist} | Left: {left_dist} | Right: {right_dist} | Blue Area: {LNM.blue_area} | Orange Area: {LNM.orange_area} | Front Area: {LNM.black_area}")
        
        if LNM.turning_direction == 0: #Obtener direccion de giro
            if LNM.orange_area > 1200:
                  LNM.turning_direction = 2
            elif LNM.blue_area > 1200:
                  LNM.turning_direction = 1
        #Determinar giro
        if front_dist < 100 and girando == False and LNM.black_area > 8000 and LNM.turning_direction != 0:
           LNM.turn_direction()
           loops += 1
           girando = True
              
        if LNM.black_area < 8000 and girando == True and front_dist > 100:
           LNM.turn_center()
           girando = False
           #time.sleep(2)
           #LNM.stop()
           #break
           
        if not girando:
            if left_dist < 25:
                # Demasiado cerca de la izquierda -> Microajuste a la derecha
                # Nota: Asegúrate de si en tu librería 1 o 2 es derecha/izquierda. 
                # Si 'LNM.turning_direction' usa 2 para un lado, aquí usamos un método manual o el inverso.
                LNM.turn_right(angle=40, speed=80) 
                print("-> Microajuste: Alejándose de la izquierda")
                
            elif right_dist < 60:
                # Demasiado cerca de la derecha -> Microajuste a la izquierda
                LNM.turn_left(angle=120, speed=80)
                print("<- Microajuste: Alejándose de la derecha")
                
            elif left_dist > 25 and right_dist > 60:
                # Si ya se alejó lo suficiente de ambas paredes, vuelve a centrar
                LNM.turn_center(angle=90, speed=80)

        #UI debug
        #LNM.debug_UI()
        #if cv2.waitKey(1) & 0xFF == ord('q'): break
        # Break the cycle if it has completed all the laps
        

        if (loops == 12):
            break
        
    except Exception as e:
        print("Exception:", e)
        #print(traceback.format_exc())
        LNM.stop()
        break
    
    

LNM.stop()
