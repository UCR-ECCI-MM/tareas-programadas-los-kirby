import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from parser import diccionary_health_content

class MedicalDictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Dictionary")
        self.root.geometry('600x400')

        # Background color
        self.bg_color = "#F7F6F6"
        self.root.configure(bg=self.bg_color)

        # Button style
        style = ttk.Style()
        style.configure("Rounded.TButton",  background="white", borderwidth=0, relief="flat", padding=10, font=("Montserrat", 11, "bold"))
        style.map("Rounded.TButton", background=[("active", "white")])  # Active color

        # Create top frame for the search area
        self.top_frame = tk.Frame(self.root, bg="#232323", height=150)
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the main screen
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the main screen
        self.create_main_screen()

    def create_rounded_button(self, parent, text, command, row, column, label_text=""):
        # Create a frame to simulate rounded corners
        button_frame = tk.Frame(parent, bg="white", padx=5, pady=5)

        # Create a button inside the frame with a fixed width and increased width
        button = ttk.Button(button_frame, text=text, command=command, style="Rounded.TButton", width=30)
        button.pack(padx=10, pady=(10, 0))  # Padding to create space above the label

        # Create a label below the button
        if label_text:
            label = tk.Label(button_frame, text=label_text, bg="white", fg="black", font=("Source Sans 3", 9), wraplength=150)
            label.pack(pady=(5, 0))  # Padding to create space below the button

        # Use grid for the button frame and make it sticky to fill the space
        button_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

    def create_main_screen(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Check if the search frame already exists
        if not hasattr(self, 'search_frame'):
            # Create a frame for the search bar and button
            self.search_frame = tk.Frame(self.top_frame, bg="#232323")
            self.search_frame.pack(pady=20)

            # Title above the search bar
            title_label = tk.Label(self.search_frame, text="Search for symptoms, diseases and procedures", bg="#232323", fg="white", font=("Montserrat", 14, "bold"))
            title_label.pack(pady=(0, 10))

            # Search entry field in the search frame
            self.entry = tk.Entry(self.search_frame, width=40)
            self.entry.pack(side=tk.LEFT, padx=(0, 10))

            search_button = ttk.Button(self.search_frame, text="Search", command=self.search, style="Rounded.TButton", width=11, padding=(6, 0))
            search_button.pack(side=tk.LEFT)
        else:
            self.search_frame.pack(pady=20)

        # Create buttons in the bottom frame
        button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)

        # Configure grid rows and columns to have equal weight and height
        for i in range(3):  # Assuming 3 columns
            button_frame.grid_columnconfigure(i, weight=1, uniform="group1")

        # Create rounded buttons with grid positions and corresponding labels
        self.create_rounded_button(button_frame, "List of Diseases and Procedures", self.accion_boton_1, 0, 0, "Find info about different medical topics")
        self.create_rounded_button(button_frame, "Health Organizations", self.accion_boton_2, 0, 1, "Catalog with different medical organizations")
        self.create_rounded_button(button_frame, "Basic Information about Dataset", self.accion_boton_3, 0, 2, "Amount of health topics, date, and time of generation of the XML file")

        # Create additional buttons in a new row
        self.create_rounded_button(button_frame, "Other languages for data", self.accion_boton_4, 1, 0, "Articles in different languages")
        self.create_rounded_button(button_frame, "Extra information about a topic", self.accion_boton_5, 1, 1, "Relevant information about various health articles")
        self.create_rounded_button(button_frame, "Data graphs", self.accion_boton_6, 1, 2, "Graphs about medical data")

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def search(self):
        query = self.entry.get()
        print(f"Searching for: {query}")

    def accion_boton_1(self):
        messagebox.showinfo("Button 1 Clicked", "Action for List of Diseases and Procedures")

    def accion_boton_2(self):
        messagebox.showinfo("Button 2 Clicked", "Action for Health Organizations")

    def accion_boton_3(self):
        messagebox.showinfo("Button 3 Clicked", "Action for Basic Information about Dataset")

    def accion_boton_4(self):
        messagebox.showinfo("Button 4 Clicked", "Action for Other languages for data")

    def accion_boton_5(self):
        messagebox.showinfo("Button 5 Clicked", "Action for Find extra information about a topic")

    def accion_boton_6(self):
        messagebox.showinfo("Button 6 Clicked", "Action for Data graphs")

def init_gui():
    root = tk.Tk()
    app = MedicalDictionaryApp(root)
    root.mainloop()

def main():
    init_gui()