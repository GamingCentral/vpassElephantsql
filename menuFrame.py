import tkinter as tk

class Menu(tk.Frame):
    def __init__(self, m, s):
        super().__init__(m)
        self.switchingFunction=s

        tk.Label(self,text="Menu Window").pack()
        tk.Button(self,text="Logout",command=self.logout).pack()

    def logout(self):
        #if logout is pressed
        self.switchingFunction("Login")