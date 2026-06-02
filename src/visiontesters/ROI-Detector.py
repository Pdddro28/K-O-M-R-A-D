import cv2
from dataclasses import dataclass
import tkinter as tk
from tkinter import filedialog

# --- DATA STRUCTURES ---
@dataclass
class ROI:
    x1: int; y1: int
    x2: int; y2: int

# --- GLOBAL VARIABLES ---
drawing = False
ix, iy = -1, -1
rois = []

window_width = 800
window_height = 600

# --- FILE MANAGEMENT AND EXPORT ---
def save_rois_dialog():
    if not rois:
        print("No hay ROIs para guardar")
        return

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python files", "*.py")],
        title="Guardar ROIs como..."
    )

    if not file_path:
        print("Guardado cancelado")
        return

    with open(file_path, "w") as f:
        f.write("from dataclasses import dataclass\n\n")
        f.write("@dataclass\n")
        f.write("class ROI:\n")
        f.write("    x1: int; y1: int\n")
        f.write("    x2: int; y2: int\n\n\n")

        f.write("rois = [\n")
        for (x1, y1, x2, y2) in rois:
            f.write(f"    ROI({x1}, {y1}, {x2}, {y2}),\n")
        f.write("]\n")

    print(f"ROIs guardadas en: {file_path}")

# --- MOUSE INTERACTION CALLBACK ---
def mouse_callback(event, x, y, flags, param):
    global ix, iy, drawing, rois

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            param["temp_rect"] = (ix, iy, x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rois.append((ix, iy, x, y))
        param["temp_rect"] = None

# --- MAIN EXECUTION APPLICATION ---
def main():
    global rois

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara")
        return

    window_name = "Camara"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_width, window_height)

    params = {"temp_rect": None}
    cv2.setMouseCallback(window_name, mouse_callback, params)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

            h, w = frame.shape[:2]

            scale = min(window_width / w, window_height / h)
            new_w = int(w * scale)
            new_h = int(h * scale)

            resized = cv2.resize(frame, (new_w, new_h))

            top = (window_height - new_h) // 2
            bottom = window_height - new_h - top
            left = (window_width - new_w) // 2
            right = window_width - new_w - left

            framed = cv2.copyMakeBorder(
                resized,
                top, bottom, left, right,
                cv2.BORDER_CONSTANT,
                value=[0, 0, 0]
            )

            display = framed.copy()

            for i, (x1, y1, x2, y2) in enumerate(rois):
                x1_, y1_ = min(x1, x2), min(y1, y2)
                x2_, y2_ = max(x1, x2), max(y1, y2)

                width = x2_ - x1_
                height = y2_ - y1_

                cv2.rectangle(display, (x1_, y1_), (x2_, y2_), (0, 255, 0), 2)

                label = f"ROI {i+1}: {width}x{height}"
                cv2.putText(display, label, (x1_, y1_ - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if params["temp_rect"]:
                x1, y1, x2, y2 = params["temp_rect"]
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 255), 1)

            cv2.imshow(window_name, display)

            key = cv2.waitKey(1)

            if key == 27:
                break
            elif key == ord('c'):
                rois = []

    finally:
        cap.release()
        cv2.destroyAllWindows()
        save_rois_dialog()

if __name__ == "__main__":
    main()
