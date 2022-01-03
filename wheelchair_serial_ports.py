#Import serial module.
import serial

# Set up serialPorts.
serialPortSTM32 = serial.Serial(port="/dev/ttyACM0", baudrate=9600,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialPortGPRS = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)