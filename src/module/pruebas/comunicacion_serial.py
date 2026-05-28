import serial
import time
import threading

# ====================================================
# MEGAPI SERIAL CONTROLLER CLASS
# ====================================================
class MegaPiController:
    """
    Controller class for MegaPi robot.
    Handles movement commands and asynchronous sensor data retrieval.
    """

    def __init__(self, port='COM9', baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            time.sleep(2)  
            print(f"✅ System: Connected to MegaPi on {port}")
            
            self.dist_sensor1 = 400
            self.dist_sensor2 = 400
            
            self.running = True
            self.reader_thread = threading.Thread(target=self._read_telemetry, daemon=True)
            self.reader_thread.start()

        except Exception as e:
            print(f"❌ Critical Error: Could not connect to {port}. {e}")
            exit()

    def _read_telemetry(self):
        """Asynchronous background loop to parse incoming packet buffers."""
        while self.running:
            try:
                if self.ser.in_waiting >= 1:
                    header = self.ser.read(1)
                    
                    if header == b'\xaa':
                        if self.ser.in_waiting >= 4:
                            payload = self.ser.read(4)
                            self.dist_sensor1 = payload[0]
                            self.dist_sensor2 = payload[1]
                    else:
                        line = self.ser.readline().decode('ascii', errors='ignore').strip()
                        if line:
                            print(f"   [MegaPi Debug]: {line}")
            except Exception:
                pass
            time.sleep(0.01)

    def _send_command(self, action, v1=0, v2=0):
        """Constructs and transmits the 5-byte serial protocol packet."""
        header = 0xFF
        msg_type = 0x01
        package = bytearray([header, msg_type, action, v1, v2])
        self.ser.write(package)

    def move_forward(self, speed, duration=None):
        print(f"CMD: Forward | Speed: {speed}")
        self._send_command(1, v1=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def move_backward(self, speed, duration=None):
        print(f"CMD: Backward | Speed: {speed}")
        self._send_command(2, v1=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, angle, speed, duration=None):
        print(f"CMD: Turn Left | Angle: {angle} | Speed: {speed}")
        self._send_command(3, v1=angle, v2=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_right(self, angle, speed, duration=None):
        print(f"CMD: Turn Right | Angle: {angle} | Speed: {speed}")
        self._send_command(4, v1=angle, v2=speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        print("CMD: Stop")
        self._send_command(5)

    def get_distances(self):
        return (self.dist_sensor1, self.dist_sensor2)

    def close(self):
        self.running = False
        if hasattr(self, 'ser') and self.ser.is_open:
            self.stop()
            self.ser.close()
            print("System: Connection closed.")

# ====================================================
# ENTRY POINT & INTEGRATION TEST
# ====================================================
if __name__ == "__main__":
    car = MegaPiController(port='COM9')

    try:
        print("\nStarting Intelligent Navigation. Press Ctrl+C to stop.")
        car.move_forward(speed=120)

        while True:
            d1, d2 = car.get_distances()
            print(f"   [Status] Front: {d1}cm | Side: {d2}cm    ", end='\r')
            
            if d1 < 30:
                print(f"\n⚠️ Obstacle at {d1}cm! Stopping.")
                car.stop()
                break
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nUser interruption.")
    finally:
        car.close()
