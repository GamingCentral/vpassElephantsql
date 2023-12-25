import tkinter as tk

class YourApp:
    def __init__(self, master):
        self.signup = tk.Frame(master)
        self.signup.pack()

        self.exit_label = tk.Label(self.signup, text="Register User", font=("courier new bold", 35), fg="#426ae3", bg="#ebedf0")
        self.exit_label.pack(pady=35)

        self.username_label_signup = tk.Label(self.signup, text="UserName", font=("bookman old style", 15), fg="#0a0a0a", bg="#ebedf0")
        self.username_label_signup.pack()
        self.username_entry_signup = tk.Entry(self.signup, width=72, font=("gothic", 13), bg="white", fg="black")
        self.username_entry_signup.pack(pady=5)

        self.password_label_signup = tk.Label(self.signup, text="Password", font=("bookman old style", 15), fg="#0a0a0a", bg="#ebedf0")
        self.password_label_signup.pack()
        self.password_entry_signup = tk.Entry(self.signup, width=72, font=("Helvetica", 12), bg="white", fg="black")
        self.password_entry_signup.pack(pady=5)

        ##########################################################################
        self.admin_var = tk.IntVar()  # Variable to store the state of the checkbox

        self.admin_checkbox = tk.Checkbutton(self.signup, text="Admin", variable=self.admin_var, font=("bookman old style", 15), fg="#0a0a0a", bg="#ebedf0")
        self.admin_checkbox.pack()

        self.submit_button = tk.Button(self.signup, width=20, command=self.submit_press_signup, text="Submit", font=("courier new bold", 15), bg="#426ae3", fg="black")
        self.submit_button.pack(pady=30)

        self.error_label_signup = tk.Label(self.signup, text='this is error', font=("bookman old style", 12), fg="red", bg='#ebedf0')
        self.error_label_signup.pack()

    def submit_press_signup(self):
        # Get values from the entries
        username = self.username_entry_signup.get()
        password = self.password_entry_signup.get()
        admin_value = self.admin_var.get()  # 1 if checked, 0 if unchecked

        # Use the values as needed (e.g., send to backend)
        print("Username:", username)
        print("Password:", password)
        print("Admin:", admin_value)

if __name__ == "__main__":
    root = tk.Tk()
    app = YourApp(root)
    root.mainloop()
