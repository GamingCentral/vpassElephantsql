import tkinter as tk

class Menu(tk.Tk):
    def __init__ (self,admin,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.minsize(400,400)
        self.title("Menu")
        self.admin = admin
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1),weight=1)
        
        width=400
        height=400
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
 
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.title_label = tk.Label(self, text="Select an Option", font=("courier new", 45, "bold"), fg="#426ae3", bg="#141414")
        self.title_label.pack(pady=20)
         