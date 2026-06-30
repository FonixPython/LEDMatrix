import serial

ser = serial.Serial("/dev/ttyUSB0",9600)

while True:
    data = input("Type in command:")
    ser.write(data.encode())