import customtkinter as ctk
from customtkinter import CTkLabel as label
from customtkinter import CTkEntry as entry
from customtkinter import CTkButton as button
import vpassElephant as vp
import checkCreds as cc

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def closeconnection(conn):  # <--------------- put it in class later
    try:
        if conn.closed==0:
            conn.close()
            print("connection closed: \n",str(conn))
    except Exception as e:
        print("Error Closing Connection to database: \n",e)

class login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.admin=False
        self.connections_dict={}
        self.minsize(600,600)
        self.title("Login page")
        self.rowconfigure(0,weight=0)
        self.columnconfigure(0,weight=1)
        width=600
        height=600
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
 
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.databaseurl_label=label(master=self, text="Database URL",font=("Arial",20))
        self.databaseurl_label.grid(row=1,column=0,padx=20,pady=(50,0))

        self.username_label=label(master=self,text="UserName",font=("Arial",20))
        self.username_label.grid(row=1,column=0,padx=20,pady=(50,0))

        self.password_label=label(master=self,text="Password",font=("Arial",20))
        self.password_label.grid(row=3,column=0,pady=(50,0))

        self.databaseurl_entry=entry(master=self, width=200,corner_radius=8,height=30,placeholder_text="Enter Database URL")
        self.databaseurl_entry.grid(row=2,column=0,pady=(10,0))

        self.username_entry=entry(master=self, width=200,corner_radius=8,height=30,placeholder_text="Enter UserName")
        self.username_entry.grid(row=2,column=0,pady=(10,0))

        self.password_entry = entry(master=self, width=200,corner_radius=8, height=30,placeholder_text="Enter password",show="•")
        self.password_entry.grid(row=4, column=0, pady=(10, 0))

        self.submit_button=button(master=self,width=100,command=self.submit_press,height=40,corner_radius=20,text="Submit")
        self.submit_button.grid(row=9,pady=(30,0),column=0,)

        self.error_label = label(master=self, text="", font=("Arial", 20), text_color="red")
        self.error_label.grid(row=10, pady=(30, 30), column=0)

        self.next_window = None

    def submit_press(self):
        dburl=self.databaseurl_entry.get()
        username=self.username_entry.get()
        password=self.password_entry.get()
        if dburl=="":
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

    def update_error_label(self, error_message):
        self.error_label.configure(text=error_message)

if __name__=="__main__":
    app=login()
    app.mainloop()
