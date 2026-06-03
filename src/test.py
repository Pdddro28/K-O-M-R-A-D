import cv2
from vision_controller import ROI, VisionController
from PID_class import PIDController

# 1. Initialize Picamera2
picam2 = VisionController()  # This will initialize the camera and set it up for OpenCV processing

color_r =  [[0, 151, 76],[255, 252, 197]]
color_g =  [[30, 45, 119],[255, 114, 182]]
roi = ROI(0, 0, picam2.image_width, picam2.image_height)
print("Camera started. Press 'q' to quit.")
set_point_red = (135, 165)
set_point_green = (430, 125)
pid_red = PIDController(Kp=0.5, Ki=0.00, Kd=0.1, set_point=set_point_red)
pid_green = PIDController(Kp=0.5, Ki=0.00, Kd=0.1, set_point=set_point_green)

try:
    while True:
        # Capture the current frame as a NumPy array
        picam2.receive_image()
        red_ctn = picam2.find_contours(color_r, roi) 
        max_ctn = picam2.max_contour(red_ctn, roi)
        picam2.draw_contours(red_ctn, roi, (0, 0, 255))  
        centroid_coords = picam2.draw_centroid_line(max_ctn, roi)
        print(f"Centroid coordinates: {centroid_coords}")
        picam2.draw_parallel_lane_line(centroid_coords, roi, offset=200, avoid_right=False)
        picam2.draw_roi(roi)  # Draw the ROI in blue
        # Display the frame in an OpenCV window
        cv2.imshow('Picamera2 + OpenCV Stream', picam2.frame)

        # Wait for 1ms and check if 'q' is pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 4. Clean up resources
    cv2.destroyAllWindows()
