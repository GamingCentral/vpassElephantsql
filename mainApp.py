import tkinter as tk
from loginFrame import Login
from menuFrame import Menu

class mainApp(tk.Tk): #the mainApp is a chlid class of tk.Tk window
    def __init__(self):
        super().__init__() #call constructor of tk.Tk parent class
        self.frameDict={} #contains the dict of frames included
        self.container=tk.Frame(self) #is a window container
        self.container.pack(fill="both",expand=True) #now pack the window first

        self.loginFrame=Login(self.container, self.switchFrames)
        self.menuFrame=Menu(self.container, self.switchFrames)

        self.frameDict["Login"]=self.loginFrame
        self.menuFrame["Menu"]=self.menuFrame
        self.show_frame("Login")

    def switchFrames(self, frameName):
        #first delete the frame if that was opened before
        frameToDelete:tk.Frame=self.frameDict[frameName]
        frameToDelete.pack_forget() #forget any previous instances
        frameToRecreate:tk.Frame=self.frameDict[frameName]
        frameToRecreate.pack(fill="both",expand=True) #make new instance for the same window
        self.title(frameName) #should include?