import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Tkinter Application")

        # Variables
        self.db_url = tk.StringVar()

        # Frames
        self.frame1 = ttk.Frame(root)
        self.frame2 = ttk.Frame(root)
        self.frame3 = ttk.Frame(root)

        # Initialize frames
        self.create_frame1()
        self.create_frame2()
        self.create_frame3()

        # Show frame1 initially
        self.show_frame(self.frame1)

    def create_frame1(self):
        label = ttk.Label(self.frame1, text="Enter DB URL:")
        entry = ttk.Entry(self.frame1, textvariable=self.db_url)
        submit_button = ttk.Button(self.frame1, text="Submit", command=self.show_frame2)

        label.pack(pady=10)
        entry.pack(pady=10)
        submit_button.pack(pady=10)

    def create_frame2(self):
        label = ttk.Label(self.frame2, text="Login Page")
        submit_button = ttk.Button(self.frame2, text="Submit", command=self.show_frame3)
        back_button = ttk.Button(self.frame2, text="Back", command=self.show_frame1)

        label.pack(pady=10)
        submit_button.pack(pady=10)
        back_button.pack(pady=10)

    def create_frame3(self):
        notebook = ttk.Notebook(self.frame3)
        
        # Create pages in the notebook
        page1 = ttk.Frame(notebook)
        page2 = ttk.Frame(notebook)
        page3 = ttk.Frame(notebook)
        page4 = ttk.Frame(notebook)

        # Add pages to the notebook
        notebook.add(page1, text="1")
        notebook.add(page2, text="2")
        notebook.add(page3, text="3")
        notebook.add(page4, text="4")

        # Create back button
        back_button = ttk.Button(self.frame3, text="Back", command=self.show_frame2)

        notebook.pack(pady=10)
        back_button.pack(pady=10)

    def show_frame(self, frame):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        frame.pack(fill="both", expand=True)

    def show_frame1(self):
        self.show_frame(self.frame1)

    def show_frame2(self):
        if self.db_url.get():
            self.show_frame(self.frame2)
        else:
            tk.messagebox.showwarning("Warning", "Please enter a DB URL first.")

    def show_frame3(self):
        self.show_frame(self.frame3)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
