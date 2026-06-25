import serial
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def main():
    app = tk.Tk()

    def changeEvent(*args):
        r = int(rSlider.get())
        g = int(gSlider.get())
        b = int(bSlider.get())
        cPreview.configure(bg='#%02x%02x%02x' % (r, int(g),int(b)))

        if isAuto.get():
            applyChanges()

    def initSerial(port):
        global ser
        ser = serial.Serial(port,9600)

    def applyChanges():
        r = int(rSlider.get())
        g = int(gSlider.get())
        b = int(bSlider.get())
        br = int(brSlider.get())
        data = f"{r} {g} {b} {br}\r\n"
        ser.write(data.encode())

    cFrame = tk.Frame(app)
    cFrame.pack(side="left",expand=True,fill="both")

    conFrame = tk.Frame(cFrame)
    conFrame.pack(expand=True,fill="x")
    
    tk.Label(conFrame,text="Select serial device:").pack(side="left")
    ports = [i.device for i in serial.tools.list_ports.comports(include_links=True)]
    portChooser = ttk.Combobox(conFrame,values=ports)
    portChooser.pack(side="left")

    tk.Button(conFrame,text="Initilaize",command=lambda: initSerial(portChooser.get())).pack(side="left")

    tk.Label(cFrame,text="Red").pack()
    rSlider = tk.Scale(cFrame,from_=0,to=255,orient="horizontal",command=changeEvent)
    rSlider.pack(fill="x",expand=True)
    
    tk.Label(cFrame,text="Green").pack()
    gSlider = tk.Scale(cFrame,from_=0,to=255,orient="horizontal",command=changeEvent)
    gSlider.pack(fill="x",expand=True)

    tk.Label(cFrame,text="Blue").pack()
    bSlider = tk.Scale(cFrame,from_=0,to=255,orient="horizontal",command=changeEvent)
    bSlider.pack(fill="x",expand=True)

    cPreview = tk.Canvas(cFrame,bg="black")
    cPreview.pack(expand=True,fill="x")
    
    bFrame = tk.Frame(app)
    bFrame.pack(side="left",expand=False,fill="y")

    tk.Label(bFrame,text="Brightness").pack()
    brSlider = tk.Scale(bFrame,from_=255,to=0,orient="vertical",digits=True,command=changeEvent)
    brSlider.pack(fill="y",expand=True)
    
    applyFrame = tk.Frame(cFrame)
    applyFrame.pack(fill="x",expand=True)
    isAuto=tk.IntVar()
    tk.Button(applyFrame,text="Apply",command=applyChanges).pack(side="right")
    autoApplyCheck=tk.Checkbutton(applyFrame,text="Auto apply",variable=isAuto)
    autoApplyCheck.pack(side="right")

    app.mainloop()

if __name__ == "__main__":
    main()