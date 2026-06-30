import serial
import threading

ser = serial.Serial("/dev/ttyUSB1",9600)

def read():
    data = ser.read_until() # Blocks!
    print(data.decode(), end='')
threading.Thread(target=read).start()

while True:
    data = input("Type in command:")
    ser.write(data.encode())