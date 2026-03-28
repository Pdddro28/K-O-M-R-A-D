import serial
import time
import threading
import pandas as pd
import random

class MegaPiController:
    """
    Controller class for MegaPi robot.
    Handles movement, telemetry, and data logging for ML training.
    """

    # Action Constants
    ACTION_LEFT = 0
    ACTION_FORWARD = 1
    ACTION_RIGHT = 2

    def __init__(self, port='COM5', baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            time.sleep(2) 
            print(f"✅ System: Connected to MegaPi on {port}")
            
            # Distance variables (3 sensors: Front, Left, Right)
            self.dist_front = 400
            self.dist_left = 400
            self.dist_right = 400
            
            # Data Logging List (For Pandas)
            self.data_log = []
            self.log_index = 0
            
            # Thread setup
            self.running = True
            self.reader_thread = threading.Thread(target=self._read_telemetry, daemon=True)
            self.reader_thread.start()

        except Exception as e:
            print(f"❌ Critical Error: Could not connect to {port}. {e}")
            exit()

    def _read_telemetry(self):
        """Background loop to parse incoming sensor data (3 sensors + 2 padding)."""
        while self.running:
            try:
                if self.ser.in_waiting >= 1:
                    header = self.ser.read(1)
                    
                    if header == b'\xaa':
                        # Read 5 bytes: [Front, Left, Right, Padding, Padding]
                        if self.ser.in_waiting >= 5:
                            payload = self.ser.read(5)
                            self.dist_front = payload[0]
                            self.dist_left = payload[1]
                            self.dist_right = payload[2]
                    else:
                        line = self.ser.readline().decode('ascii', errors='ignore').strip()
                        if line:
                            print(f"   [MegaPi Debug]: {line}")
            except Exception:
                pass
            time.sleep(0.01)

    def _send_command(self, action, v1=0, v2=0):
        header = 0xFF
        msg_type = 0x01
        package = bytearray([header, msg_type, action, v1, v2])
        self.ser.write(package)

    def obtenerarea_frontal(self):
        return random.randint(0, 100000)

    def obtenerarea_izquierda(self):
        return random.randint(0, 100000)

    def obtenerarea_derecha(self):
        return random.randint(0, 100000)

    def log_step(self, action_code):
        d_front, d_left, d_right = self.get_distances()
        area_front = self.obtenerarea_frontal()
        area_left = self.obtenerarea_izquierda()
        area_right = self.obtenerarea_derecha()
        
        self.data_log.append({
            'index': self.log_index,
            'dist_front_cm': d_front,
            'dist_left_cm': d_left,
            'dist_right_cm': d_right,
            'black_front_area': area_front,
            'black_left_area': area_left,
            'black_right_area': area_right,
            'action_taken': action_code
        })
        
        self.log_index += 1

    def move_forward(self, speed, duration=None, log=True):
        print(f"CMD: Forward | Speed: {speed}")
        self._send_command(1, v1=speed)
        if log: self.log_step(self.ACTION_FORWARD)
        if duration:
            time.sleep(duration)
            self.stop()

    def move_backward(self, speed, duration=None, log=True):
        print(f"CMD: Backward | Speed: {speed}")
        self._send_command(2, v1=speed)
        if log: self.log_step(self.ACTION_FORWARD)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, angle, speed, duration=None, log=True):
        print(f"CMD: Turn Left | Angle: {angle} | Speed: {speed}")
        self._send_command(3, v1=angle, v2=speed)
        if log: self.log_step(self.ACTION_LEFT)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_right(self, angle, speed, duration=None, log=True):
        print(f"CMD: Turn Right | Angle: {angle} | Speed: {speed}")
        self._send_command(4, v1=angle, v2=speed)
        if log: self.log_step(self.ACTION_RIGHT)
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self, log=True):
        print("CMD: Stop")
        self._send_command(5)
        if log: self.log_step(self.ACTION_FORWARD)

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


# --------------------Main Execution Loop (Solo para testing)--------------------
if __name__ == "__main__":
    car = MegaPiController(port='COM5')

    try:
        print("\n🤖 Starting Data Collection for AI Training...")
        car.move_forward(speed=100, log=True)

        while True:
            d_front, d_left, d_right = car.get_distances()
            print(f"   [Sensors] F:{d_front:3}cm L:{d_left:3}cm R:{d_right:3}cm  ", end='\r')
            
            if d_front < 25:
                car.stop(log=True)
                time.sleep(0.5)
                if d_left > d_right: 
                    car.turn_left(angle=90, speed=80, duration=0.5, log=True)
                else:
                    car.turn_right(angle=90, speed=80, duration=0.5, log=True)
                car.move_forward(speed=100, log=True)
            elif d_left < 15:
                car.turn_right(angle=10, speed=80, duration=0.2, log=True)
                car.move_forward(speed=100, log=True)
            elif d_right < 15:
                car.turn_left(angle=10, speed=80, duration=0.2, log=True)
                car.move_forward(speed=100, log=True)
            else:
                car.log_step(car.ACTION_FORWARD)
            
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\n⛔ User interruption detected.")
    finally:
        car.save_data_to_csv('training_data.csv')
        car.close()