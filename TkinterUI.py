import tkinter as tk
import vpassElephant as vp
import checkCreds as cc


def closeconnection(conn):  # <--------------- put it in class later
    try:
        if conn.closed==0:
            conn.close()
            print("connection closed: \n",str(conn))
    except Exception as e:
        print("Error Closing Connection to database: \n",e)

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.admin = False
        self.connections_dict = {}
        self.minsize(800, 450)
        self.title("Login page")
        self.geometry_centered(800, 450)
        self.configure(bg='#141414')

        self.title_label = tk.Label(self, text="Login", font=("courier new", 45, "bold"), fg="#426ae3", bg="#141414")
        self.title_label.pack(pady=20)

        self.databaseurl_label = tk.Label(self, text="Database URL", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.databaseurl_label.pack()
        self.databaseurl_entry = tk.Entry(self, width=82, font=("Helvetica",11), bg="white", fg="#141414")
        self.databaseurl_entry.pack(pady=5)
        #self.databaseurl_entry.grid(row=1, column=1, pady=(50, 0))
        #self.databaseurl_label.grid(row=1, column=0, padx=20, pady=(50, 0))

        self.username_label = tk.Label(self, text="UserName", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.username_label.pack()
        #self.username_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.username_entry = tk.Entry(self, width=72,font=("gothic",13), bg="white", fg="#141414")
        self.username_entry.pack(pady=5)
        #self.username_entry.grid(row=2, column=1, pady=(10, 0))

        self.password_label = tk.Label(self, text="Password", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.password_label.pack()
        #self.password_label.grid(row=3, column=0, pady=(10, 0))
        self.password_entry = tk.Entry(self, width=70,font=("Helvetica",12), show="•", bg="white", fg="#141414")
        self.password_entry.pack(pady=5)
        #self.password_entry.grid(row=3, column=1, pady=(10, 0))

        self.submit_button = tk.Button(self, width=20, command=self.submit_press, text="Submit",font=("courier new bold",15),bg="#426ae3",fg="black")
        self.submit_button.pack(pady=30)
        #self.submit_button.grid(row=4, pady=(30, 0), column=1)

        self.error_label = tk.Label(self, text=None, font=("bookman old style", 12), fg="red",bg='#141414')
        self.error_label.pack()
        #self.error_label.grid(row=5, pady=(10, 10), column=0, columnspan=2)

        self.next_window = None

    def geometry_centered(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def submit_press(self):
        dburl = self.databaseurl_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if dburl == "" or username=="" or password=="":
            self.update_error_label("Please fill the fields to continue")
        else: #need to check for credentials and dburl validity
            #checking url validity
            try:
                if dburl in self.connections_dict: #the connection exists
                    connection=self.connections_dict[dburl]  #fetches an existing connection object
                else:
                    connection=vp.runcheckconnect(dburl)
                if isinstance(connection,str):
                    self.update_error_label("Error: Database URL Not Found--Check the url again.")
                else: #returns connection
                    self.update_error_label("")
                    print("Array recieved: Connection Success! ",connection)
                    self.connections_dict[dburl]=connection #added connection to the dict
                    admin=cc.credchecker(username,password,connection) #returns admin value(int 0 or 1) or None 
                    if admin is not None:
                        if admin==1 or admin=='1':
                            self.admin=True  #user is an admin
                    else:
                        self.update_error_label("Invalid Credentials--Please retry combination")
                    closeconnection(connection)     # <----------- current connection being closed here
                    del self.connections_dict[dburl]
                    #further operations or re-entering the detials
                    #got connection now check for credentials
            except Exception as e:
                print(e)

    def update_error_label(self, message):
        self.error_label.config(text=message)


if __name__ == "__main__":
    app = Login()
    app.mainloop()
