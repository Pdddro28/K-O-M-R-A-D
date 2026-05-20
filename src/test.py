import cv2
from picamera2 import Picamera2

# 1. Initialize Picamera2
picam2 = Picamera2()

# 2. Configure for OpenCV (RGB888 format is standard for CV)
# You can adjust resolution and framerate here
config = picam2.create_video_configuration(main={"format": 'RGB888'})
picam2.configure(config)

# 3. Start the camera
picam2.start()

print("Camera started. Press 'q' to quit.")

try:
    while True:
        # Capture the current frame as a NumPy array
        frame = picam2.capture_array()
        frame = cv2.flip(frame, 0)  # Flip the frame horizontally if needed
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally if needed
        # Optional: Perform OpenCV processing here
        # Example: Gray scale conversion
        # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Display the frame in an OpenCV window
        cv2.imshow('Picamera2 + OpenCV Stream', frame)

        # Wait for 1ms and check if 'q' is pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 4. Clean up resources
    picam2.stop()
    cv2.destroyAllWindows()
