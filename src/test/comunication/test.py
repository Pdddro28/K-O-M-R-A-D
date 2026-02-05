import serial 

megapi = serial.Serial("COM3", 115200)

# Header o cabezal
# 0xAA 0x55
HEADER = 0xAA

def send_comand(type,action,value,value2):
    msg = bytearray([HEADER,type,action,value,value2])
    megapi.write(msg)

    