import tkinter as tk

class Menu(tk.Tk):
    def __init__(self, s, p):
        super().__init__()
        self.switchingFunction=s
        self.admin = None
        self.pool = p

        tk.Label(self,text="Menu Window").pack()
        tk.Button(self,text="Logout",command=self.logout).pack()
        tk.Label(self, text=self.admin).pack()
    
    def update_admin_info(self,admin):
        self.admin = admin

    def logout(self):
        #if logout is pressed
        self.switchingFunction("Login")