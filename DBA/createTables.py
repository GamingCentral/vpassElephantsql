import tkinter as tk
import connectionpool as cp

class createtables(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Create Tables")
        self.minsize(800,400)
        self.connections_dict = {}
        self.geometry_centered(800,400)
        self.configure(bg='#141414')

        self.title_label = tk.Label(self, text="Make Database Tables", font=("courier new", 45, "bold"), fg="#426ae3", bg="#141414")
        self.title_label.pack(pady=20)

        self.databaseurl_label = tk.Label(self, text="Database URL", font=("bookman old style", 15),fg="gray", bg="#141414")
        self.databaseurl_label.pack()
        self.databaseurl_entry = tk.Entry(self, width=82, font=("Helvetica",11), bg="white", fg="#141414")
        self.databaseurl_entry.pack(pady=5)

        self.submit_button = tk.Button(self, width=20, command=self.submit_press, text="Submit",font=("courier new bold",15),bg="#426ae3",fg="black")
        self.submit_button.pack(pady=30)
        #self.submit_button.grid(row=4, pady=(30, 0), column=1)

        self.error_label = tk.Label(self, text=None, font=("bookman old style", 12), fg="red",bg='#141414')
        self.error_label.pack()

        self.next_window = None

    def geometry_centered(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def submit_press(self):
        dburl = self.databaseurl_entry.get()
        if dburl == "":
            self.update_error_label("Please fill the fields to continue")
        else: #need to check for credentials and dburl validity
            #checking url validity
            try:
                self.pool=cp.poolcreate(dburl)
                connection=self.pool.get_connection()
                if isinstance(connection,str):
                    self.update_error_label("Error: Database URL Not Found / No Internet Connection")
                else: #returns connection
                    self.update_error_label("")
                    try:
                        res=self.tablecreate(connection)
                        if res==1:
                            self.update_error_label("Created all tables required: you can now close this window")
                            self.pool.return_connection(connection)
                            self.pool.close_pool()
                        else:
                            res=self.pool.recover_connection(connection)
                            if res==0: #connection not recovered
                                self.pool.return_connection(connection)
                            self.update_error_label("Unable to get connection / No Internet Connection")
                    except Exception as e:
                        print(e)
                        self.pool.close_pool()
                        print('connections closed')
            except Exception as e:
                print(e)

    def tablecreate(self,connection):
        create_qravailable_query="CREATE TABLE IF NOT EXISTS QRavailable (qrid VARCHAR(50) PRIMARY KEY,availability integer default 1 not null)"
        create_records_query = "CREATE TABLE IF NOT EXISTS Records (vid BIGINT PRIMARY KEY,qrid VARCHAR(50),Name VARCHAR(25),PhoneNumber varchar(20),Email VARCHAR(40),PersonToVisit VARCHAR(25), ReasonToVisit VARCHAR(75),InTime varchar(20),OutTime varchar(20) default NULL,foreign key(qrid) references qravailable(qrid))"
        create_invisitors_query = "CREATE TABLE IF NOT EXISTS InVisitors (vid BIGINT,qrid VARCHAR(50),Name VARCHAR(25),PhoneNumber varchar(20),Email VARCHAR(40),PersonToVisit VARCHAR(25),ReasonToVisit VARCHAR(75),InTime varchar(20),foreign key(vid) references Records(vid))"
        create_faculty_query = "CREATE TABLE IF NOT EXISTS Faculty (Name VARCHAR(25),Email varchar(40) not null, PhoneNumber varchar(20) PRIMARY KEY, Department varchar(10) not null)"
        create_table_creds= "CREATE TABLE IF NOT EXISTS LoginCredentials (Username varchar(30) primary key, Password varchar(30) not null, Admin Integer not null default 0)"

        try:
            with connection.cursor() as cursor:
                cursor.execute(create_qravailable_query)
                cursor.execute(create_records_query)
                cursor.execute(create_invisitors_query)
                cursor.execute(create_faculty_query)
                cursor.execute(create_table_creds)
                connection.commit()
                cursor.execute("insert into LoginCredentials values('Admin','123456','1')")
                cursor.execute("insert into Faculty values('Other Reasons','admin@institute.in','0','general')")
                connection.commit()
            self.pool.close_pool()
            return 1
        except Exception as e:
            print(e)
            return 0
        
    def update_error_label(self, message):
        self.error_label.config(text=message)


if __name__=="__main__":
    app=createtables()
    app.mainloop()
