# --------------------libraries------------------------
import cv2 as cv
import numpy as np
# --------------------libraries------------------------

# --------------------Classes--------------------------
class ROI:
    """Define el área de búsqueda (Región de Interés)"""
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

class VisionController():
    """Controlador de hardware y procesamiento de imagen"""
    def __init__(self, usb_port=0):
        self.image_width  = 640
        self.image_height = 480
        self.camera_cap = cv.VideoCapture(usb_port)
        self.camera_cap.set(cv.CAP_PROP_FRAME_WIDTH, self.image_width)
        self.camera_cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.image_height)

    def receive_image(self):
        """Captura y pre-procesa el frame actual"""
        ret, frame_read = self.camera_cap.read()
        if not ret: return False
        self.frame = frame_read
        # Filtro LAB para estabilidad ante cambios de luz
        self.image_lab = cv.cvtColor(self.frame, cv.COLOR_BGR2LAB)
        self.image_lab = cv.GaussianBlur(self.image_lab, (5,5), 0)
        return True

    def find_mask(self, color_range, roi):
        """Genera máscara binaria y limpia ruido morfológico"""
        img_segmented = self.image_lab[roi.y1:roi.y2, roi.x1:roi.x2]
        mask = cv.inRange(img_segmented, np.array(color_range[0]), np.array(color_range[1]))
        
        # Operaciones morfológicas para una máscara limpia
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel) # Elimina ruido
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) # Cierra huecos
        return mask
# --------------------Classes--------------------------

# --------------------Constants & Profiles--------------
# Perfiles base para evitar que el usuario empiece de cero
# Orden: [L, A, B]
COLOR_PROFILES = {
    0: {"name": "ROJO",   "range": [[40, 160, 130], [180, 255, 255]], "bgr": (0, 0, 255)},
    1: {"name": "VERDE",  "range": [[50, 40, 140],  [200, 110, 255]], "bgr": (0, 255, 0)},
    2: {"name": "BLANCO", "range": [[210, 120, 120], [255, 135, 135]], "bgr": (255, 255, 255)},
    3: {"name": "NEGRO",  "range": [[0, 120, 120],   [60, 135, 135]],   "bgr": (40, 40, 40)}
}
# --------------------Constants & Profiles--------------

def nothing(x): pass

def run_test():
    vision = VisionController(0)
    
    # --- Configuración de Interfaz Única ---
    cv.namedWindow("Dashboard de Control", cv.WINDOW_AUTOSIZE)
    
    # Selector de color (Modo Único)
    cv.createTrackbar("MODO (R:0, V:1, B:2, N:3)", "Dashboard de Control", 0, 3, nothing)
    
    # Sliders de ajuste fino
    cv.createTrackbar("L-min", "Dashboard de Control", 0, 255, nothing)
    cv.createTrackbar("L-max", "Dashboard de Control", 255, 255, nothing)
    cv.createTrackbar("A-min", "Dashboard de Control", 0, 255, nothing)
    cv.createTrackbar("A-max", "Dashboard de Control", 255, 255, nothing)
    cv.createTrackbar("B-min", "Dashboard de Control", 0, 255, nothing)
    cv.createTrackbar("B-max", "Dashboard de Control", 255, 255, nothing)

    last_mode = -1
    test_roi = ROI(0, 0, 640, 480)

    while True:
        if not vision.receive_image(): break

        # 1. Obtener modo actual y forzar perfiles si cambia
        mode = cv.getTrackbarPos("MODO (R:0, V:1, B:2, N:3)", "Dashboard de Control")
        if mode != last_mode:
            p = COLOR_PROFILES[mode]
            cv.setTrackbarPos("L-min", "Dashboard de Control", p["range"][0][0])
            cv.setTrackbarPos("A-min", "Dashboard de Control", p["range"][0][1])
            cv.setTrackbarPos("B-min", "Dashboard de Control", p["range"][0][2])
            cv.setTrackbarPos("L-max", "Dashboard de Control", p["range"][1][0])
            cv.setTrackbarPos("A-max", "Dashboard de Control", p["range"][1][1])
            cv.setTrackbarPos("B-max", "Dashboard de Control", p["range"][1][2])
            last_mode = mode

        # 2. Leer valores de ajuste manual
        low = [cv.getTrackbarPos("L-min", "Dashboard de Control"),
               cv.getTrackbarPos("A-min", "Dashboard de Control"),
               cv.getTrackbarPos("B-min", "Dashboard de Control")]
        high = [cv.getTrackbarPos("L-max", "Dashboard de Control"),
                cv.getTrackbarPos("A-max", "Dashboard de Control"),
                cv.getTrackbarPos("B-max", "Dashboard de Control")]

        # 3. Procesar Máscara Exclusiva
        mask = vision.find_mask([low, high], test_roi)
        mask_3ch = cv.cvtColor(mask, cv.COLOR_GRAY2BGR) # Para poder concatenar
        
        # Aplicar máscara al frame original
        result = cv.bitwise_and(vision.frame, vision.frame, mask=mask)

        # 4. Construcción del Dashboard Visual (HSTACK)
        # Añadimos etiquetas de texto
        cv.putText(vision.frame, f"VISTA REAL - MODO: {COLOR_PROFILES[mode]['name']}", (15, 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_PROFILES[mode]['bgr'], 2)
        cv.putText(result, "DETECCION AISLADA", (15, 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Unir las dos imágenes horizontalmente
        combined_view = np.hstack((vision.frame, result))
        
        # Redimensionar para que quepa bien en laptops (opcional)
        display_res = cv.resize(combined_view, (1280, 480))

        cv.imshow("Dashboard de Control", display_res)

        if cv.waitKey(1) & 0xFF == ord('q'): 
            print(f"Valores Finales ({COLOR_PROFILES[mode]['name']}): Low:{low}, High:{high}")
            break

    vision.camera_cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    run_test()