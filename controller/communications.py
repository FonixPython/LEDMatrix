import serial
import serial.tools.list_ports
import time
import threading
import queue


BAUD_RATE = 9600


class ControllerAPI():
    def __init__(self):
        self.serialSocket = None
        self.xDimension = None
        self.yDimension = None
        self.brightness = 32
        self.speed = 100
        self.mode = "Single"
        self.pattern = "Rainbow"
        self.text = "Hello_world"
        self.textColorMode = "Solid"
        self.effectColor = [255, 128, 0]
        self.serialQueue = queue.Queue()
        self.senderThread = threading.Thread(
            target=self.queueSendingTask,
            daemon=True
        )
        self.serialLock = threading.Lock()
        self.senderThread.start()
    def queueSendingTask(self):
        while True:
            data = self.serialQueue.get()
            if self.serialSocket:
                self._send(data)
                print(f"Sent: '{data}'")
                self.serialSocket.read_until()
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


if __name__ == "__main__":
    controller = ControllerAPI()
    controller.getDevices()