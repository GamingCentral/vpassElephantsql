import tkinter as tk
from tkinter import ttk
import mainAppBackend as backend
import json
'''from loginFrame import Login
from menuFrame import Men'''
#import connectionpool as cp

class mainApp:
    def __init__(self,root):
        self.root:tk.Tk=root
        self.root.configure(bg='#ebedf0')

        style = ttk.Style()
        style.configure("TFrame", background='#ebedf0')
        style.configure("TNotebook.Tab", background="#426ae3")
        style.map("TNotebook", background= [("selected", "#426ae3")])

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
        self.pool = None
        self.faculty_selected = None
        #self.admin = 0 #default
        self.dbFrameInitalizer()
        self.loginFrameInitializer()
        self.menuFrameInitializer()

        self.frameSwitch(self.dbFrame)

    def dbFrameInitalizer(self):

        self.databaseurl_label = tk.Label(self.dbFrame, text="Database URL", font=("bookman old style", 15), fg="#0a0a0a", bg="#ebedf0")
        self.databaseurl_label.pack(pady=45)
        self.databaseurl_entry = tk.Entry(self.dbFrame, width=82, font=("Helvetica", 11), bg="white", fg="black")
        self.databaseurl_entry.pack(pady=5)

        ##############################################################################
        self.submit_button = tk.Button(self.dbFrame, width=20, command=self.submit_press_dburl, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=45)

        self.error_label_dburl = tk.Label(self.dbFrame, text=None, font=("bookman old style", 12), fg="red", bg='#ebedf0')
        self.error_label_dburl.pack()

    def loginFrameInitializer(self):

        self.title_label = tk.Label(self.loginFrame, text="Login", font=("courier new", 45, "bold"), fg="#426ae3", bg="#ebedf0")
        self.title_label.pack(pady=20)

        self.username_label = tk.Label(self.loginFrame, text="UserName", font=("bookman old style", 15),fg="#0a0a0a", bg="#ebedf0")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.loginFrame, width=72,font=("gothic",13), bg="white", fg="black")
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.loginFrame, text="Password", font=("bookman old style", 15),fg="#0a0a0a", bg="#ebedf0")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.loginFrame, width=72,font=("Helvetica",12), show="•", bg="white", fg="black")
        self.password_entry.pack(pady=5)

        ##########################################################################
        self.submit_button = tk.Button(self.loginFrame, width=20, command=self.submit_press_login, text="Submit",font=("courier new bold",15),bg="#426ae3",fg="black")
        self.submit_button.pack(pady=30)

        ##########################################################################
        self.back_button = tk.Button(self.loginFrame, text="Back", width=20, command=self.back_press_login, font=("courier new bold",15),bg="#426ae3",fg="black")
        self.back_button.pack(pady=50)

        self.error_label_login = tk.Label(self.loginFrame, text=None, font=("bookman old style", 12), fg="red",bg='#ebedf0')
        self.error_label_login.pack()

    def menuFrameInitializer(self): #intialise after self.admin is fetched

        self.notebook = ttk.Notebook(self.menuFrame,width=self.ww)
        
        self.visitorEntry = ttk.Frame(self.notebook) #showdefault?
        self.addVisitorEntry()
        self.visitorExit = ttk.Frame(self.notebook)
        self.addVisitorExit()
        self.signup = ttk.Frame(self.notebook)
        self.addSignUp()
        self.facultyRegistration = ttk.Frame(self.notebook)
        self.addFacultyRegistration()
        self.qrRegistration = ttk.Frame(self.notebook)
        self.addqrRegistration()

        self.notebook.add(self.visitorEntry, text='Visitor Entry')
        self.notebook.add(self.visitorExit, text='visitor Exit')  

        backButton = tk.Button(self.menuFrame, text='Back', command=self.back_button_menu, font=("courier new bold",15),bg="#426ae3",fg="black")
        self.notebook.pack(pady=10)
        backButton.pack(pady=10)

    def addVisitorEntry(self):
        self.entry_label = tk.Label(self.visitorEntry, text="Visitor Entry", font=("courier new bold", 25), fg="#426ae3", bg="#ebedf0")
        self.entry_label.pack(pady=15)

        self.visitorNameLabel = tk.Label(self.visitorEntry, text="Name", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.visitorNameLabel.pack()
        self.visitorNameEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="black")
        self.visitorNameEntry.pack(pady=3)

        self.visitorNumberLabel = tk.Label(self.visitorEntry, text="Phone Number", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.visitorNumberLabel.pack()
        self.visitorNumberEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="black")
        self.visitorNumberEntry.pack(pady=3)

        self.visitorEmailLabel = tk.Label(self.visitorEntry, text="Email", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.visitorEmailLabel.pack()
        self.visitorEmailEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="black")
        self.visitorEmailEntry.pack(pady=3)

        # to be switched with a dropdown
        self.visitorFacultyLabel = tk.Label(self.visitorEntry, text="Faculty Name", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.visitorFacultyLabel.pack()
        self.visitorFacultyButton = tk.Button(self.visitorEntry, text="🠟", font=25, width=10, bg='#426ae3',command=self.dropdown)
        self.visitorFacultyButton.pack(pady=3)

        self.visitorReasonLabel = tk.Label(self.visitorEntry, text="Reason To Visit", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.visitorReasonLabel.pack()
        self.visitorReasonEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="black")
        self.visitorReasonEntry.pack(pady=3)

        self.visitorBarcodeLabel = tk.Label(self.visitorEntry, text="Scan Barcode Here", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.visitorBarcodeLabel.pack()
        self.visitorBarcodeEntry = tk.Entry(self.visitorEntry, width=72,font=("gothic",13), bg="white", fg="black")
        self.visitorBarcodeEntry.pack(pady=3)

        self.submit_button = tk.Button(self.visitorEntry, width=40, command=self.submit_press_visitorEntry, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=15)

        self.error_label_visitorEntry = tk.Label(self.visitorEntry, text='this is error', font=("bookman old style", 15), fg="red", bg='#ebedf0')
        self.error_label_visitorEntry.pack()
    
    def addVisitorExit(self):
        self.exit_label = tk.Label(self.visitorExit, text="Visitor Exit", font=("courier new bold", 35), fg="#426ae3", bg="#ebedf0")
        self.exit_label.pack(pady=35)

        self.barcodeExit = tk.Label(self.visitorExit, text="Name", font=("bookman old style", 15),fg="#0a0a0a", bg="#ebedf0")
        self.barcodeExit.pack()
        self.visitorBarcodeExit = tk.Entry(self.visitorExit, width=72,font=("gothic",13), bg="white", fg="black")
        self.visitorBarcodeExit.pack(pady=10)

        self.submit_button = tk.Button(self.visitorExit, width=30, command=self.submit_press_visitorExit, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=35)

        self.error_label_visitorEntry = tk.Label(self.visitorExit, text='this is error', font=("bookman old style", 15), fg="red", bg='#ebedf0')
        self.error_label_visitorEntry.pack(pady=15)
    
    def addSignUp(self):
        self.exit_label = tk.Label(self.signup, text="Register User", font=("courier new bold", 35), fg="#426ae3", bg="#ebedf0")
        self.exit_label.pack(pady=35)

        self.username_label_signup = tk.Label(self.signup, text="UserName", font=("bookman old style", 15),fg="#0a0a0a", bg="#ebedf0")
        self.username_label_signup.pack()
        self.username_entry_singup = tk.Entry(self.signup, width=72,font=("gothic",13), bg="white", fg="black")
        self.username_entry_singup.pack(pady=5)

        self.password_label_signup = tk.Label(self.signup, text="Password", font=("bookman old style", 15),fg="#0a0a0a", bg="#ebedf0")
        self.password_label_signup.pack()
        self.password_entry_singup = tk.Entry(self.signup, width=72,font=("Helvetica",12), bg="white", fg="black")
        self.password_entry_singup.pack(pady=5)

        self.admin_var = tk.IntVar()
        self.admin_checkbox = tk.Checkbutton(self.signup, text="Admin", variable=self.admin_var, font=("bookman old style", 15), fg="#0a0a0a", bg="#ebedf0")
        self.admin_checkbox.pack(pady=5)

        ##########################################################################
        self.submit_button = tk.Button(self.signup, width=20, command=self.submit_press_signup, text="Submit",font=("courier new bold",15),bg="#426ae3",fg="black")
        self.submit_button.pack(pady=30)

        self.error_label_signup = tk.Label(self.signup, text='this is error', font=("bookman old style", 12), fg="red",bg='#ebedf0')
        self.error_label_signup.pack()

    def addFacultyRegistration(self):
        self.faculty_label = tk.Label(self.facultyRegistration, text="Faculty Registration", font=("courier new bold", 25), fg="#426ae3", bg="#ebedf0")
        self.faculty_label.pack(pady=15)

        self.facultyNameLabel = tk.Label(self.facultyRegistration, text="Name", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.facultyNameLabel.pack()
        self.facultyNameEntry = tk.Entry(self.facultyRegistration, width=72,font=("gothic",13), bg="white", fg="black")
        self.facultyNameEntry.pack(pady=3)

        self.facultyNumberLabel = tk.Label(self.facultyRegistration, text="Phone Number", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.facultyNumberLabel.pack()
        self.facultyNumberEntry = tk.Entry(self.facultyRegistration, width=72,font=("gothic",13), bg="white", fg="black")
        self.facultyNumberEntry.pack(pady=3)

        self.facultyEmailLabel = tk.Label(self.facultyRegistration, text="Email", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.facultyEmailLabel.pack()
        self.facultyEmailEntry = tk.Entry(self.facultyRegistration, width=72,font=("gothic",13), bg="white", fg="black")
        self.facultyEmailEntry.pack(pady=3)

        self.facultyDeptLabel = tk.Label(self.facultyRegistration, text="Department", font=("bookman old style", 12),fg="#0a0a0a", bg="#ebedf0")
        self.facultyDeptLabel.pack()
        self.facultyDeptEntry = tk.Entry(self.facultyRegistration, width=72,font=("gothic",13), bg="white", fg="black")
        self.facultyDeptEntry.pack(pady=3)

        self.submit_button = tk.Button(self.facultyRegistration, width=40, command=self.submit_press_facultyRegister, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=15)

        self.error_label_faculty = tk.Label(self.facultyRegistration, text='this is error', font=("bookman old style", 15), fg="red", bg='#ebedf0')
        self.error_label_faculty.pack()

    def addqrRegistration(self):
        self.qr_label = tk.Label(self.qrRegistration, text="Barcode Registration", font=("courier new bold", 35), fg="#426ae3", bg="#ebedf0")
        self.qr_label.pack(pady=35)

        self.barcodeNew = tk.Label(self.qrRegistration, text="Scan Barcode Here", font=("bookman old style", 15),fg="#0a0a0a", bg="#ebedf0")
        self.barcodeNew.pack()
        self.barcodeNewEntry = tk.Entry(self.qrRegistration, width=72,font=("gothic",13), bg="white", fg="black")
        self.barcodeNewEntry.pack(pady=10)

        self.submit_button = tk.Button(self.qrRegistration, width=30, command=self.submit_press_qrRegister, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=35)

        self.error_label_qr = tk.Label(self.qrRegistration, text='this is error', font=("bookman old style", 15), fg="red", bg='#ebedf0')
        self.error_label_qr.pack(pady=15) 

    def menuFrameUpdater(self):
        self.notebook.add(self.signup, text='Sign Up/ Register')
        self.notebook.add(self.facultyRegistration, text='Faculty Registration')
        self.notebook.add(self.qrRegistration, text='QR Registration')

    def menuFrameRemover(self):
        self.notebook.forget(self.signup)
        self.notebook.forget(self.facultyRegistration)
        self.notebook.forget(self.qrRegistration)

    def update_error_label_dburl(self,message):
        self.error_label_dburl.config(text=message)
    
    def update_error_label_login(self,message):
        self.error_label_login.config(text=message)

    def update_error_label_facultyRegistration(self,message):
        self.error_label_faculty.config(text=message)

    def update_error_label_signup(self,message):
        self.error_label_signup.config(text=message)

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
        '''self.loginFrameSwitch()''' #remove later ###################################################
        databaseURL = self.databaseurl_entry.get()
        if databaseURL=='':
            self.update_error_label_dburl("Please enter the database url")
        else:
            object = backend.dbUrlFunctions(databaseURL)
            poolObject = object.fetchPoolObject()
            if not isinstance(poolObject,int):
                self.databaseurl_entry.delete(0,tk.END)
                self.pool=poolObject
                self.facultyObject = backend.facultyFunctions(self.pool)
                response = self.facultyObject.initalCallToJson()
                if response==1:
                    self.loginFrameSwitch()
                else:
                    self.update_error_label_dburl('Connectivity lost to database\nUnable to fetch required data')
            else:
                self.update_error_label_dburl("Database URL was not valid or\nCheck Internet Connection")

    def submit_press_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username=='' or password=='':
            self.update_error_label_login("Please enter the username and password")
        else:
            try:
                obj = backend.loginFunctions(username,password,self.pool)
                admin = obj.checkUser()
                if isinstance(admin,int):
                    if admin==1:
                        self.menuFrameUpdater()
                    self.menuFrameSwitch()
                else:
                    self.update_error_label_login(admin) # here admin becomes exception or error message
            except Exception as e:
                print(e)
                self.update_error_label_login("Lost Internet Connection")

    def back_press_login(self):
        self.username_entry.delete(0,tk.END)
        self.password_entry.delete(0,tk.END)
        self.on_closing()
        self.pool=None
        self.dbFrameSwitch()

    def back_button_menu(self):
        try:
            self.username_entry.delete(0,tk.END)
            self.password_entry.delete(0,tk.END)
            self.menuFrameRemover()
        except Exception:
            pass
        self.loginFrameSwitch()

    def dropdown(self):
        self.dropdownFrame = tk.Toplevel(self.visitorEntry)
        self.dropdownFrame.title("Faculty Dropdown")
        self.dropdownFrame.configure(bg='#ebedf0')
        self.dropdownFrame.resizable(False,False)
        self.faculty_data = read_faculty_data_from_json("json_data.json")
        def callback(selected_value):
            self.dropdownFrame.destroy()
            self.faculty_selected = selected_value
            print(self.faculty_selected)
        
        faculty_data_entry = FacultyDataEntryFrame(self.dropdownFrame, callback, self.faculty_data)

    def submit_press_visitorEntry(self):
        print('visitor entry data')

    def submit_press_visitorExit(self):
        print('submit function here')

    def submit_press_signup(self):
        if self.username_entry_singup.get()=='' or self.password_entry_singup.get()=='':
            self.update_error_label_signup("Please fill all the details")
        else:
            obj = backend.signUpFunctions(self.pool)
            response = obj.signUp(self.username_entry_singup.get(),self.password_entry_singup.get(),self.admin_var.get())
            if not isinstance(response,str):
                if response==1:
                    self.update_error_label_signup("User Registered Successfully")
                else:
                    self.update_error_label_signup('User Already Exists')
                self.username_entry_singup.delete(0,tk.END)
                self.password_entry_singup.delete(0,tk.END)
            else:
                self.update_error_label_signup(response)


    def submit_press_facultyRegister(self):
        facultyName = self.facultyNameEntry.get()
        facultyNumber = self.facultyNumberEntry.get()
        facultyEmail = self.facultyEmailEntry.get()
        facultyDept = self.facultyDeptEntry.get()
        if facultyName=='' or facultyNumber=='' or facultyEmail=='' or facultyDept=='':
            self.error_label_faculty.config("Please fill all the details")
        else:
            response = self.facultyObject.facultyRegister(facultyName,facultyNumber,facultyEmail,facultyDept)
            self.update_error_label_facultyRegistration(response)
            if response==1:
                self.facultyNameEntry.delete(0,tk.END)
                self.facultyNumberEntry.delete(0,tk.END)
                self.facultyEmailEntry.delete(0,tk.END)
                self.facultyDeptEntry.delete(0,tk.END)


    def submit_press_qrRegister(self):
        print('to qr register')

    def on_closing(self):
        try:
            if self.pool is not None:
                self.pool.close_pool()
                print("All Connections are Closed")
            else:
                print("No Connections were taken")
        except Exception as e:
            print(e)

class FacultyDataEntryFrame(tk.Frame):
    def __init__(self, master=None, callback=None, faculty_data=None):
        super().__init__(master)
        self.master = master
        self.callback = callback
        self.faculty_data = faculty_data or []
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        self.branch_label = ttk.Label(self, text="Branch:")
        self.branch_label.grid(row=0, column=0, padx=10, pady=10)
        self.branch_var = tk.StringVar()
        self.phno_var = tk.StringVar()

        # Combo box for selecting the branch
        self.branch_combo_box = ttk.Combobox(self, state="readonly", textvariable=self.branch_var)
        self.branch_combo_box.grid(row=0, column=1, padx=10, pady=10)
        branches = set(faculty["dept"] for faculty in self.faculty_data)
        self.branch_combo_box['values'] = [""] + list(branches)  # Add an empty option for no selection
        self.branch_var.trace_add("write", self.update_name_combo_box)  # Attach a callback to update name combo box

        self.phno_label = ttk.Label(self, text="Phone Number:")
        self.phno_label.grid(row=0, column=2, padx=10, pady=10)

        self.phno_entry = ttk.Entry(self, textvariable=self.phno_var)
        self.phno_entry.grid(row=0, column=3, padx=10, pady=10)
        self.phno_var.trace_add("write", self.update_name_combo_box)  # Attach a callback to update name combo box

        self.name_label = ttk.Label(self, text="Name:")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)

        self.name_combo_box = ttk.Combobox(self, state="readonly")
        self.name_combo_box.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.name_combo_box.bind("<<ComboboxSelected>>", self.on_name_select)  # Attach a callback for selection

        all_names = [faculty["name"] for faculty in self.faculty_data]
        self.name_combo_box['values'] = all_names

    def update_name_combo_box(self, *args):
        selected_branch = self.branch_var.get()
        selected_phno = self.phno_var.get()

        if not selected_branch and not selected_phno:
            all_names = [faculty["name"] for faculty in self.faculty_data]
            self.name_combo_box['values'] = all_names
        else:
            filtered_names = [faculty["name"] for faculty in self.faculty_data
                              if (not selected_branch or faculty["dept"] == selected_branch) and
                              (not selected_phno or faculty["phno"] == selected_phno)]

            self.name_combo_box['values'] = filtered_names

    def on_name_select(self, event):
        selected_value = self.name_combo_box.get()
        print(f"Selected Name: {selected_value}")
        if self.callback:
            self.callback(selected_value)

def read_faculty_data_from_json(file_path):
    with open(file_path, 'r') as file:
        faculty_data = json.load(file)
    return faculty_data

if __name__=='__main__':
    root = tk.Tk()
    appInstance=mainApp(root)
    root.mainloop()
    try:
        root.protocol("WM_DELETE_WINDOW",appInstance.on_closing())
    except Exception as e:
        print(e)
        pass
