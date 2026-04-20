import serial
import time
import threading

class MegaPiController:
    """
    Controller class for MegaPi robot.
    Handles movement commands and asynchronous sensor data retrieval.
    """

    def __init__(self, port='COM9', baudrate=115200):
        """
        Initializes serial connection on Windows and starts the telemetry thread.
        """
        try:
            # On Windows, we just use the port name like 'COM9'
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            time.sleep(2)  # Critical: Wait for Arduino to reboot after connection
            print(f"✅ System: Connected to MegaPi on {port}")
            
            # Distance variables (updated by background thread)
            self.dist_sensor1 = 400
            self.dist_sensor2 = 400
            
            # Start Background Telemetry Thread
            self.running = True
            self.reader_thread = threading.Thread(target=self._read_telemetry, daemon=True)
            self.reader_thread.start()

        except Exception as e:
            print(f"❌ Critical Error: Could not connect to {port}. {e}")
            exit()

    def _read_telemetry(self):
        """
        Private method: Background loop to parse incoming sensor data and debug text.
        """
        while self.running:
            try:
                if self.ser.in_waiting >= 1:
                    # Look for the binary telemetry header (0xAA)
                    header = self.ser.read(1)
                    
                    if header == b'\xaa':
                        # Read the next 4 bytes: [Dist1, Dist2, Padding, Padding]
                        if self.ser.in_waiting >= 4:
                            payload = self.ser.read(4)
                            self.dist_sensor1 = payload[0]
                            self.dist_sensor2 = payload[1]
                    else:
                        # If it's text (like our Arduino debug prints), try to read the line
                        line = self.ser.readline().decode('ascii', errors='ignore').strip()
                        if line:
                            print(f"   [MegaPi Debug]: {line}")
            except Exception as e:
                # Silently handle transient serial errors
                pass
            time.sleep(0.01)

    def _send_command(self, action, v1=0, v2=0):
        """
        Sends the 5-byte protocol packet to the MegaPi.
        """
        header = 0xFF
        msg_type = 0x01
        package = bytearray([header, msg_type, action, v1, v2])
        self.ser.write(package)

    def move_forward(self, speed, duration=None):
        """Moves the car forward."""
        print(f"CMD: Forward | Speed: {speed}")
        self._send_command(1, v1=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def move_backward(self, speed, duration=None):
        """Moves the car backward."""
        print(f"CMD: Backward | Speed: {speed}")
        self._send_command(2, v1=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, angle, speed, duration=None):
        """Adjusts steering left and moves."""
        print(f"CMD: Turn Left | Angle: {angle} | Speed: {speed}")
        self._send_command(3, v1=angle, v2=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_right(self, angle, speed, duration=None):
        """Adjusts steering right and moves."""
        print(f"CMD: Turn Right | Angle: {angle} | Speed: {speed}")
        self._send_command(4, v1=angle, v2=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        """Emergency stop: kills motors and centers steering."""
        print("CMD: Stop")
        self._send_command(5)

    def get_distances(self):
        """Returns the latest sensor readings as a tuple (S1, S2)."""
        return (self.dist_sensor1, self.dist_sensor2)

    def close(self):
        """Clean shutdown of the controller."""
        self.running = False
        if hasattr(self, 'ser') and self.ser.is_open:
            self.stop()
            self.ser.close()
            print("System: Connection closed.")

# --------------------Main Execution Loop--------------------
if __name__ == "__main__":
    # Initialize using the COM9 port for Windows
    car = MegaPiController(port='COM9')

    try:
        print("\nStarting Intelligent Navigation. Press Ctrl+C to stop.")
        
        # Initial action
        car.move_forward(speed=120)

        while True:
            # Update sensor values from the background thread
            d1, d2 = car.get_distances()
            
            # Print status on a single line (overwriting)
            print(f"   [Status] Front: {d1}cm | Side: {d2}cm    ", end='\r')
            
            # Obstacle avoidance logic
            if d1 < 30:
                print(f"\n⚠️  Obstacle at {d1}cm! Stopping.")
                car.stop()
                break
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nUser interruption.")
    finally:
        car.close()