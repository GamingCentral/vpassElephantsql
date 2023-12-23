import tkinter as tk
from tkinter import ttk
'''from loginFrame import Login
from menuFrame import Men'''
#import connectionpool as cp

class mainApp:
    def __init__(self,root):
        self.root:tk.Tk=root
        self.root.configure(bg='#141414')

        style = ttk.Style()
        style.configure("TFrame", background='#141414')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the width and height of the window based on a fraction of the screen size
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.ww = window_width

        # Calculate the x and y coordinates to center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 3

        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        #self.root.pack(fill="both", expand=True)

        self.root.title("Visitor Pass System")

        self.dbFrame = ttk.Frame(root,style='TFrame')
        self.loginFrame = ttk.Frame(root,style='TFrame')
        self.menuFrame = ttk.Frame(root,style='TFrame')

        #self.admin = 0 #default
        self.dbFrameInitalizer()
        self.loginFrameInitializer()
        self.menuFrameInitializer()

        self.frameSwitch(self.dbFrame)

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
        self.password_entry = tk.Entry(self.loginFrame, width=72,font=("Helvetica",12), show="•", bg="white", fg="#141414")
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

        self.notebook = ttk.Notebook(self.menuFrame,width=self.ww)

        style = ttk.Style()
        style.configure('TNotebook.Tab', background="#426ae3")
        style.map("TNotebook", background= [("selected", "#426ae3")])
        
        self.visitorEntry = ttk.Frame(self.notebook) #showdefault?
        self.addVisitorEntry()
        self.visitorExit = ttk.Frame(self.notebook)
        self.signup = ttk.Frame(self.notebook)

        self.notebook.add(self.visitorEntry, text='Visitor Entry')
        self.notebook.add(self.visitorExit, text='visitor Exit')  

        backButton = tk.Button(self.menuFrame, text='Back', command=self.back_button_menu, font=("courier new bold",15),bg="#426ae3",fg="black")
        self.notebook.pack(pady=10)
        backButton.pack(pady=10)

    def addVisitorEntry(self):
        self.entry_label = tk.Label(self.visitorEntry, text="Visitor Entry", font=("courier new bold", 25), fg="#426ae3", bg="#141414")
        self.entry_label.pack(pady=15)

        self.visitorNameLabel = tk.Label(self.visitorEntry, text="Name", font=("bookman old style", 10),fg="gray", bg="#141414")
        self.visitorNameLabel.pack()
        self.visitorNameEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.visitorNameEntry.pack(pady=5)

        self.visitorNumberLabel = tk.Label(self.visitorEntry, text="Phone Number", font=("bookman old style", 10),fg="gray", bg="#141414")
        self.visitorNumberLabel.pack()
        self.visitorNumberEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.visitorNumberEntry.pack(pady=5)

        self.visitorEmailLabel = tk.Label(self.visitorEntry, text="Email", font=("bookman old style", 10),fg="gray", bg="#141414")
        self.visitorEmailLabel.pack()
        self.visitorEmailEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.visitorEmailEntry.pack(pady=5)

        # to be switched with a dropdown
        self.visitorFacultyLabel = tk.Label(self.visitorEntry, text="Faculty Name", font=("bookman old style", 10),fg="gray", bg="#141414")
        self.visitorFacultyLabel.pack()
        self.visitorFacultyButton = tk.Button(self.visitorEntry, text="🠟", font=25, width=10, bg='#426ae3',command=self.dropdown)
        self.visitorFacultyButton.pack(pady=5)

        self.visitorReasonLabel = tk.Label(self.visitorEntry, text="Reason To Visit", font=("bookman old style", 10),fg="gray", bg="#141414")
        self.visitorReasonLabel.pack()
        self.visitorReasonEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.visitorReasonEntry.pack(pady=5)

        self.visitorBarcodeLabel = tk.Label(self.visitorEntry, text="Barcode", font=("bookman old style", 10),fg="gray", bg="#141414")
        self.visitorBarcodeLabel.pack()
        self.visitorBarcodeEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.visitorBarcodeEntry.pack(pady=5)

        self.submit_button = tk.Button(self.visitorEntry, width=40, command=self.submit_press_dburl, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=15)

        self.error_label = tk.Label(self.visitorEntry, text='this is error', font=("bookman old style", 15), fg="red", bg='#141414')
        self.error_label.pack()
    
    def addVisitorExit():
        print("code for exit")
    
    def menuFrameUpdater(self):
        self.notebook.add(self.signup, text='Sign Up/ Register')

    def frameSwitch(self,frame:ttk.Frame):
        try:
            self.dbFrame.pack_forget()
            self.loginFrame.pack_forget()
            self.menuFrame.pack_forget()
        except Exception as e:
            print(e)
        finally:
            frame.pack(fill="both",expand=True)

    def dbFrameSwitch(self):
        self.frameSwitch(self.dbFrame)

    def loginFrameSwitch(self):
        self.frameSwitch(self.loginFrame)

    def menuFrameSwitch(self):
        self.frameSwitch(self.menuFrame)

    def submit_press_dburl(self):
        self.loginFrameSwitch()

    def submit_press_login(self):
        #first run code for credentials and update admin
        admin=True
        if admin:
            self.menuFrameUpdater()
        self.menuFrameSwitch()

    def back_press_login(self):
        self.dbFrameSwitch()

    def back_button_menu(self):
        self.loginFrameSwitch()

    def dropdown(self):
        print('dropdown here')

if __name__=='__main__':
    root = tk.Tk()
    appInstance=mainApp(root)
    root.mainloop()


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