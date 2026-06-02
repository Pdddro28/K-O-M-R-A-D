import cv2
from vision_controller import ROI, VisionController

# 1. Initialize Picamera2
picam2 = VisionController()  # This will initialize the camera and set it up for OpenCV processing

color =  [[30, 170, 120],[255, 255, 170]]
roi = ROI(0, 0, picam2.image_height, picam2.image_width)
print("Camera started. Press 'q' to quit.")

try:
    while True:
        # Capture the current frame as a NumPy array
        picam2.receive_image()
        red_ctn = picam2.find_contours(color, roi) 
        max_ctn = picam2.max_contour(red_ctn, roi)
        picam2.draw_contours(red_ctn, roi, (0, 0, 255))  
        picam2.draw_centroid_line(max_ctn, roi)
        # Display the frame in an OpenCV window
        cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

        # Wait for 1ms and check if 'q' is pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 4. Clean up resources
    cv2.destroyAllWindows()
