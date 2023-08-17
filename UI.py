import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkButton as button
from customtkinter import CTkEntry as entry
from customtkinter import CTkLabel as label
from customtkinter import CTkToplevel as window
from customtkinter import CTkTextbox as textbox
from customtkinter import CTkOptionMenu as dropdown
import mysql.connector
import vpass as vp
import new_login_registration as nlr
import threading as th
import dropdown_dynamic as dd
import database_ui as dui
import Installation_files.databaseConnect as dc
from customtkinter import CTkSegmentedButton as rbutton 

def connect_database(u,p):
    try:
        mydb = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user=str(u),
            password=str(p),
            database=str(u)
        )
        mydb.close()
        return True
    except:
        return False

def provide_connect():
    dbp=dc.extractinfo()
    u,p=dbp[0],dbp[1]
    mydb = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user=str(u),
            password=str(p),
            database=str(u)
        )
    return mydb

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class login(ctk.CTk):
    def __init__(self):
        super().__init__()
        
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
     
        self.username_label = label(master=self, text="Username",font=("Arial",20))
        self.username_label.grid(row=1,column=0,padx=20,pady=(50,0))
        
        self.username=entry(master=self, width=200,corner_radius=8,height=30,placeholder_text="Enter username or E-mail ID")
        self.username.grid(row=2,column=0,pady=(10,0))

        
        self.password_label=label(master=self,text="Password",font=("Arial",20))
        self.password_label.grid(row=3,column=0,pady=(50,0))
        
        self.password = entry(master=self, width=200,corner_radius=8, height=30,placeholder_text="Enter password",show="•")
        self.password.grid(row=4, column=0, pady=(10, 0))
        self.host_label = label(
            master=self, text="Database Name", font=("Arial", 20))
        self.host_label.grid(row=5, column=0, padx=20, pady=(50, 0))

        self.host = entry(master=self, width=200, corner_radius=8,
                              height=30, placeholder_text="Enter host ID")
        self.host.grid(row=6, column=0, pady=(10, 0))

        self.Database_label = label(
            master=self, text="PasswordDB", font=("Arial", 20))
        self.Database_label.grid(row=7, column=0, pady=(50, 0))

        self.Database = entry(master=self, width=200, corner_radius=8,
                              height=30, placeholder_text="Enter Database ID", show="*")
        self.Database.grid(row=8, column=0, pady=(10, 0))

        
        self.submit=button(master=self,width=100,command=self.submit_press,height=40,corner_radius=20,text="Submit")
        self.submit.grid(row=9,pady=(30,0),column=0)
        
        
        
        self.next_window = None
        
    def check_con(self): #-------->add the backend here 
        user=self.host.get()
        password=self.Database.get()
        try:
            check=connect_database(user,password)
            if check==True:
                dc.copyinfo(user,password)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    def submit_press(self):
        uid=self.username.get()
        pwd=self.password.get()
        if self.get_credentials(uid,pwd) and self.check_con(): #use get credentials here
            self.open_next_window()
            
        elif not self.get_credentials(uid,pwd) :
            self.error_msg=label(master=self,text="Enter valid credentials")
            self.error_msg.grid(row=10,pady=(30,30),column=0)
            
        elif not self.check_con():
            self.error_msg = label(master=self, text="Unable to connect to Database")
            self.error_msg.grid(row=10, pady=(30, 30), column=0)


    ADMIN=True  #change this to false once code to check admin rights has been made

    def get_credentials(self,uid, pwd): #for login process at start not signup
        # Connect to the database
        mydb=provide_connect()
        c = mydb.cursor()

        c.execute("SELECT LOWER(username), password,Admin FROM credentails")

        rows = c.fetchall()
        c.close()
        mydb.close()
        

        for row in rows:

            if row[0] == str(uid).lower() and row[1] == pwd and row[2]==1:
                login.ADMIN=True
                return True
            elif row[0] == str(uid).lower() and row[1] == pwd and row[2]==0:
                login.ADMIN=False

            if row[0] == str(uid).lower() and row[1] == pwd:

                return True
       
        
        return False

            
    def closeall(self):
        self.quit()
    def open_next_window(self):
        if self.next_window is None or not self.next_window.winfo_exists():
            self.next_window=menu(self)
            self.next_window.protocol("WM_DELETE_WINDOW", self.closeall)
            self.withdraw()
            self.next_window.deiconify()
 
class menu(window):
    def __init__ (self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.minsize(400,400)
        self.title("Select and option")
        
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
        
        self.entry=button(master=self,text="Visitor Entry",height=50,width=100,command=self.open_visitor_entry)
        self.entry.grid(row=0,column=0,padx=10,pady=(20,0))
        
        self.exit=button(master=self,text="Visitor Exit",height=50,width=100,command=self.open_visitor_exit)
        self.exit.grid(row=0,column=1,padx=10,pady=(20,0))
        
        if login.ADMIN==True:
        
            self.database=button(master=self,text="Database",height=50,width=100,command=self.open_database)
            self.database.grid(row=1,column=0,padx=10,pady=(0,20))       
        
            self.signup=button(master=self,text="Sign-up",height=50,width=100,command=self.signup_pressed)
            self.signup.grid(row=1,column=1,padx=10,pady=(0,20))
            
            self.database_window = None
            self.sign_up_window = None
        
        
        self.visitor_entry =None
        self.visitor_exit=None
    
        
    def open_visitor_entry(self):
        if self.visitor_entry is None or not self.visitor_entry.winfo_exists():
            self.visitor_entry=enter_details(self)
            self.visitor_entry.protocol("WM_DELETE_WINDOW",self.quit)
            self.withdraw()
            self.visitor_entry.deiconify()

                                  #code to move to database search window

    def signup_pressed(self):
        if self.sign_up_window is None or not self.sign_up_window.winfo_exists():
            self.sign_up_window=sign_up(self)
            self.sign_up_window.protocol("WM_DELETE_WINDOW", self.quit)
            self.withdraw()
            self.sign_up_window.deiconify()
    
    
    def open_visitor_exit(self) :
        if self.visitor_exit is None or not self.visitor_exit.winfo_exists():
            self.visitor_exit=enter_barcode(self)
            self.visitor_exit.protocol("WM_DELETE_WINDOW",self.quit)
            self.withdraw()
            self.visitor_exit.deiconify()
            
    def open_database(self):
        '''if self.database_window is None or not self.database_window.winfo_exists():
            self.database_window=database(self)
            self.database_window.protocol("WM_DELETE_WINDOW",self.quit)
            self.withdraw()
            self.database_window.deiconify()'''
        d=database()
        d.download()
                
class enter_barcode(window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.minsize(400,300)
        self.title("Exit barcode scan")
        
        self.columnconfigure(0,weight=1)
        self.rowconfigure((0,1,2),weight=1)
        
        width=400
        height=300
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
 
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
        self.scanl=label (master=self,text="Enter barcode",font=("Arial", 20))
        self.scanl.grid(row=0,column=0,padx=20,pady=(20,0))
        
        self.scan=entry(master=self,width=200,height=30,placeholder_text="Enter barcode here")
        self.scan.grid(row=1,column=0,padx=20,pady=(20,0))
	
	
        self.submit = button(master=self, width=100, command=self.submit_press,height=40, corner_radius=20, text="Submit")
        self.submit.grid(row=2, pady=(30, 0), padx=(20, 20), column=0,sticky="W")
        
        
        
        self.back = button(master=self, height=40, width=100,text='Back', command=self.back_press, corner_radius=20)
        self.back.grid(row=2, column=0, pady=(30, 0), padx=(20, 20),sticky="E")
        
        self.status_label=label(master=self,text=" ")
        self.status_label.grid(row=3,column=0,pady=30,padx=20)
        
        self.menu=None
        
        
    def submit_press(self):
        #code to scan barcode upon exit
        b=self.scan.get()
        self.scan.delete(0,tk.END)
        vp.exit(b)
        #use self.status_label.configure(text="Scan complete , exit time =") to show scan is successful in ui
        return
        
    def back_press(self):
        if self.menu is None or not self.menu.winfo_exists():
            self.menu = menu(self)
            self.menu.protocol("WM_DELETE_WINDOW", self.quit)
            self.withdraw()
            self.menu.deiconify()

class database(): #-----------------------------------------------------------------label to be added here!!!!
    def download(self):
        vp.database_download()
        dui.run_main()
    '''def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.minsize(1000,1000)
        self.title("Database Access")  
        
        self.columnconfigure((0),weight=1)
        
        self.Main_heading=label(master=self,text="Please select respective type to search for",font=("Arial",20))
        self.Main_heading.grid(row=0,column=0,padx=20,pady=(20,0))

        self.rbut=rbutton(master=self,values=["Name","Phone number","E-mail","Faculty"])
        self.rbut.grid(row=1,column=0,padx=20,pady=(20.0))
        
        self.enter=entry(master=self,placeholder_text="",width=100,height=30).grid(row=2,column=0,padx=20,pady=(20,0))
        
        choice=self.rbut.get()
        
        if choice=="Name":
            self.enter.configure(placeholder_text="Enter name")
        elif choice=="Phone number":
            self.enter.configure(placeholder_text="Enter name")'''
        

class sign_up(window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.minsize(600, 400)
        self.title("Sign-up page")
        self.rowconfigure(0, weight=0)
        self.columnconfigure((0,1,2), weight=1)
        
        width=600
        height=400
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
 
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
        

        self.username_label = label(
            master=self, text="Username", font=("Arial", 20))
        self.username_label.grid(row=1, column=1, padx=20, pady=(50, 0))

        self.username = entry(master=self, width=200, corner_radius=8,
                              height=30, placeholder_text="Enter username or E-mail ID")
        self.username.grid(row=2, column=1, pady=(10, 0))

        self.password_label = label(
            master=self, text="Password", font=("Arial", 20))
        self.password_label.grid(
            row=3, column=1, pady=(50, 0))

        self.password = entry(master=self, width=200, corner_radius=8,
                              height=30, placeholder_text="Enter password", show="*")
        self.password.grid(row=4, column=1, pady=(10, 0))

        self.submit = button(master=self, width=100, command=self.submit_press,
                             height=40, corner_radius=20, text="Submit")
        self.submit.grid(row=6, pady=(30, 30), padx=(20, 20), column=1,sticky="E")
        
        
        
        self.back = button(master=self, height=40, width=100,
                           text='Back', command=self.back_press, corner_radius=20)
        self.back.grid(row=6, column=1, pady=(30, 30), padx=(20, 20),sticky="W")
        
        self.rbut1=rbutton(master=self, values=["ADMIN","NON-ADMIN"] )
        self.rbut1.grid(row=5,column=1,pady=(20,0),padx=20
        
        )
        
        self.status_label=label(master=self,text=" ")
        self.status_label.grid(row=7,column=1,pady=30,padx=20
        )
        
        
        self.menu=None
        
    def submit_press(self):
        username = self.username.get()
        password = self.password.get()
        admin=self.rbut1.get()
        if admin=="ADMIN":
                admin=1
        else:
                admin=0
        status=nlr.main_run(username,password,admin)
        if status==0:
            self.status_label.configure(text="Credentials already exist.")
        else:
            self.status_label.configure(text="Inserted.")
        self.username.delete(0,tk.END)
        self.password.delete(0,tk.END)
        self.username.focus_set()
        # write code to create login credentials
        #<--------Write me a another option called "barcode_scanning"
        return

    def back_press(self):
        if self.menu is None or not self.menu.winfo_exists():
            self.menu = menu(self)
            self.menu.protocol("WM_DELETE_WINDOW", self.quit)
            self.withdraw()
            self.menu.deiconify()
            
class enter_details(window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Enter the details")
        self.columnconfigure((0,1,2),weight=0)
        self.rowconfigure((0,1),weight=0)
        
        self.geometry("1000x1000")
        
        
        
        width=1000
        height=1000
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
 
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
        

        self.name_l = label(master=self, text="Name of visitor", font=("Arial", 20))
        self.name_l.grid(row=0, column=0, sticky="W", padx=(20,0), pady=(20,0))

        self.name_box = entry(master=self, height=50, width=300,placeholder_text="Enter visitor name")
        self.name_box.grid(row=1, column=0, sticky="W", padx=(20,0), pady=(0,10))

        self.num_l = label(master=self, text="Visitor number", font=("Arial", 20))
        self.num_l.grid(row=0, column=1, sticky="W",padx=(20, 0), pady=(20, 0))

        self.num_box = entry(master=self, height=50, width=200,placeholder_text="Enter visitor number")
        self.num_box.grid(row=1, column=1, sticky="W",padx=(20, 0), pady=(0, 10))

        self.mail_l =  label(master=self, text="E-mail address", font=("Arial", 20))
        self.mail_l.grid(row=0, column=2, sticky="W",padx=(20, 0), pady=(20, 0))

        self.mail_box = entry(master=self, height=50, width=300,placeholder_text="Enter visitor E-mail")
        self.mail_box.grid(row=1, column=2, sticky="W",padx=(20, 20), pady=(0, 10))
        
        self.reason_l = label(
            master=self, text="Reason for Visit", font=("Arial", 20))
        self.reason_l.grid(row=2, column=0, sticky="W",padx=(20, 0), pady=(20, 0))
        
        self.reason_box = entry(
            master=self, height=50, width=300, placeholder_text="Enter reason for visit")
        self.reason_box.grid(row=3, column=0, columnspan=3, rowspan=1, sticky="NSEW", padx=(
            20, 20), pady=(0, 10))
        
        
        self.faculty_l=label( master=self, text="Faculty to visit",font=("Arial",20))
        self.faculty_l.grid(row=4,column=0,sticky="W",padx=(20,0),pady=(20,0) )

        self.fac_button=button(master=self,height=40,width=40,corner_radius=10,text="Dropdown",command=self.dropdown_run)
        self.fac_button.grid(row=4,column=1, columnspan=3, rowspan=1, sticky="NSEW", padx=(
            20, 40), pady=(50, 40))
        
        '''self.faculty_menu = dropdown(
            master=self, values=self.faculty_list(),  height=50, width=200,font=("Arial",12))
        self.faculty_menu.grid(row=5,column=0,padx=(20, 0), pady=(20, 0),sticky="W")
        self.faculty_menu.set(value="Select the faculty to visit")''' 
        
        # add command=self.submit_press here 
        self.submit = button(master=self, height=50,
                             width=100,  corner_radius=10, text="Submit",command=self.submit_press) 
        self.submit.grid(row=8, pady=(40, 0), column=0,sticky="W",padx=20)
        
        self.barcodel =  label(master=self, text="Barcode No.", font=("Arial", 20))
        self.barcodel.grid(row=6, column=0, sticky="W",padx=(20, 0), pady=(20, 0))
        
        self.barcode = entry(master=self, height=50, width=300,placeholder_text="Enter Barcode number")
        self.barcode.grid(row=7, column=0, sticky="W",padx=(20, 20), pady=(0, 10))
        
        self.grid_propagate(False)
        

        self.resizable(False, False)

        self.name_box.bind("<Return>", focus_next_widget)
        self.num_box.bind("<Return>", focus_next_widget)
        self.mail_box.bind("<Return>", focus_next_widget)
        '''self.faculty_menu.bind("<Return>", focus_next_widget)'''
        self.reason_box.bind("<Return>", focus_next_widget)
        self.barcode.bind("<Return>",focus_next_widget)
        self.submit.bind("<Return>", lambda event: self.submit.invoke())

        self.back = button(master=self, height=50, width=100,
                           corner_radius=10, text='Back', command=self.back_press)
        self.back.grid(row=8, column=1, pady=(40, 0), padx=(20, 0), sticky="E")
        
        self.menu=None


    '''def faculty_list(self):
        file = open(
            "fac_list.txt", "r")
        details=file.readlines()
        details=[x.rstrip('\n') for x in details]
        return details'''
    
    def dropdown_run(self):
        value=dd.run_main()
        self.fac_value=value
    
    def back_press(self):
        if self.menu is None or not self.menu.winfo_exists():
            self.menu = menu(self)
            self.menu.protocol("WM_DELETE_WINDOW", self.quit)
            self.withdraw()
            self.menu.deiconify()

    def submit_press(self):
        self.data=[]
        name=self.name_box.get()
        num=self.num_box.get()
        mail=self.mail_box.get()
        reason=self.reason_box.get()
        '''fac=self.faculty_menu.get()'''
        fptr=open('selected.txt','r')
        data=fptr.read()
        fptr.close()
        fac=data
        code=self.barcode.get()
        if (name=="" or num=="" or mail=="" or reason=="" or code=="") or fac == "Select the faculty to visit":
            self.error=label(master=self,text="Kindly fill all the details",font=("Arial",15))
            self.error.grid(row=7,pady=(20,0),column=0,sticky="W",padx=20)
            
        else:
            #self.submit_details(name,num,mail,reason,fac)
            self.submitclear()
            t1=th.Thread(target=self.threadbg,args=(name,num,mail,fac,reason,code))
            t1.start()
            #data
            return
    #def submit_details(self,name,num,mail,reason,fac):
    def submitclear(self):
        self.name_box.delete(0, tk.END)
        self.num_box.delete(0, tk.END)
        self.mail_box.delete(0, tk.END)
        self.reason_box.delete(0, tk.END)
        self.barcode.delete(0,tk.END)
        self.name_box.focus_set()
    
    def threadbg(self,name,num,mail,fac,reason,code):
        vp.allthreadrun(name,num,mail,fac,reason,code)

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"
            
if __name__=="__main__":
    app=login()
    app.mainloop()