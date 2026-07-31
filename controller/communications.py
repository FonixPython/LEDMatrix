import serial
import serial.tools.list_ports
import time
import threading
import queue


BAUD_RATE = 9600


class ControllerAPI():
    def __init__(self):
        self.serialSocket = None
        self.xDimension = 8
        self.yDimension = 8
        self.serialQueue = queue.Queue()
        self.senderThread = threading.Thread(
            target=self.queueSendingTask,
            daemon=True
        )
        self.serialLock = threading.Lock()
        self.senderThread.start()
        self._initValues()
    def _initValues(self):
        self.brightness = 32
        self.speed = 100
        self.mode = "Single"
        self.pattern = "Rainbow"
        self.text = "Hello_world"
        self.textColorMode = "Solid"
        self.effectColor = [255, 128, 0]
        self.isPlaying = False
    def queueSendingTask(self):
        while True:
            data = self.serialQueue.get()
            if self.serialSocket:
                if type(data) == type("a"):
                    self._send(data)
                    if not "af" in data:
                        self.serialSocket.read_until()
                    else:
                        time.sleep(1)
                else:
                    self.serialSocket.write(data)
                    time.sleep(1)
                print(f"Sent: '{data}'")
    def getDevices(self):
        portList = serial.tools.list_ports.comports()
        portsObject = [{"name":i.name,"device":i.device,"product":i.product} for i in portList]
        return portsObject
    def getStatus(self):
        return {
            "connected": self.serialSocket != None,
            "dimensions":{
                "x":self.xDimension,
                "y":self.yDimension
            }
        }
    def connect(self,comport:str):
        self.serialSocket = serial.Serial(comport,BAUD_RATE,timeout=5)
        self.serialSocket.read_until()
        self._send("gd")
        response = self.serialSocket.read_until().decode('utf-8').strip()
        self.xDimension = int(response.split("x")[0])
        self.yDimension = int(response.split("x")[1])
        self._initValues()
        self.setBrightness(self.brightness)
        self.setSpeed(self.speed)
        self.setMode(self.mode)
        self.setPattern(self.pattern)
        self.setText(self.text)
        self.setTextColor(self.textColorMode)
        self.setColor(self.effectColor[0],self.effectColor[1],self.effectColor[2])
    def disconnect(self):
        if self.serialSocket: self.serialSocket.close()
        self.serialSocket = None
        self.xDimension = None
        self.yDimension = None
    def checkConnection(self):
        if not self.serialSocket: raise ConnectionError("Device not connected!")
    def _send(self,data):
        self.checkConnection()
        with self.serialLock:
            self.serialSocket.write((data+"\n").encode())
    def setMode(self,mode:str):
        modeIndex = 0
        match mode:
            case "Single": modeIndex = 0
            case "Pattern": modeIndex = 1
            case "Animation": modeIndex = 2
            case "Text": modeIndex = 3
            case _: raise ValueError("Invalid mode!")
        self.serialQueue.put(f"sm {modeIndex}")
        self.mode = mode
    def setPattern(self,mode:str):
        modeIndex = 0
        match mode:
            case "Rainbow":modeIndex = 0
            case "Checker":modeIndex = 1
            case "Scanner":modeIndex = 2
            case "Pulse": modeIndex = 3
            case "Snake": modeIndex = 4
            case "Rainbow fill": modeIndex = 5
            case _: raise ValueError("Invalid pattern!")
        self.serialQueue.put(f"em {modeIndex}")
        self.pattern = mode
    def setColor(self,r:int,g:int,b:int):
        if r not in range(256) or g not in range(256) or b not in range(256): raise ValueError("A channel is out of the accepted range of 0-255!")
        self.serialQueue.put(f"ec {r} {g} {b}")
        self.effectColor = [r,g,b]
    def setBrightness(self,value:int):
        if not value in range(256): raise ValueError("Brightness value is out of range!")
        self.serialQueue.put(f"sb {value}")
        self.brightness = value
    def setSpeed(self,value:int):
        if value < 0: value = value * -1
        self.serialQueue.put(f"ss {value}")
        self.speed = value
    def fillWithColor(self):
        self.serialQueue.put("f")
    def setPixel(self,x:int,y:int,r:int,g:int,b:int):
        if r not in range(256) or g not in range(256) or b not in range(256): raise ValueError("A channel is out of the accepted range of 0-255!")
        if x not in range(self.xDimension) or y not in range(self.yDimension): raise ValueError("Invalid pixel address!")
        self.serialQueue.put(f"o {x} {y} {r} {g} {b}")
    def setText(self,text:str):
        if len(text) >= 60: raise ValueError("Text too long!")
        text = text.replace(" ","_")
        self.serialQueue.put(f"ts {text}")
        self.text = text
    def setTextColor(self,mode:str):
        modeIndex = 0
        match mode:
            case "Solid": modeIndex = 0
            case "Rainbow": modeIndex = 1
            case _: raise ValueError("Invalid color mode!")
        self.serialQueue.put(f"tc {modeIndex}")
        self.textColorMode = mode
    def play(self):
        self.isPlaying = not self.isPlaying
        self.serialQueue.put(f"ap")

    def _coordinatesToAddress(self,x,y):
        x+=1;y+=1
        address = self.xDimension*y
        if y%2==0: address -= x
        else: address-=self.xDimension-x+1
        return address
    
    def _matrixToOneDimensionArray(self,matrix):
        oneDArray = [0 for i in range(self.xDimension*self.yDimension)]
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                oneDArray[self._coordinatesToAddress(x,y)] = str(matrix[y][x])
        return oneDArray
    def _pixelToNibleArray(self,text):
        if len(text) % 2 != 0:text += "0"
        result = bytearray()
        for i in range(0, len(text), 2):
            low_char = text[i]
            high_char = text[i + 1]
            low = ord(low_char) - ord('0')
            high = ord(high_char) - ord('0')
            packed = (high << 4) | low
            result.append(packed)
        return result

    def sendAnimation(self,animationObject):
        if len(animationObject["frames"][0]) != self.yDimension or len(animationObject["frames"][0][0]) != self.xDimension:
            raise ValueError("Invalid size for animation frames!")
        for i,frame in enumerate(animationObject["frames"]):
            oneD = self._matrixToOneDimensionArray(frame)
            bytearray = self._pixelToNibleArray("".join(oneD))
            self.serialQueue.put(f"af {i}")
            self.serialQueue.put(bytearray)
            self.serialQueue.put(b'\n')

        for i,color in enumerate(animationObject["palette"]):
            rgb = color.getRgb()
            self.serialQueue.put(f"ac {i} {rgb[0]} {rgb[1]} {rgb[2]}")
        self.serialQueue.put(f"as {len(animationObject["frames"])}")

if __name__ == "__main__":
    controller = ControllerAPI()
    controller.getDevices()