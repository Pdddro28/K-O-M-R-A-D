import serial
import time
import threading
import pandas as pd
import random
from vision_controller import VisionController
import json
import cv2
from dataclasses import dataclass

@dataclass
class ROI:
    """Recive two points from the frame  to extract the Region Of Interest"""

    x1: int; y1: int
    x2: int; y2: int



class MegaPiController:
    """
    Controller class for MegaPi robot.
    Handles movement, telemetry, and data logging for ML training.
    """


    def __init__(self, port='COM9', baudrate=115200 ):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            time.sleep(2) 
            print(f"✅ System: Connected to MegaPi on {port}")
            
            # Distance variables (3 sensors: Front, Left, Right)
            self.dist_front = 0
            self.dist_left = 0
            self.dist_right = 0
            
            # Data Logging List (For Pandas)
            self.data_log = []
            self.log_index = 0
            self.vision = VisionController()  # Assuming specified camera is used for vision
            # Thread setup
            time.sleep(1)  # Give the serial connection a moment to stabilize
            self.running = True
            self.reader_thread = threading.Thread(target=self._read_telemetry, daemon=True)
            self.reader_thread.start()
            self.button_value = 0
            self.turning_direction = 0 # 0: No turn, 1: Left, 2: Right

            # Action Constants
            self.ACTION_LEFT = 0
            self.ACTION_FORWARD = 1
            self.ACTION_RIGHT = 2

            # Carga de máscaras
            self.load_masks()

            # Color Areas 
            self.black_area = 0
            self.black_area_derecha = 0
            self.blue_area = 0
            self.orange_area = 0
            self.green_area = 0
            self.red_area = 0
            
            #Region´s of interest
            self.rois = [
                ROI(200, 50, 430, 200),
                ROI(200, 300, 440, 350)
            ]

        except Exception as e:
            print(f"❌ Critical Error: Could not connect to {port}. {e}")
            exit()

    def _read_telemetry(self):
            """Background loop to parse incoming sensor data (Header + 5 bytes)."""
            while self.running:
                try:
                    # Necesitamos al menos 6 bytes para un paquete completo
                    if self.ser.in_waiting >= 6:
                        header = self.ser.read(1)
                        
                        if header == b'\xaa':
                            # Leemos exactamente los 5 bytes restantes: 
                            # [Front, Left, Right, Button, Padding]
                            payload = self.ser.read(5)
                            
                            self.dist_front = payload[0]
                            self.dist_left  = payload[1]
                            self.dist_right = payload[2]
                            self.button_value = payload[3]  # El botón es el 4to byte (índice 3)
                            
                        else:
                            # Si no es el header, limpiamos el buffer para buscar el próximo AA
                            # Esto evita que el error se arrastre
                            line = self.ser.readline().decode('ascii', errors='ignore').strip()
                            if line:
                                print(f"   [MegaPi Debug]: {line}")
                except Exception as e:
                    print(f"Telemetry Error: {e}")
                
                time.sleep(0.01) # Pequeño respiro para el procesador
    
    def _send_command(self, action, v1=0, v2=0):
        header = 0xFF
        msg_type = 0x01
        package = bytearray([header, msg_type, action, v1, v2])
        self.ser.write(package)

# -------------------------------------Vision stuff------------------------------------ 
    def get_masks(self, color):
        with open(f'src/Colors/mask_{color}.json') as f:
            config = json.load(f)
        lower = config['bounds']['lower']
        upper = config['bounds']['upper']
        return [lower, upper]

    def load_masks(self):

        # Carga de máscaras
        self.mask_blue = self.get_masks('azul')
        self.mask_orange = self.get_masks('naranja')
        self.mask_black = self.get_masks('negro')
        #self.mask_green = self.get_masks('verde')
        #self.mask_red = self.get_masks('rojo')
        #self.mask_purple = self.get_masks('morado')

    def obtenerarea_frontal(self):
        self.cnt_front_wall = self.vision.find_contours(self.mask_black, self.rois[0])
        self.black_area = self.vision.max_contour(self.cnt_front_wall, self.rois[0])[0]

    def obtener_linea_naranja(self):
        self.cnt_orange_line = self.vision.find_contours(self.mask_orange, self.rois[1])
        self.orange_area = self.vision.max_contour(self.cnt_orange_line, self.rois[1])[0]

    def obtener_linea_azul(self):
        self.cnt_blue_line = self.vision.find_contours(self.mask_blue, self.rois[1])
        self.blue_area = self.vision.max_contour(self.cnt_blue_line, self.rois[1])[0]
    

    def debug_UI(self):
        # Llamar a la función con corrección de posición
        for item in self.rois:
            self.vision.draw_roi(item)  # ROI para pared frontal
        self.vision.draw_contours(self.cnt_blue_line, self.rois[1], (255, 0, 0))  # Contornos de línea azul
        self.vision.draw_contours(self.cnt_orange_line, self.rois[1], (0, 165, 255))  # Contornos de línea naranja
        self.vision.draw_contours(self.cnt_front_wall, self.rois[0], (0, 0, 255))  # Contornos de pared frontal izquierda

            # Mostrar áreas en la consola
        cv2.imshow('Vision HD - Posicion Corregida', self.vision.frame)



# -------------------------------------Vision stuff------------------------------------ 

    def log_step(self, action_code):
        d_front, d_left, d_right = self.get_distances()

        
        self.data_log.append({
            'index': self.log_index,
            'dist_front_cm': d_front,
            'dist_left_cm': d_left,
            'dist_right_cm': d_right,
        })
        
        self.log_index += 1

    def move_forward(self, speed, log=True):
        self._send_command(1, v1=speed)
        if log: self.log_step(self.ACTION_FORWARD)


    def move_backward(self, speed, log=True):
        #print(f"CMD: Backward | Speed: {speed}")
        self._send_command(2, v1=speed)
        if log: self.log_step(self.ACTION_FORWARD)

    def turn_direction(self):
        if self.turning_direction == 1:
            self.turn_left(angle=40, speed=50, log=True) # OLVIDENSE DE ESTO
        elif self.turning_direction == 2:
            self.turn_right(angle=120, speed=50, log=True) # ESTAMOS AQUI

    def turn_left(self, angle, speed, log=True):
        #print(f"CMD: Turn Left | Angle: {angle} | Speed: {speed}")
        self._send_command(3, v1=angle, v2=speed)
        if log: self.log_step(self.ACTION_LEFT)

    def turn_right(self, angle, speed, log=True):
        #print(f"CMD: Turn Right | Angle: {angle} | Speed: {speed}")
        self._send_command(4, v1=angle, v2=speed)
        if log: self.log_step(self.ACTION_RIGHT)

    def turn_center(self, log=True):
        #print("CMD: Turn Center")
        self._send_command(6)
        if log: self.log_step(self.ACTION_FORWARD)

    def stop(self, log=True):
        #print("CMD: Stop")
        self._send_command(5)
        #if log: self.log_step(self.ACTION_FORWARD)

    def get_distances(self):
        return (self.dist_front, self.dist_left, self.dist_right)

    def save_data_to_csv(self, filename='training_data.csv'):
        if not self.data_log:
            print("⚠️ No data collected to save.")
            return

        try:
            df = pd.DataFrame(self.data_log)
            df.set_index('index', inplace=True)
            df.to_csv(filename, index=True)
            print(f"\n✅ Success: Saved {len(df)} records to '{filename}'")
            print(df.head())
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")

    def close(self):
        self.running = False
        if hasattr(self, 'ser') and self.ser.is_open:
            self.stop(log=False)
            self.ser.close()
            print("System: Connection closed.")

    def start (self):
        return self.button_value == 1

