import cv2 as cv
import numpy as np
from dataclasses import dataclass
from picamera import PiCamera  # Librería necesaria
from picamera.array import PiRGBArray # Para convertir a arrays de numpy
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
        self.image_height = 480
        self.image_lab = 0
        self.frame = None

        # Inicialización de PiCamera
        self.camera = PiCamera()
        self.camera.resolution = (self.image_width, self.image_height)
        self.camera.framerate = 32
        
        # Generamos el buffer para capturar imágenes
        self.raw_capture = PiRGBArray(self.camera, size=(self.image_width, self.image_height))

        # Tiempo de espera para que la cámara caliente (opcional pero recomendado)
        time.sleep(0.1)

    def receive_image(self):
        """Receive image array from PiCamera and convert it to LAB format"""
        
        # Limpiamos el buffer antes de la nueva captura
        self.raw_capture.truncate(0)
        
        # Capturamos un solo frame
        self.camera.capture(self.raw_capture, format="bgr", use_video_port=True)
        
        # Obtenemos la imagen como un array de numpy (formato OpenCV)
        self.frame = self.raw_capture.array

        if self.frame is None:
            print("No se pudo obtener imagen de la PiCamera.")
            return

        # Procesamiento
        self.image_lab = cv.cvtColor(self.frame, cv.COLOR_BGR2LAB)
        self.image_lab = cv.GaussianBlur(self.image_lab, (7,7), 0)

    # ... El resto de tus métodos (draw_roi, find_contours, etc.) permanecen igual ...

    def draw_roi(self, roi):
        cv.rectangle(self.frame, (roi.x1, roi.y1), (roi.x2, roi.y2), (0,255,0), 2)

    def draw_contours(self, cnt, roi, color):
        cv.drawContours(self.frame[roi.y1:roi.y2, roi.x1:roi.x2], cnt, -1, color, 2)

    def find_contours(self, range_colors, roi: ROI):
        img_segmented = self.image_lab[roi.y1:roi.y2, roi.x1:roi.x2]
        lower_mask = np.array(range_colors[0])
        upper_mask = np.array(range_colors[1])
        mask = cv.inRange(img_segmented, lower_mask, upper_mask)
        kernel = np.ones((5, 5), np.uint8)
        eroded_mask = cv.erode(mask, kernel, iterations=1)
        dilated_mask = cv.dilate(eroded_mask, kernel, iterations=1)
        contours = cv.findContours(dilated_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
        return contours
    
    def max_contour(self, contours, roi: ROI):
        max_area = 0
        max_y = 0
        max_x = 0
        max_cnt = None

        for c in contours:
            area = cv.contourArea(c)
            if area > 100:
                approx = cv.approxPolyDP(c, 0.01 * cv.arcLength(c, True), True)
                x, y, w, h = cv.boundingRect(approx)
                x += roi.x1 + w // 2
                y += roi.y1 + h // 2

                if area > max_area:
                    max_area = area
                    max_y = y
                    max_x = x
                    max_cnt = c

        return [max_area, max_x, max_y, max_cnt]