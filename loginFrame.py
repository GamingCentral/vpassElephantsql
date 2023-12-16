import tkinter as tk
import checkCreds as cc
import connectionpool as cp

class Login(tk.Tk):
    def __init__(self,switch,pool,mfu):
        super().__init__()
        
        self.configure(bg='#141414')
        self.switchingFunction=switch
        self.pool=pool
        self.menuFrameUpdater = mfu

        self.title_label = tk.Label(self, text="Login", font=("courier new", 45, "bold"), fg="#426ae3", bg="#141414")
        self.title_label.pack(pady=20)

        self.username_label = tk.Label(self, text="UserName", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, width=70,font=("Helvetica",12), show="•", bg="white", fg="#141414")
        self.password_entry.pack(pady=5)

        self.submit_button = tk.Button(self, width=20, command=self.submit_press, text="Submit",font=("courier new bold",15),bg="#426ae3",fg="black")
        self.submit_button.pack(pady=30)

        self.back_button = tk.Button(self, text="Back", width=20, command=self.back_press, font=("courier new bold",15),bg="#426ae3",fg="black")
        self.back_button.pack(pady=50)

        self.error_label = tk.Label(self, text=None, font=("bookman old style", 12), fg="red",bg='#141414')
        self.error_label.pack()

    def submit_press(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username=="" or password=="":
            self.update_error_label("Please fill the fields to continue")
        else:
            try:
                self.connection = self.pool.get_connection()
                if isinstance(self.connection) is not str:
                    self.admin = self.credentialCheck(username,password,self.connection) #send admin when calling menu
                    if callable(self.menuFrameUpdater):
                        self.menuFrameUpdater(self.admin)

            except Exception as e:
                print(e)
        
    def back_press(self):
        self.switchingFunction("Main")
    
    def update_error_label(self,message):
        self.error_label.config(text=message)

    def credentialCheck(self,username,password,connection):
        admin=cc.credchecker(username,password,connection) #returns admin value(int 0 or 1) or None 
        if admin is not None:
            self.update_error_label("")
            if admin==1 or admin=='1':
                self.admin=True  #user is an admin
            self.update_error_label("next window shows up") #next menu frame here
            self.pool.return_connection(connection) #should i return tho?
            return admin
        else:
            self.update_error_label("Invalid Credentials--Please retry combination")
            return None

