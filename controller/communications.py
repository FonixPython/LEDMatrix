import serial
import serial.tools.list_ports

BAUD_RATE = 9600


class ControllerAPI():
    def __init__(self):
        self.serialSocket = None
        self.xDimension = None
        self.yDimension = None
    def getDevices(self):
        portList = serial.tools.list_ports()
    def connect(self,comport:str):
        self.serialSocket = serial.Serial(comport,BAUD_RATE)
        self._send("gd")
        response = self.serialSocket.read_until().decode('utf-8').strip()
        self.xDimension = int(size.split("x")[0])
        self.yDimension = int(size.split("x")[1])
    def disconnect(self):
        if self.serialSocket: self.serialSocket.close()
        self.serialSocket = None
        self.xDimension = None
        self.yDimension = None
    def checkConnection(self):
        if not self.serialSocket: raise ConnectionError("Device not connected!")
    def _send(self,data):
        self.checkConnection()
        self.serialSocket.write((data + "\n").encode())
    def setMode(self,mode:str):
        modeIndex = 0
        match mode:
            case "Single": modeIndex = 0
            case "Effect": modeIndex = 1
            case "Animation": modeIndex = 2
            case "Text": modeIndex = 3
            case _: ValueError("Invalid mode!")
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
        self._send(f"em {modeIndex}")
    def setColor(self,r:int,g:int,b:int):
        if not r in range(256) or g in range(256) or b in range(256): raise ValueError("A channel is out of the accepted range of 0-255!")
        self._send(f"ec {r} {g} {b}")
    def setBrightness(self,value:int):
        if not value in range(256): raise ValueError("Brightness value is out of range!")
        self._send(f"sb {value}")
    def setSpeed(self,value:int):
        if value < 0: value = value * -1
        self._send(f"ss {value}")
    def fillWithColor(self):
        self._send("f")
    def setPixel(self,x:int,y:int,r:int,g:int,b:int):
        if not r in range(256) or g in range(256) or b in range(256): raise ValueError("A channel is out of the accepted range of 0-255!")
        if not x in range(self.xDimension) or y in range(self.yDimension): raise ValueError("Invalid pixel address!")
        self._send(f"o {x} {y} {r} {g} {b}")
    def setText(self,text:str):
        if len(text) <= 60: raise ValueError("Text too long!")
        self._send(f"ts {text}")
    def setTextColor(self,mode:str):
        modeIndex = 0
        match mode:
            case "Solid": modeIndex = 0
            case "Rainbow": modeIndex = 1
            case _: raise ValueError("Invalid color mode!")
        self._send("tc")
