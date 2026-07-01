import serial
import json
import time

ser = serial.Serial("/dev/ttyUSB0",9600)
time.sleep(5)
input("Start? ")
def send(data): ser.write((data +"\n").encode())

with open("animation.json","r") as f:
    data = json.load(f)



def pixelToNibleArray(text):
    if len(text) % 2 != 0:
        text += "0"
    result = bytearray()
    for i in range(0, len(text), 2):
        low_char = text[i]
        high_char = text[i + 1]
        low = ord(low_char) - ord('0')
        high = ord(high_char) - ord('0')
        packed = (high << 4) | low
        result.append(packed)
    return result


send("gd")
size = ser.read_until().decode('utf-8').strip()
print(size)
X = int(size.split("x")[0])
Y = int(size.split("x")[1])
print(X,Y)
input("Continue? ")
send("sb 16")
input("Continue? ")
send("sm 2")
input("Continue? ")
send(f"as {len(data['frames'])}")
input("Continue? ")

for i in range(len(data["frames"])):
    currentBuffer = ""
    for c in data["frames"][i]:
        currentBuffer+=c
    
    print(currentBuffer)
    send(f"af {i}")
    ser.write(pixelToNibleArray(currentBuffer))
    ser.write(b'\n')
    input("Continue? ")


send("ap")

while True:
    send(input("Type in command:"))
