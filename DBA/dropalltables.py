import tkinter as tk
import vpcheck as vp


def closeconnection(conn):  # <--------------- put it in class later
    try:
        if conn.closed==0:
            conn.close()
            print("connection closed: \n",str(conn))
    except Exception as e:
        print("Error Closing Connection to database: \n",e)


class createtables(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drop Tables")
        self.minsize(800,400)
        self.connections_dict = {}
        self.geometry_centered(800,400)
        self.configure(bg='#141414')

        self.title_label = tk.Label(self, text="Delete Database", font=("courier new", 45, "bold"), fg="#426ae3", bg="#141414")
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
                    #code here
                    drop_qravailable_query="DROP TABLE IF EXISTS QRavailable"
                    drop_records_query = "DROP TABLE IF EXISTS Records"
                    drop_invisitors_query = "DROP TABLE IF EXISTS InVisitors"
                    drop_faculty_query = "DROP TABLE IF EXISTS faculty"
                    drop_table_creds= "DROP TABLE IF EXISTS creds"
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(drop_table_creds)
                            cursor.execute(drop_faculty_query)
                            cursor.execute(drop_invisitors_query)
                            cursor.execute(drop_records_query)
                            cursor.execute(drop_qravailable_query)
                            connection.commit()
                            self.update_error_label("Dropped all tables: you can now close this window")
                    except Exception as e:
                        print(e)
                    closeconnection(connection)     # <----------- current connection being closed here
                    del self.connections_dict[dburl]

            except Exception as e:
                print(e)

        
    def update_error_label(self, message):
        self.error_label.config(text=message)


if __name__=="__main__":
    app=createtables()
    app.mainloop()
