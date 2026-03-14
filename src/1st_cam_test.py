# --------------------libraries------------------------
import cv2 as cv
import numpy as np
import json
import datetime
import tkinter as tk
from tkinter import filedialog
# --------------------libraries------------------------

# --------------------Classes--------------------------
class ROI:
    """
    Region of Interest: Defines the rectangular area 
    where the color search will be performed.
    """
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

class VisionController():
    """
    Handles camera stream, image preprocessing, 
    and color segmentation logic.
    """
    def __init__(self, usb_port=0):
        self.image_width  = 640
        self.image_height = 480
        self.image_lab = None
        self.frame = None
        
        self.camera_cap = cv.VideoCapture(usb_port)
        self.camera_cap.set(cv.CAP_PROP_FRAME_WIDTH, self.image_width)
        self.camera_cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.image_height)

    def receive_image(self):
        """
        Captures frame from hardware and converts it to 
        LAB color space for better light invariance.
        """
        ret, frame_read = self.camera_cap.read()
        if not ret:
            return False
            
        self.frame = frame_read
        self.image_lab = cv.cvtColor(self.frame, cv.COLOR_BGR2LAB)
        self.image_lab = cv.GaussianBlur(self.image_lab, (7,7), 0)
        return True

    def find_mask(self, color_range, roi):
        """
        Generates a binary mask based on a color range within a ROI.
        """
        img_segmented = self.image_lab[roi.y1:roi.y2, roi.x1:roi.x2]
        lower = np.array(color_range[0])
        upper = np.array(color_range[1])
        
        mask = cv.inRange(img_segmented, lower, upper)
        
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=1)
        mask = cv.dilate(mask, kernel, iterations=1)
        return mask
# --------------------Classes--------------------------

# --------------------Configuration & Presets----------
COLOR_PRESETS = {
    0: {"name": "ROJO",      "lower": [ 30, 170, 120], "upper": [255, 255, 170]},
    1: {"name": "VERDE",     "lower": [ 30,   0, 100], "upper": [255, 100, 160]},
    2: {"name": "AZUL",      "lower": [ 30, 110,   0], "upper": [255, 150, 110]},
    3: {"name": "MORADO",    "lower": [ 30, 160,   0], "upper": [255, 255, 110]},
    4: {"name": "NARANJA",   "lower": [ 50, 140, 150], "upper": [255, 255, 255]},
    5: {"name": "NEGRO",     "lower": [  0,   0,   0], "upper": [ 60, 255, 255]}
}

COLOR_NAMES_LIST = [COLOR_PRESETS[i]["name"] for i in range(len(COLOR_PRESETS))]
# --------------------Configuration & Presets----------

# --------------------Global Variables-----------------
WINDOW_NAME = "Sistema de Vision Integral"
save_triggered = False
save_status = "LISTO"
save_status_frames = 0
# --------------------Global Variables-----------------

# --------------------Helper Functions-----------------
def on_color_selector_change(val):
    """
    Callback: Update trackbars when color preset changes.
    """
    preset = COLOR_PRESETS[val]
    cv.setTrackbarPos("L-min", WINDOW_NAME, preset["lower"][0])
    cv.setTrackbarPos("L-max", WINDOW_NAME, preset["upper"][0])
    cv.setTrackbarPos("A-min", WINDOW_NAME, preset["lower"][1])
    cv.setTrackbarPos("A-max", WINDOW_NAME, preset["upper"][1])
    cv.setTrackbarPos("B-min", WINDOW_NAME, preset["lower"][2])
    cv.setTrackbarPos("B-max", WINDOW_NAME, preset["upper"][2])

def on_save_button_change(val):
    """
    Callback: Triggered when user clicks/moves the Save trackbar.
    We use this as a button by checking if value changed to 1.
    """
    global save_triggered
    if val == 1:
        save_triggered = True
        # Reset trackbar to 0 immediately so it can be clicked again
        cv.setTrackbarPos(">>> GUARDAR JSON <<<", WINDOW_NAME, 0)

def save_config_to_json(lower, upper, color_name):
    """
    Opens a file dialog and saves the current configuration to JSON.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        initialfile=f"mask_{color_name.lower()}.json",
        title="Guardar Configuración de Máscara"
    )
    
    if file_path:
        config_data = {
            "color": color_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "bounds": {
                "lower": lower,
                "upper": upper
            },
            "space": "LAB"
        }
        try:
            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=4)
            return True, file_path
        except Exception as e:
            return False, str(e)
    return None, None

def nothing(x):
    pass
# --------------------Helper Functions-----------------

# --------------------Test Loop------------------------
def run_test():
    global save_triggered, save_status, save_status_frames
    
    vision = VisionController(0)
    
    if not vision.camera_cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    # Create Main Window with trackbars at top
    cv.namedWindow(WINDOW_NAME)
    
    # --- Trackbars Panel (All controls in one place) ---
    # Color Selector
    cv.createTrackbar("Color:", WINDOW_NAME, 0, 5, on_color_selector_change)
    
    # LAB Values
    cv.createTrackbar("L-min", WINDOW_NAME, 0, 255, nothing)
    cv.createTrackbar("L-max", WINDOW_NAME, 255, 255, nothing)
    cv.createTrackbar("A-min", WINDOW_NAME, 0, 255, nothing)
    cv.createTrackbar("A-max", WINDOW_NAME, 255, 255, nothing)
    cv.createTrackbar("B-min", WINDOW_NAME, 0, 255, nothing)
    cv.createTrackbar("B-max", WINDOW_NAME, 255, 255, nothing)
    
    # Save Button (implemented as trackbar)
    cv.createTrackbar(">>> GUARDAR JSON <<<", WINDOW_NAME, 0, 1, on_save_button_change)

    # Initialize with first color
    on_color_selector_change(0)

    test_roi = ROI(0, 0, vision.image_width, vision.image_height)

    print("Sistema activo. Panel de control integrado arriba.")
    print("Click en 'GUARDAR JSON' para exportar configuración.")

    while True:
        if not vision.receive_image():
            break

        # 1. Get Values
        color_idx = cv.getTrackbarPos("Color:", WINDOW_NAME)
        current_color_name = COLOR_PRESETS[color_idx]["name"]
        
        l_min = cv.getTrackbarPos("L-min", WINDOW_NAME)
        l_max = cv.getTrackbarPos("L-max", WINDOW_NAME)
        a_min = cv.getTrackbarPos("A-min", WINDOW_NAME)
        a_max = cv.getTrackbarPos("A-max", WINDOW_NAME)
        b_min = cv.getTrackbarPos("B-min", WINDOW_NAME)
        b_max = cv.getTrackbarPos("B-max", WINDOW_NAME)

        # Validation
        if l_min > l_max: l_max = l_min
        if a_min > a_max: a_max = a_min
        if b_min > b_max: b_max = b_min

        lower = [l_min, a_min, b_min]
        upper = [l_max, a_max, b_max]

        # 2. Process Image
        mask = vision.find_mask([lower, upper], test_roi)
        result = cv.bitwise_and(vision.frame, vision.frame, mask=mask)
        mask_color = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

        # 3. Create Video Layout (Original | Mask | Result)
        combined_video = np.hstack([vision.frame, mask_color, result])
        
        # Add overlay text on video with current values
        cv.putText(combined_video, f"Color: {current_color_name}", 
                   (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv.putText(combined_video, f"LAB: [{l_min},{a_min},{b_min}] - [{l_max},{a_max},{b_max}]", 
                   (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Add save status on video
        if save_status != "LISTO":
            cv.putText(combined_video, f"Estado: {save_status}", 
                       (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            save_status_frames += 1
            if save_status_frames > 60:  # Show status for ~2 seconds
                save_status = "LISTO"
                save_status_frames = 0

        # 4. Handle Save Request
        if save_triggered:
            save_status = "Guardando..."
            success, msg = save_config_to_json(lower, upper, current_color_name)
            if success:
                save_status = f"Guardado: {msg.split('/')[-1]}"
            else:
                save_status = "Error al guardar"
            save_triggered = False

        # 5. Show Unified Interface
        cv.imshow(WINDOW_NAME, combined_video)

        # Exit
        if cv.waitKey(1) & 0xFF == ord('q'):
            print(f"\nSistema detenido. Última config: {current_color_name}")
            print(f"Lower: {lower}, Upper: {upper}")
            break

    vision.camera_cap.release()
    cv.destroyAllWindows()
# --------------------Test Loop------------------------

if __name__ == "__main__":
    run_test()