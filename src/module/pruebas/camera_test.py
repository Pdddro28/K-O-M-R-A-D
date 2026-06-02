# ====================================================
# LIBRARIES
# ====================================================
import cv2 as cv
import numpy as np

# ====================================================
# COMPUTER VISION SUBSYSTEM DATA STRUCTURES
# ====================================================
class ROI:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

class VisionController():
    def __init__(self, usb_port=0):
        self.image_width  = 640
        self.image_height = 480
        self.camera_cap = cv.VideoCapture(usb_port)
        self.camera_cap.set(cv.CAP_PROP_FRAME_WIDTH, self.image_width)
        self.camera_cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.image_height)

    def receive_image(self):
        ret, frame_read = self.camera_cap.read()
        if not ret: 
            return False
        self.frame = frame_read
        
        self.image_lab = cv.cvtColor(self.frame, cv.COLOR_BGR2LAB)
        self.image_lab = cv.GaussianBlur(self.image_lab, (5,5), 0)
        return True

    def find_mask(self, color_range, roi):
        img_segmented = self.image_lab[roi.y1:roi.y2, roi.x1:roi.x2]
        mask = cv.inRange(img_segmented, np.array(color_range[0]), np.array(color_range[1]))
        
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel) 
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) 
        return mask

# ====================================================
# COLOR CALIBRATION PROFILE PRESETS
# ====================================================
COLOR_PROFILES = {
    0: {"name": "RED",   "range": [[40, 160, 130], [180, 255, 255]], "bgr": (0, 0, 255)},
    1: {"name": "GREEN", "range": [[50, 40, 140],  [200, 110, 255]], "bgr": (0, 255, 0)},
    2: {"name": "WHITE", "range": [[210, 120, 120], [255, 135, 135]], "bgr": (255, 255, 255)},
    3: {"name": "BLACK", "range": [[0, 120, 120],   [60, 135, 135]],  "bgr": (40, 40, 40)}
}

def nothing(x): 
    pass

# ====================================================
# CALIBRATION INTERFACE LOOP
# ====================================================
def run_test():
    vision = VisionController(0)
    window_name = "Control Dashboard"
    
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    
    cv.createTrackbar("MODE (R:0, G:1, W:2, B:3)", window_name, 0, 3, nothing)
    cv.createTrackbar("L-min", window_name, 0, 255, nothing)
    cv.createTrackbar("L-max", window_name, 255, 255, nothing)
    cv.createTrackbar("A-min", window_name, 0, 255, nothing)
    cv.createTrackbar("A-max", window_name, 255, 255, nothing)
    cv.createTrackbar("B-min", window_name, 0, 255, nothing)
    cv.createTrackbar("B-max", window_name, 255, 255, nothing)

    last_mode = -1
    test_roi = ROI(0, 0, 640, 480)

    while True:
        if not vision.receive_image(): 
            break

        mode = cv.getTrackbarPos("MODE (R:0, G:1, W:2, B:3)", window_name)
        if mode != last_mode:
            p = COLOR_PROFILES[mode]
            cv.setTrackbarPos("L-min", window_name, p["range"][0][0])
            cv.setTrackbarPos("A-min", window_name, p["range"][0][1])
            cv.setTrackbarPos("B-min", window_name, p["range"][0][2])
            cv.setTrackbarPos("L-max", window_name, p["range"][1][0])
            cv.setTrackbarPos("A-max", window_name, p["range"][1][1])
            cv.setTrackbarPos("B-max", window_name, p["range"][1][2])
            last_mode = mode

        low = [cv.getTrackbarPos("L-min", window_name),
               cv.getTrackbarPos("A-min", window_name),
               cv.getTrackbarPos("B-min", window_name)]
        high = [cv.getTrackbarPos("L-max", window_name),
                cv.getTrackbarPos("A-max", window_name),
                cv.getTrackbarPos("B-max", window_name)]

        mask = vision.find_mask([low, high], test_roi)
        result = cv.bitwise_and(vision.frame, vision.frame, mask=mask)

        cv.putText(vision.frame, f"RAW VIEW - MODE: {COLOR_PROFILES[mode]['name']}", (15, 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_PROFILES[mode]['bgr'], 2)
        cv.putText(result, "ISOLATED DETECTION", (15, 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        combined_view = np.hstack((vision.frame, result))
        display_res = cv.resize(combined_view, (1280, 480))

        cv.imshow(window_name, display_res)

        if cv.waitKey(1) & 0xFF == ord('q'): 
            print(f"Final Bounds ({COLOR_PROFILES[mode]['name']}): Low:{low}, High:{high}")
            break

    vision.camera_cap.release()
    cv.destroyAllWindows()

# ====================================================
# ENTRY POINT
# ====================================================
if __name__ == "__main__":
    run_test()
