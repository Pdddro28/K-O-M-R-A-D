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
while not LNM.start():
    pass

running = True
loops = 0
line_detected = False

girando = False

LNM.turning_direction = 2

# Start moving
while running:
    try:
        LNM.move_forward(speed = 65)  #Avanza siempre
        front_dist, left_dist, right_dist = LNM.get_distances()

        # get areas and contours-----------------
        #LNM.vision.receive_image()
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


        # get areas and contours-----------------
        
        # get turn direction based on line color----------
        
        # if (LNM.turning_direction == 0): #only look for line colors if no colors have been detected yet.
        #     if (blue_area >= 10):
        #         LNM.turning_direction = 1 #left
        #     elif (orange_area >= 10):
        #         LNM.turning_direction = 2 #right
        # get turn direction based on line color----------
        
        # Determines if the car have to turn
        # if (black_area >= TURN_THRESH):
        #     LNM.turn_direction()
        #     if line_detected:
        #         line_detected = False

        # # Center the car  
        # if (LNM.turning_direction != 0):
        #     if (black_area <= TURN_EXIT_THRESH):
        #         LNM.turn_center()
        #         if not line_detected:
        #             loops += 1
        #             line_detected = True
                
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

