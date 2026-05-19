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
        print(f"Distances - Front: {front_dist} | Left: {left_dist} | Right: {right_dist} | Blue Area: {LNM.blue_area} | Orange Area: {LNM.orange_area} | Front Area: {LNM.black_area}")
        
        if LNM.turning_direction == 0: #Obtener direccion de giro
            if LNM.orange_area > 2000:
                  LNM.turning_direction = 1
            elif LNM.blue_area > 2000:
                  LNM.turning_direction = 2
        #Determinar giro
        if front_dist < 100 and LNM.black_area > 12000 and LNM.turning_direction != 0:
           LNM.turn_direction()
           loops += 1
        elif LNM.black_area < 9000:
           LNM.turn_center()

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

