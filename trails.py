import tkinter as tk


def login():
    # Replace this function with your authentication logic
    username = username_entry.get()
    password = password_entry.get()
    database_url = database_url_entry.get()
    print("Database URL:", database_url)
    print("Username:", username)
    print("Password:", password)

# Create the main window
root = tk.Tk()
root.title("Dark Theme Login")
root.geometry("600x350")  # Slightly increased height to accommodate the extra field

root.configure(bg="#141414")

# Create a label for the login page title
title_label = tk.Label(root, text="Login", font=("Helvetica", 24, "bold"), fg="#426ae3", bg="#141414")
title_label.pack(pady=20)

# Create the database URL entry field
database_url_label = tk.Label(root, text="Database URL", font=("Helvetica", 12), fg="gray", bg="#141414")
database_url_label.pack()
database_url_entry = tk.Entry(root, font=("Helvetica", 12), bg="white", fg="black")
database_url_entry.pack(pady=5)

# Create the username entry field
username_label = tk.Label(root, text="Username", font=("Helvetica", 12), fg="gray", bg="#141414")
username_label.pack()
username_entry = tk.Entry(root, font=("Helvetica", 12), bg="white", fg="#141414")
username_entry.pack(pady=5)

# Create the password entry field
password_label = tk.Label(root, text="Password", font=("Helvetica", 12), fg="gray", bg="#141414")
password_label.pack()
password_entry = tk.Entry(root, font=("Helvetica", 12), show="*", bg="white", fg="#141414")
password_entry.pack(pady=5)

# Create the login button
login_button = tk.Button(root, text="Submit", font=("Helvetica", 14), bg="#426ae3", fg="#141414", command=login)
login_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
