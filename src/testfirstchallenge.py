from mega_pi_controller import *
from constants import *
import cv2 as cv
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

LNM.turning_direction = 2

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
        LNM.vision.receive_image()
        print(f"Distances - Front: {front_dist} | Left: {left_dist} | Right: {right_dist}")

        if front_dist < 100 and LNM.turning_direction == 2: #Gira derecha
           print("Obstacle detected! Stopping.")
           LNM.turn_left(angle=40, speed=130)
           girando = True
        elif front_dist < 100 and left_dist > 41: #Gira izquierda
           print("Obstacle detected! Stopping.")
           #LNM.turn_right(angle=40, speed=120)
           girando = True
        elif right_dist < 70 and left_dist < 70 and girando == True: #Sigue avanzando
           print("Obstacle detected! Stopping.")
           LNM.turn_left(angle=90, speed=80)
           girando = False
           #time.sleep(2)
           #LNM.stop()
           #break
        
        LNM.debug_UI()
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        # Break the cycle if it has completed all the laps
        if (loops == 12):
            break

        print(loops)
        
        
            
        
    except Exception as e:
        print("Exception:", e)
        #print(traceback.format_exc())
        LNM.stop()
        break
    
    

LNM.stop()

