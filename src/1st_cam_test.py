# --------------------libraries------------------------
import cv2 as cv
import numpy as np
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
        # Default resolution for processing stability
        self.image_width  = 640
        self.image_height = 480
        self.image_lab = None
        self.frame = None
        
        # Camera hardware initialization
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
        # Convert BGR (OpenCV default) to LAB space
        self.image_lab = cv.cvtColor(self.frame, cv.COLOR_BGR2LAB)
        # Apply blur to reduce high-frequency noise/grain
        self.image_lab = cv.GaussianBlur(self.image_lab, (7,7), 0)
        return True

    def find_mask(self, color_range, roi):
        """
        Generates a binary mask based on a color range within a ROI.
        """
        # Crop the image to the specified region
        img_segmented = self.image_lab[roi.y1:roi.y2, roi.x1:roi.x2]
        lower = np.array(color_range[0])
        upper = np.array(color_range[1])
        
        # Binary segmentation: pixels in range become white (255)
        mask = cv.inRange(img_segmented, lower, upper)
        
        # Morphological operations to clean the binary image
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=1)  # Removes small dots
        mask = cv.dilate(mask, kernel, iterations=1) # Restores object size
        return mask
# --------------------Classes--------------------------

# --------------------Helper Functions-----------------
def nothing(x):
    """Placeholder function for trackbar callbacks"""
    pass
# --------------------Helper Functions-----------------

# --------------------Test Loop------------------------
def run_test():
    # Instance of the controller using laptop's integrated camera (0)
    vision = VisionController(0)
    
    # Trackbar Interface for real-time color calibration
    cv.namedWindow("Trackbars")
    cv.createTrackbar("L-min", "Trackbars", 0, 255, nothing)
    cv.createTrackbar("L-max", "Trackbars", 255, 255, nothing)
    cv.createTrackbar("A-min", "Trackbars", 0, 255, nothing)
    cv.createTrackbar("A-max", "Trackbars", 255, 255, nothing)
    cv.createTrackbar("B-min", "Trackbars", 0, 255, nothing)
    cv.createTrackbar("B-max", "Trackbars", 255, 255, nothing)

    # Full screen Region of Interest for testing
    test_roi = ROI(0, 0, 640, 480)

    print("System active. Press 'q' to stop and print values.")

    while True:
        if not vision.receive_image():
            break

        # Fetch current UI slider values
        l_min = cv.getTrackbarPos("L-min", "Trackbars")
        l_max = cv.getTrackbarPos("L-max", "Trackbars")
        a_min = cv.getTrackbarPos("A-min", "Trackbars")
        a_max = cv.getTrackbarPos("A-max", "Trackbars")
        b_min = cv.getTrackbarPos("B-min", "Trackbars")
        b_max = cv.getTrackbarPos("B-max", "Trackbars")

        lower = [l_min, a_min, b_min]
        upper = [l_max, a_max, b_max]

        # Generate the black and white mask
        mask = vision.find_mask([lower, upper], test_roi)
        
        # Merge mask with original frame to see color result
        result = cv.bitwise_and(vision.frame, vision.frame, mask=mask)

        # Output windows
        cv.imshow("Original con ROI", vision.frame)
        cv.imshow("Mascara (Blanco y Negro)", mask)
        cv.imshow("Resultado (Color Filtrado)", result)

        # Break loop on 'q' key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            print(f"Calibration Complete.")
            print(f"Lower Bound: {lower}")
            print(f"Upper Bound: {upper}")
            break

    # Hardware cleanup
    vision.camera_cap.release()
    cv.destroyAllWindows()
# --------------------Test Loop------------------------

if __name__ == "__main__":
    run_test()
