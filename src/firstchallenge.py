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
        LNM.move_forward(speed=100)
        # get areas and contours-----------------
        LNM.vision.receive_image()
        
        cnt_lines_blue = LNM.vision.find_contours(mask_blue_test, ROI_LINES)
        cnt_lines_orange = LNM.vision.find_contours(mask_orange_test, ROI_LINES)
        cnt_front_wall = LNM.vision.find_contours(mask_black_test, OPEN_ROI_CENTER)
        
        black_area = LNM.vision.max_contour(cnt_front_wall, OPEN_ROI_CENTER)[0]
        blue_area = LNM.vision.max_contour(cnt_lines_blue, ROI_LINES)[0]
        orange_area = LNM.vision.max_contour(cnt_lines_orange, ROI_LINES)[0]
        # get areas and contours-----------------
        
        # get turn direction based on line color----------
        
        if (LNM.turning_direction == 0): #only look for line colors if no colors have been detected yet.
            if (blue_area >= 10):
                LNM.turning_direction = 1 #left
            elif (orange_area >= 10):
                LNM.turning_direction = 2 #right
        # get turn direction based on line color----------
        
        # Determines if the car have to turn
        if (black_area >= TURN_THRESH):
            LNM.turn_direction()
            if line_detected:
                line_detected = False

        # Center the car  
        if (LNM.turning_direction != 0):
            if (black_area <= TURN_EXIT_THRESH):
                LNM.turn_center()
                if not line_detected:
                    loops += 1
                    line_detected = True
                
        # Break the cycle if it has completed all the laps
        if (loops == 12):
            break

        print(loops)
        
        
        
        #DRAWING------------------------------------------------------
        #draw rois---------s
        for roi in ROIS:
            LNM.vision.draw_roi(roi)
        #draw rois---------
            
        #draw contours-----------
        LNM.vision.draw_contours(cnt_front_wall, OPEN_ROI_CENTER, (255,255,0))
        LNM.vision.draw_contours(cnt_lines_blue, ROI_LINES, (255,255,0))
        LNM.vision.draw_contours(cnt_lines_orange, ROI_LINES, (255,0,0))
        #draw contours-----------
        
        #draw final img
        cv.putText(LNM.vision.frame, "black area: " + str(black_area), (0,20), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv.putText(LNM.vision.frame, "blue area: " + str(blue_area), (0,40), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv.putText(LNM.vision.frame, "orange area: " + str(orange_area), (0,60), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv.imshow("frame", LNM.vision.frame)
        
        #------------
        if cv.waitKey(1) == ord('q') or not running:
            LNM.vision.camera_cap.release()
            cv.destroyAllWindows()
            
        
    except Exception as e:
        print("Exception:", e)
        #print(traceback.format_exc())
        LNM.stop()
        break
    
    

LNM.stop()

