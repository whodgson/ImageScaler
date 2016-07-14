import os, sys
import os.path
import string

import Tkinter
import tkMessageBox
import tkFileDialog 

from Tkinter import *
from PIL     import Image

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
        #Create Info Label 1
        self.infoVar1   = Tkinter.StringVar()
        self.infoVar1.set("")
        self.infoLabel1 = Tkinter.Label(self,textvariable=self.infoVar1,anchor="c",bg="gray")
        self.infoLabel1.grid(column=1,row=2,columnspan=2,sticky="ew")
        #Create Info Label 2
        self.infoVar2   = Tkinter.StringVar()
        self.infoVar2.set("")
        self.infoLabel2 = Tkinter.Label(self,textvariable=self.infoVar2,anchor="c",bg="gray")
        self.infoLabel2.grid(column=1,row=3,columnspan=2,sticky="ew")
        #Create Info Label 3
        self.infoVar3   = Tkinter.StringVar()
        self.infoVar3.set("")
        self.infoLabel3 = Tkinter.Label(self,textvariable=self.infoVar3,anchor="c",bg="gray")
        self.infoLabel3.grid(column=1,row=4,columnspan=2,sticky="ew")
        #Create Configure Label
        self.configureLabel = Tkinter.Label(self,anchor="c",text="Configure",fg="white",bg="blue")
        self.configureLabel.grid(column=0,row=5,columnspan=3,sticky="ew")
        #Create Scale Label
        self.scaleLabel = Tkinter.Label(self,anchor="c",text="Scale Factor")
        self.scaleLabel.grid(column=0,row=6,columnspan=1,sticky="ew")
        #Create Scale Entry
        self.scaleList = [5,10,15,20,25,50,75]
        self.scaleVar  = Tkinter.IntVar()
        self.scaleVar.set(50)
        self.scaleMenu = Tkinter.OptionMenu(self,self.scaleVar,*self.scaleList)
        self.scaleMenu.config(width=20)
        self.scaleMenu.grid(column=1,row=6,stick="ew")
        #Create Scale Button
        self.scaleButton = Tkinter.Button(self,text=u"Scale Image",command=self.onScaleButtonClick)
        self.scaleButton.grid(column=2,row=6,columnspan=1,sticky="ew")
        #Allow Column To Resize
        self.grid_columnconfigure(0,weight=1)
        #Disallow H Resize, Disallow V Resize
        self.resizable(False,False)
    
    def onOpenButtonClick(self):
        #Open File Dialog And Get File Directory
        imageTypes = [("Image files",("*.png","*.jpg","*.jpeg","*.gif")), ("All files", "*")]
        fileDialog = tkFileDialog.Open(self, filetypes = imageTypes)
        fileName = fileDialog.show()
        #Check If Any File Selected
        if fileName != '':
            #Check If Image File Selected
            if fileName.lower().endswith((".png",".jpg",".jpeg",".gif")):
                #Store File Directory
                self.openVar.set(fileName)
                self.setFileInfo()
                self.fileSelected = True
            else:
                self.showError("Invalid Filetype!")
                self.fileSelected = False
                self.clearFileInfo()
        else:
            #Clear File Directory
            self.openVar.set("No File Selected")
            self.fileSelected = False
            #Clear File Info
            self.clearFileInfo()
            
    def onScaleButtonClick(self):
        #Check If Valid Image Directory Selected
        if(self.fileSelected):
            #Confirm File Overwrite
            choice = tkMessageBox.askquestion("Save","Overwrite Existing Image With Scaled Version?",icon="warning")
            if choice == "yes":
                #Rescale File
                image = self.scaleFile()
                #Check Image Was Scaled Successfully
                if image != None:
                    #Overwrite Selected File With Existing File
                    self.saveFile(image)
                else:
                    self.showError("Error During Image Scale!")
                    return None
            else:
                #Cancel Scale Operation
                self.showInfo("Scale Operation Cancelled!")
                return None
        else:
            self.showError("No File Selected!")
            
        #Clear File Directory
        self.fileSelected = False
        #Reset File Infov
        self.openVar.set("No File Selected")
        self.clearFileInfo()
     
    def scaleFile(self):
        #Get File And Size Information
        image = Image.open(self.openVar.get())
        size  = image.size
        sizeX = size[0]
        sizeY = size[1]
        #Get Scale Factor And New Image Dimensions
        scaleFactor = self.scaleVar.get()
        newSizeX    = sizeX*(scaleFactor*0.01)
        newSizeY    = sizeY*(scaleFactor*0.01)
        newSize     = (newSizeX,newSizeY)
        #Check New Size Is Not Impossible
        if newSizeX < 1 or newSizeY < 1:
            self.showError("Cannot Scale That Small! \n(Width or Height Below One Pixel)")
            return None
        #Scale Image
        image.thumbnail(newSize)
        #Return Scaled Image
        return image
        
    def saveFile(self, image):
        try:
            image.save(self.openVar.get())
            self.showInfo("Saved Image Successfully!")
        except IOError:
            self.showError("Error During Image Save!")
        
    def setFileInfo(self):
        image = Image.open(self.openVar.get())
        self.infoVar1.set(image.format)
        self.infoVar2.set(image.size)
        self.infoVar3.set(image.mode)
    
    def clearFileInfo(self):
        self.infoVar1.set("")
        self.infoVar2.set("")
        self.infoVar3.set("")
        
    def showError(self, message):
        tkMessageBox.showerror("Error",message)
        
    def showInfo(self, message):
        tkMessageBox.showinfo("Info",message)
        
if __name__ == "__main__":
    app = ImageScaler(None)
    app.title("Image Scaler")
    app.mainloop()