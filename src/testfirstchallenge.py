from mega_pi_controller import *
from constants import *
import cv2 as cv
# LNMbi setup
LNM = MegaPiController("COM9", 115200, cam_port=0)

# Centering the directions
LNM.turn_center()

# Saving the ROIs
ROIS = [OPEN_ROI_CENTER, ROI_LINES]

# Waiting to press the button
while LNM.start():
    pass

running = True
loops = 0
line_detected = False

# Start moving
while running:
    try:
        LNM.move_forward(speed=100)  # Works
        # get areas and contours-----------------
        #LNM.vision.receive_image()
        front_dist, left_dist, right_dist = LNM.get_distances()
        print(f"Distances - Front: {front_dist} | Left: {left_dist} | Right: {right_dist}")

        if front_dist < 20:
            print("Obstacle detected! Stopping.")
            LNM.stop()
            break
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

