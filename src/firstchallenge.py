from mega_pi_controller import *
from constants import *
import cv2 as cv
import time

# LNMbi setup
LNM = MegaPiController("COM9", 115200, cam_port=0)

# Centering the directions
LNM.turn_center()

# Saving the ROIs (Comentado por ahora ya que Vision no procesa)
# ROIS = [OPEN_ROI_CENTER, ROI_LINES]

# --- NUEVOS UMBRALES DE DISTANCIA ---
DIST_TURN_THRESH = 30   # Equivale a TURN_THRESH (cuándo empezar a girar)
DIST_EXIT_THRESH = 50   # Equivale a TURN_EXIT_THRESH (cuándo centrar)

# Waiting to press the button
print("Esperando botón para iniciar...")
while not LNM.start():
    time.sleep(0.1)

running = True
loops = 0
line_detected = False
giro_en_progreso = False

# Start moving
while running:
    try:
        # El carro avanza
        LNM.move_forward(speed=100)

        # 1. OBTENER DISTANCIAS (Sustituye a la visión)
        f, l, r = LNM.get_distances()

        # --- SECCIÓN OPENCV COMENTADA ---
        """
        LNM.vision.receive_image()
        
        cnt_lines_blue = LNM.vision.find_contours(mask_blue_test, ROI_LINES)
        cnt_lines_orange = LNM.vision.find_contours(mask_orange_test, ROI_LINES)
        cnt_front_wall = LNM.vision.find_contours(mask_black_test, OPEN_ROI_CENTER)
        
        black_area = LNM.vision.max_contour(cnt_front_wall, OPEN_ROI_CENTER)[0]
        blue_area = LNM.vision.max_contour(cnt_lines_blue, ROI_LINES)[0]
        orange_area = LNM.vision.max_contour(cnt_lines_orange, ROI_LINES)[0]
        """
        # Variables de área en 0 para evitar errores si algo quedó sin comentar
        black_area = 0
        blue_area = 0
        orange_area = 0
        # ---------------------------------
        
        # Lógica de dirección (si no hay visión, decide por el lado más despejado)
        if (LNM.turning_direction == 0):
            if l > r:
                LNM.turning_direction = 1 # izquierda
            else:
                LNM.turning_direction = 2 # derecha
        
        # Determina si el carro tiene que girar (USANDO DISTANCIA FRONTAL)
        if (f <= DIST_TURN_THRESH):
            if not giro_en_progreso:
                LNM.turn_direction()
                giro_en_progreso = True
                if line_detected:
                    line_detected = False

        # Centrar el carro (USANDO DISTANCIA FRONTAL)
        if (giro_en_progreso):
            if (f >= DIST_EXIT_THRESH):
                LNM.turn_center()
                giro_en_progreso = False
                if not line_detected:
                    loops += 1
                    line_detected = True
                
        # Break the cycle if it has completed all the laps
        if (loops == 12):
            print("\n🏁 ¡12 vueltas completadas!")
            break

        print(f"Vueltas: {loops} | Distancia Frontal: {f}cm  ", end='\r')
        
        # --- SECCIÓN DE DIBUJO Y GUI COMENTADA ---
        """
        for roi in ROIS:
            LNM.vision.draw_roi(roi)
            
        LNM.vision.draw_contours(cnt_front_wall, OPEN_ROI_CENTER, (255,255,0))
        LNM.vision.draw_contours(cnt_lines_blue, ROI_LINES, (255,255,0))
        LNM.vision.draw_contours(cnt_lines_orange, ROI_LINES, (255,0,0))
        
        cv.putText(LNM.vision.frame, "F Dist: " + str(f), (0,20), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv.imshow("frame", LNM.vision.frame)
        
        if cv.waitKey(1) == ord('q'):
            break
        """
        # -----------------------------------------
        
        time.sleep(0.05)
        
    except Exception as e:
        print("\nException:", e)
        LNM.stop()
        break

LNM.stop()
LNM.close()
