import json
import tkinter as tk
from tkinter import ttk

class FacultyDataEntryFrame(tk.Frame):
    def __init__(self, master=None, callback=None, faculty_data=None):
        super().__init__(master)
        self.master = master
        self.callback = callback
        self.faculty_data = faculty_data or []
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        # Label for branch combo box
        self.branch_label = ttk.Label(self, text="Branch:")
        self.branch_label.grid(row=0, column=0, padx=10, pady=10)

        # Create StringVars for the filters
        self.branch_var = tk.StringVar()
        self.phno_var = tk.StringVar()

        # Combo box for selecting the branch
        self.branch_combo_box = ttk.Combobox(self, state="readonly", textvariable=self.branch_var)
        self.branch_combo_box.grid(row=0, column=1, padx=10, pady=10)
        branches = set(faculty["dept"] for faculty in self.faculty_data)
        self.branch_combo_box['values'] = [""] + list(branches)  # Add an empty option for no selection
        self.branch_var.trace_add("write", self.update_name_combo_box)  # Attach a callback to update name combo box

        # Label for phone number entry
        self.phno_label = ttk.Label(self, text="Phone Number:")
        self.phno_label.grid(row=0, column=2, padx=10, pady=10)

        # Entry field for entering phone number
        self.phno_entry = ttk.Entry(self, textvariable=self.phno_var)
        self.phno_entry.grid(row=0, column=3, padx=10, pady=10)
        self.phno_var.trace_add("write", self.update_name_combo_box)  # Attach a callback to update name combo box

        # Combo box for selecting the name
        self.name_label = ttk.Label(self, text="Name:")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)

        self.name_combo_box = ttk.Combobox(self, state="readonly")
        self.name_combo_box.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.name_combo_box.bind("<<ComboboxSelected>>", self.on_name_select)  # Attach a callback for selection

        # Show all names by default
        all_names = [faculty["name"] for faculty in self.faculty_data]
        self.name_combo_box['values'] = all_names

    def update_name_combo_box(self, *args):
        # Update the name combo box values based on selected branch and phno
        selected_branch = self.branch_var.get()
        selected_phno = self.phno_var.get()

        if not selected_branch and not selected_phno:
            # If no branch or phno is selected, show all names
            all_names = [faculty["name"] for faculty in self.faculty_data]
            self.name_combo_box['values'] = all_names
        else:
            # Filter names based on selected branch and phno
            filtered_names = [faculty["name"] for faculty in self.faculty_data
                              if (not selected_branch or faculty["dept"] == selected_branch) and
                              (not selected_phno or faculty["phno"] == selected_phno)]

            self.name_combo_box['values'] = filtered_names

    def on_name_select(self, event):
        # Store the selected value in a variable or perform any desired action
        selected_value = self.name_combo_box.get()
        print(f"Selected Name: {selected_value}")
        # Pass the selected value to the callback function
        if self.callback:
            self.callback(selected_value)

def read_faculty_data_from_json(file_path):
    with open(file_path, 'r') as file:
        faculty_data = json.load(file)
    return faculty_data

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create the main window
        self.title("Main Application")

        # Button to open Faculty Data Entry Frame
        self.open_frame_button = ttk.Button(self, text="Open Faculty Data Entry", command=self.open_faculty_frame)
        self.open_frame_button.pack(pady=20)

    def open_faculty_frame(self):
        # Read faculty data from JSON file
        faculty_data = read_faculty_data_from_json("json_data.json")

        # Open the Faculty Data Entry Frame in a pop-up dialog
        faculty_frame = tk.Toplevel(self)
        faculty_frame.title("Faculty Data Entry")
        
        # Define a callback function to receive the selected value
        def callback(selected_value):
            print(f"Selected Value in Main Window: {selected_value}")
        
        faculty_data_entry = FacultyDataEntryFrame(faculty_frame, callback, faculty_data)

# Run the Tkinter main loop
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
