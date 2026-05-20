import cv2
import numpy as np
from dataclasses import dataclass
from picamera2 import Picamera2  # Librería necesaria
import time

@dataclass
class ROI:
    """Recive two points from the frame to extract the Region Of Interest"""
    x1: int; y1: int
    x2: int; y2: int

class VisionController():
    """
    Initialize the vision controller with the PiCamera
    """
    def __init__(self):
        # Configuraciones de resolución
        self.image_width  = 640
        self.image_height = 370
        self.image_lab = 0
        self.frame = None

        # Inicialización de PiCamera
        self.camera = Picamera2()
        self.camera.resolution = (self.image_width, self.image_height)
        self.camera.framerate = 32
        config = self.camera.create_video_configuration(main={"format": 'RGB888', 'size': (self.image_width, self.image_height)})
        self.camera.configure(config)
        self.camera.start()
        
        # Tiempo de espera para que la cámara caliente (opcional pero recomendado)
        time.sleep(0.1)

    def receive_image(self):
        """Receive image array from PiCamera and convert it to LAB format"""
        

        # Obtenemos la imagen como un array de numpy (formato OpenCV)
        self.frame = self.camera.capture_array('main')
        self.frame = cv2.flip(self.frame, 0)
        self.frame = cv2.flip(self.frame, 1)

        if self.frame is None:
            print("No se pudo obtener imagen de la PiCamera.")
            return

        # Procesamiento
        self.image_lab = cv2.cvtColor(self.frame, cv2.COLOR_BGR2LAB)
        self.image_lab = cv2.GaussianBlur(self.image_lab, (7,7), 0)

    def draw_roi(self, roi):
        cv2.rectangle(self.frame, (roi.x1, roi.y1), (roi.x2, roi.y2), (0,255,0), 2)

    def draw_contours(self, cnt, roi, color):
        cv2.drawContours(self.frame[roi.y1:roi.y2, roi.x1:roi.x2], cnt, -1, color, 2)

    def find_contours(self, range_colors, roi: ROI):
        img_segmented = self.image_lab[roi.y1:roi.y2, roi.x1:roi.x2]
        lower_mask = np.array(range_colors[0])
        upper_mask = np.array(range_colors[1])
        mask = cv2.inRange(img_segmented, lower_mask, upper_mask)
        kernel = np.ones((5, 5), np.uint8)
        eroded_mask = cv2.erode(mask, kernel, iterations=1)
        dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=1)
        contours = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        return contours
    
    def max_contour(self, contours, roi: ROI):
        max_area = 0
        max_y = 0
        max_x = 0
        max_cnt = None

        for c in contours:
            area = cv2.contourArea(c)
            if area > 100:
                approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
                x, y, w, h = cv2.boundingRect(approx)
                x += roi.x1 + w // 2
                y += roi.y1 + h // 2

                if area > max_area:
                    max_area = area
                    max_y = y
                    max_x = x
                    max_cnt = c

        return [max_area, max_x, max_y, max_cnt]