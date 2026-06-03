import cv2
import numpy as np
from dataclasses import dataclass
from picamera2 import Picamera2  
import time
import traceback

# --- DATA STRUCTURES ---
@dataclass
class ROI:
    x1: int; y1: int
    x2: int; y2: int

# --- VISION SYSTEM CONTROLLER ---
class VisionController():
    
    # --- INITIALIZATION AND CAMERA SETUP ---
    def __init__(self):
        self.image_width  = 640
        self.image_height = 370
        self.image_lab = 0
        
        # Almacenamiento para los frames paralelos
        self.frame = None       # Frame principal para dibujo (BGR en OpenCV)
        self.frame_rgb = None   # Frame en formato RGB nativo
        self.frame_bgr = None   # Frame en formato BGR limpio

        self.camera = Picamera2()
        self.camera.resolution = (self.image_width, self.image_height)
        self.camera.framerate = 32
        
        # Configuración nativa en RGB888
        config = self.camera.create_video_configuration(main={"format": 'RGB888', 'size': (self.image_width, self.image_height)})
        self.camera.configure(config)
        self.camera.start()
        
        time.sleep(0.1)

    # --- IMAGE ACQUISITION AND PROCESSING ---
    def receive_image(self):
        # 1. Captura del array nativo (RGB)
        raw_frame = self.camera.capture_array('main')
        raw_frame = cv2.flip(raw_frame, 0)
        raw_frame = cv2.flip(raw_frame, 1)

        # 2. Producción de los frames paralelos solicitados
        self.frame_rgb = raw_frame.copy()                           # Frame RGB puro
        self.frame_bgr = cv2.cvtColor(raw_frame, cv2.COLOR_RGB2BGR) # Frame BGR puro
        
        # Asignamos self.frame como BGR para que las funciones de dibujo pinten con colores correctos
        self.frame = self.frame_bgr.copy()

        # 3. Pipeline de procesamiento en espacio de color LAB
        self.image_lab = cv2.cvtColor(self.frame_rgb, cv2.COLOR_RGB2LAB)
       
        l_channel, a_channel, b_channel = cv2.split(self.image_lab)
       
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl_channel = clahe.apply(l_channel)
       
        self.image_lab = cv2.merge((cl_channel, a_channel, b_channel))
        self.image_lab = cv2.GaussianBlur(self.image_lab, (7, 7), 0)

    # --- DRAWING UTILITIES ---
    def draw_roi(self, roi):
        cv2.rectangle(self.frame, (roi.x1, roi.y1), (roi.x2, roi.y2), (0,255,0), 2)

    def draw_contours(self, cnt, roi, color):
        cv2.drawContours(self.frame[roi.y1:roi.y2, roi.x1:roi.x2], cnt, -1, color, 2)

    def draw_centroid_line(self, max_contour_data, roi: ROI, color=(255, 0, 0), thickness=2):
        max_cnt = max_contour_data[3]
        if max_cnt is None:
            return None

        M = cv2.moments(max_cnt)
        if M["m00"] != 0:
            global_cx = int(M["m10"] / M["m00"]) + roi.x1
            cv2.line(self.frame, (global_cx, roi.y1), (global_cx, roi.y2), color, thickness)
            
            global_cy = int(M["m01"] / M["m00"]) + roi.y1
            cv2.circle(self.frame, (global_cx, global_cy), 5, color, -1)
            return (global_cx, global_cy)
        else:
            return None

    def draw_parallel_lane_line(self, centroid_coords, roi: ROI, offset=80, avoid_right=True, color=(0, 255, 255), thickness=2):
        if centroid_coords is None:
            return None

        global_cx, global_cy = centroid_coords

        if avoid_right:
            lane_x = global_cx + offset
        else:
            lane_x = global_cx - offset

        lane_x = max(0, min(lane_x, self.image_width))
        cv2.line(self.frame, (lane_x, roi.y1), (lane_x, roi.y2), color, thickness)
        
        arrow_direction = 30 if avoid_right else -30
        cv2.arrowedLine(self.frame, (global_cx, global_cy), (global_cx + arrow_direction, global_cy), color, 2, tipLength=0.3)

        return lane_x

    # --- COMPUTER VISION ALGORITHMS ---
    def find_contours(self, range_colors, roi: ROI, frame_mode='lab'):
        """
        Busca contornos permitiendo escoger cuál frame paralelo/espacio utilizar.
        :param frame_mode: 'lab', 'rgb' o 'bgr'
        """
        # Declaración que permite elegir el frame objetivo
        if frame_mode.lower() == 'rgb':
            img_source = self.frame_rgb
        elif frame_mode.lower() == 'bgr':
            img_source = self.frame_bgr
        else:
            img_source = self.image_lab # Por defecto usa LAB procesado
            
        img_segmented = img_source[roi.y1:roi.y2, roi.x1:roi.x2]
        
        lower_mask = np.array(range_colors[0])
        upper_mask = np.array(range_colors[1])
        mask = cv2.inRange(img_segmented, lower_mask, upper_mask)
       
        kernel = np.ones((5, 5), np.uint8)
        smoothed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        smoothed_mask = cv2.morphologyEx(smoothed_mask, cv2.MORPH_OPEN, kernel)
       
        contours = cv2.findContours(smoothed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
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


# --- TESTING SCRIPT ---
def probar_sistema_vision():
    print("Inicializando la cámara Picamera2... Espera un momento.")
    try:
        # Instanciación corregida con mayúsculas exactas
        vision = VisionController()
        print("Cámara inicializada con éxito.")
        print("Controles: Presiona 'q' en cualquiera de las ventanas para salir.")
        
        time.sleep(1) 
        
        while True:
            # Capturar nueva imagen y generar los frames paralelos
            vision.receive_image()
            
            # Mostrar los 4 flujos en ventanas separadas para comparar
            cv2.imshow("1. Frame Principal (Para Dibujo)", vision.frame)
            cv2.imshow("2. Frame BGR Limpio", vision.frame_bgr)
            cv2.imshow("3. Frame RGB Puro (Invertido en imshow)", vision.frame_rgb)
            cv2.imshow("4. Espacio LAB Preprocesado", vision.image_lab)
            
            # Romper el bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Cerrando la prueba...")
                break
                
    except Exception as e:
        print("\n[ERROR] Ocurrió un fallo en el sistema de visión:")
        traceback.print_exc()
        
    finally:
        # Liberación limpia de recursos visuales
        cv2.destroyAllWindows()
        print("Prueba finalizada de forma segura.")

if __name__ == "__main__":
    probar_sistema_vision()
