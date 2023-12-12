import tkinter as tk
from loginFrame import Login
from menuFrame import Menu
import connectionpool as cp

class mainApp(tk.Tk): #the mainApp is a chlid class of tk.Tk window
    def __init__(self):
        super().__init__() #call constructor of tk.Tk parent class
        self.frameDict={} #contains the dict of frames included
        self.container=tk.Frame(self) #is a window container
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.pool=None

        # Set the width and height of the window based on a fraction of the screen size
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        # Calculate the x and y coordinates to center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the geometry of the window
        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.container.pack(fill="both",expand=True) #now pack the window first

        self.databaseurl_label = tk.Label(self, text="Database URL", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.databaseurl_label.pack()
        self.databaseurl_entry = tk.Entry(self, width=82, font=("Helvetica",11), bg="white", fg="#141414")
        self.databaseurl_entry.pack(pady=5)

        self.submit_button = tk.Button(self, width=20, command=self.submit_press, text="Submit",font=("courier new bold",15),bg="#426ae3",fg="black")
        self.submit_button.pack(pady=30)
        #self.submit_button.grid(row=4, pady=(30, 0), column=1)

        self.error_label = tk.Label(self, text=None, font=("bookman old style", 12), fg="red",bg='#141414')
        self.error_label.pack()

        #self.show_frame("Login") 

    def submit_press(self):
        self.dburl= self.databaseurl_entry.get()
        if self.dburl=="":
            self.update_error_label("Enter the database url")
        else:
            try:
                self.pool=cp.poolcreate(self.dburl) #pool object
                self.menuFrame=Menu(self.container, self.switchFrames, self.pool)
                self.loginFrame=Login(self.container, self.switchFrames, self.pool, self.menuFrame)
                self.frameDict["Login"]=self.loginFrame
                self.frameDict["Menu"]=self.menuFrame
                #pool should be active
                self.connection = self.pool.get_connection()
                if isinstance(self.connection) is not str:
                    self.show_frame("Login")
                else:
                    self.update_error_label("Fetching connection failed recheck data base url")
            except Exception as e:
                self.update_error_label(e)

    def switchFrames(self, frameName):
        for frame_key in self.frameDict:
            self.frameDict[frame_key].pack_forget()

        # Show the selected frame
        selected_frame = self.frameDict[frameName]
        selected_frame.pack(fill="both", expand=True)

        # Update the window title
        self.title(frameName)

    def show_frame(self,frameName):
        self.frameNeeded=self.frameDict[frameName]
        self.frameNeeded.pack(fill="both", expand=True)
        self.title(frameName)

    def update_error_label(self,message):
        self.error_label.config(text=message)

    def on_closing(self):
        try:
            self.pool.close_pool()  
            print("all connections are closed")
            self.destroy()
        except Exception as e:
            print("Close call was not success")
            self.destroy()

    def menuFrameUpdater(self,admin):
        self.menuFrame.update_admin_info(admin)


if __name__=="__main__":
    app=mainApp()
    app.protocol("WM_DELETE_WINDOW",app.on_closing)
    app.mainloop()
