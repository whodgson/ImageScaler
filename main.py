import os, sys
import os.path
import string

import Tkinter
import tkMessageBox
import tkFileDialog 
from Tkinter import *

class ImageScaler(Tkinter.Tk):
    def __init__(self,parent):
        #Call Super's Constructor
        Tkinter.Tk.__init__(self,parent)
        #Store Reference To Parent
        self.parent = parent
        #Initialize GUI
        self.initializeWindow()
        #Initialize Variables
        self.fileSelected = False
        
    def initializeWindow(self):
        #Create Grid Layout Manager
        self.grid() 
        #Create Title Label
        self.titleLabel = Tkinter.Label(self,anchor="c",text="Image Scaler",fg="white",bg="blue")
        self.titleLabel.grid(column=0,row=0,columnspan=3,sticky="ew")
        #Create Open Button
        self.openButton = Tkinter.Button(self,text=u"Open Image",command=self.onOpenButtonClick)
        self.openButton.grid(column=0,row=1,columnspan=1,sticky="ew") 
        #Create Open label
        self.openVar   = Tkinter.StringVar()
        self.openVar.set("No File Selected")
        self.openLabel = Tkinter.Label(self,textvariable=self.openVar,anchor="c",bg="gray")
        self.openLabel.grid(column=1,row=1,columnspan=2,sticky="ew")
        #Create Configure Label
        self.configureLabel = Tkinter.Label(self,anchor="c",text="Configure",fg="white",bg="blue")
        self.configureLabel.grid(column=0,row=2,columnspan=3,sticky="ew")
        #Create Scale Label
        self.scaleLabel = Tkinter.Label(self,anchor="c",text="Scale Factor")
        self.scaleLabel.grid(column=0,row=3,columnspan=1,sticky="ew")
        #Create Scale Entry
        self.scaleList = [25,50,75]
        self.scaleVar  = Tkinter.IntVar()
        self.scaleVar.set(50)
        self.scaleMenu = Tkinter.OptionMenu(self,self.scaleVar,*self.scaleList)
        self.scaleMenu.config(width=20)
        self.scaleMenu.grid(column=1,row=3,stick="ew")
        #Create Scale Button
        self.scaleButton = Tkinter.Button(self,text=u"Scale Image",command=self.onScaleButtonClick)
        self.scaleButton.grid(column=2,row=3,columnspan=1,sticky="ew")
        
        #Allow Column To Resize
        self.grid_columnconfigure(0,weight=1)
        #Disallow H Resize, Disallow V Resize
        self.resizable(False,False)
    
    def onOpenButtonClick(self):
        #Open File Dialog And Get File Directory
        imageTypes = [("Image files",("*.png","*.jpg","*.jpeg","*.gif")), ("All files", "*")]
        fileDialog = tkFileDialog.Open(self, filetypes = imageTypes)
        fileName = fileDialog.show()
        if fileName != '':
            if fileName.lower().endswith((".png",".jpg",".jpeg",".gif")):
                self.openVar.set(fileName)
                self.fileSelected = True
            else:
                self.showError("Invalid Filetype!")
                self.fileSelected = False
        else:
            self.openVar.set("No File Selected")
            self.fileSelected = False
            
    def onScaleButtonClick(self):
        if(self.fileSelected):
            print "Working"
        else:
            self.showError("No File Selected!")
        self.fileSelected = False
        
    def showError(self, message):
        tkMessageBox.showinfo("Error",message)
        
if __name__ == "__main__":
    app = ImageScaler(None)
    app.title("Image Scaler")
    app.mainloop()