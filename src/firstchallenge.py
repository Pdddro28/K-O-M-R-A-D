from mega_pi_controller import *
from constants import *
import cv2 as cv
import time

# --- INITIALIZATION AND CONFIGURATION ---
LNM = MegaPiController("/dev/ttyUSB1", 115200)

DIST_TURN_THRESH = 30   
DIST_EXIT_THRESH = 50   

print("Esperando botón para iniciar...")
while not LNM.start():
    time.sleep(0.1)

running = True
loops = 0
line_detected = False
giro_en_progreso = False

# --- MAIN CONTROL LOOP ---
while running:
    try:
        LNM.move_forward(speed=100)  
        
        # Computer Vision Data Acquisition
        LNM.vision.receive_image()
        
        cnt_lines_blue = LNM.vision.find_contours(mask_blue_test, ROI_LINES)
        cnt_lines_orange = LNM.vision.find_contours(mask_orange_test, ROI_LINES)
        cnt_front_wall = LNM.vision.find_contours(mask_black_test, OPEN_ROI_CENTER)
        
        black_area = LNM.vision.max_contour(cnt_front_wall, OPEN_ROI_CENTER)[0]
        blue_area = LNM.vision.max_contour(cnt_lines_blue, ROI_LINES)[0]
        orange_area = LNM.vision.max_contour(cnt_lines_orange, ROI_LINES)[0]
        
        # Race Execution Management
        if loops == 12:
            print("\n🏁 ¡12 vueltas completadas!")
            break

        print(f"Vueltas: {loops} | Distancia Frontal: {f}cm  ", end='\r')
        
        time.sleep(0.05)
        
    except Exception as e:
        print("\nException:", e)
        LNM.stop()
        break

# --- RESOURCE CLEANUP ---
LNM.stop()
LNM.close()
