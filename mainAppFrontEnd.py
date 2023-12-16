import tkinter as tk
from tkinter import ttk
'''from loginFrame import Login
from menuFrame import Men'''
import connectionpool as cp

class mainApp:
    def __init__(self,root):
        self.root:tk.Tk=root
        self.root.configure(bg='#141414')

        style = ttk.Style()
        style.configure("TFrame", background='#141414')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the width and height of the window based on a fraction of the screen size
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        # Calculate the x and y coordinates to center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.root.pack(fill="both", expand=True)

        self.root.title("Visitor Pass System")
        self.dbUrl = tk.StringVar()

        self.dbFrame = ttk.Frame(root,style='TFrame')
        self.loginFrame = ttk.Frame(root,style='TFrame')
        self.MenuFrame = ttk.Frame(root,style='TFrame')

        self.admin = 0 #default

    def dbFrameInitalizer(self):

        self.databaseurl_label = tk.Label(self.dbFrame, text="Database URL", font=("bookman old style", 15), fg="gray", bg="#141414")
        self.databaseurl_label.pack(pady=45)
        self.databaseurl_entry = tk.Entry(self.dbFrame, width=82, font=("Helvetica", 11), bg="white", fg="#141414")
        self.databaseurl_entry.pack(pady=5)

        ##############################################################################
        self.submit_button = tk.Button(self.dbFrame, width=20, command=self.submit_press_dburl, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=45)

        self.error_label = tk.Label(self.dbFrame, text=None, font=("bookman old style", 12), fg="red", bg='#141414')
        self.error_label.pack()

    def loginFrameInitializer(self):

        self.title_label = tk.Label(self.loginFrame, text="Login", font=("courier new", 45, "bold"), fg="#426ae3", bg="#141414")
        self.title_label.pack(pady=20)

        self.username_label = tk.Label(self.loginFrame, text="UserName", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.loginFrame, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.loginFrame, text="Password", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.loginFrame, width=70,font=("Helvetica",12), show="•", bg="white", fg="#141414")
        self.password_entry.pack(pady=5)

        ##########################################################################
        self.submit_button = tk.Button(self.loginFrame, width=20, command=self.submit_press_login, text="Submit",font=("courier new bold",15),bg="#426ae3",fg="black")
        self.submit_button.pack(pady=30)

        ##########################################################################
        self.back_button = tk.Button(self.loginFrame, text="Back", width=20, command=self.back_press_login, font=("courier new bold",15),bg="#426ae3",fg="black")
        self.back_button.pack(pady=50)

        self.error_label = tk.Label(self.loginFrame, text=None, font=("bookman old style", 12), fg="red",bg='#141414')
        self.error_label.pack()

    def menuFrameInitializer(self): #intialise after self.admin is fetched

        notebook = ttk.Notebook(self.MenuFrame)
        
        visitorEntry = ttk.Frame(notebook)
        visitorExit = ttk.Frame(notebook)
        signup = ttk.Frame(notebook)

        notebook.add(visitorEntry, text='Visitor Entry')
        notebook.add(visitorExit, text='visitor Exit')

        if self.admin is 1:
            notebook.add(signup, text='Sign Up/ Register')  

        backButton = tk.Button(self.MenuFrame, text='Back', command=self.back_button_menu)
        notebook.pack(pady=10)
        backButton.pack(pady=10)



'''class mainApp(tk.Tk): #the mainApp is a chlid class of tk.Tk window
    def __init__(self):
        super().__init__()
        self.frameDict = {}
        self.configure(bg='#141414')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the width and height of the window based on a fraction of the screen size
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        # Calculate the x and y coordinates to center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the geometry of the window
        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.container = tk.Frame(self, bg='#141414')
        self.container.pack(fill="both", expand=True)

        self.databaseurl_label = tk.Label(self.container, text="Database URL", font=("bookman old style", 15), fg="gray", bg="#141414")
        self.databaseurl_label.pack(pady=45)
        self.databaseurl_entry = tk.Entry(self.container, width=82, font=("Helvetica", 11), bg="white", fg="#141414")
        self.databaseurl_entry.pack(pady=5)

        self.submit_button = tk.Button(self.container, width=20, command=self.submit_press, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=45)

        self.error_label = tk.Label(self.container, text=None, font=("bookman old style", 12), fg="red", bg='#141414')
        self.error_label.pack()

    def submit_press(self):
        self.dburl= self.databaseurl_entry.get()
        if self.dburl=="":
            self.update_error_label("Enter the database url")
        else:
            try:
                self.pool=cp.poolcreate(self.dburl) #pool object
                self.menuFrame=Menu(self.switchFrames, self.pool)
                self.loginFrame=Login(self.switchFrames, self.pool, self.menuFrameUpdater)
                self.frameDict["Login"]=self.loginFrame
                self.frameDict["Menu"]=self.menuFrame
                self.frameDict["Main"]=self.container
                #pool should be active
                self.connection = self.pool.get_connection()
                if not isinstance(self.connection,str):
                    self.frameDict["Main"].pack_forget()
                    self.show_frame("Login")
                else:
                    self.update_error_label("Fetching connection failed recheck data base url")
            except Exception as e:
                self.update_error_label(e)
                print(e)

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
'''