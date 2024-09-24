import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from parser import diccionary_health_content
from tkinter import PhotoImage  # Asegúrate de importar PhotoImage
from PIL import Image, ImageTk  # Importa las clases necesarias de Pillow

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

    def create_rounded_button(self, parent, text, command, row, column, label_text="", image_path=None):
        # Create a frame to simulate rounded corners
        button_frame = tk.Frame(parent, bg="white", padx=5, pady=5)

        # Create a button inside the frame with a fixed width and increased width
        button = ttk.Button(button_frame, text=text, command=command, style="Rounded.TButton", width=40)

        # Load the image if image_path is provided
        if image_path:
            img = Image.open(image_path)  # Open the image file
            img = img.resize((30, 30), Image.LANCZOS)  # Adjust the image size
            photo = ImageTk.PhotoImage(img)  # Image to PhotoImage
            button.config(image=photo, compound=tk.TOP)  # Set image above text
            button.image = photo  # Keep a reference to avoid garbage collection

        button.pack(padx=10, pady=(10, 0))  # Padding to create space above the label

        # Create a label below the button if label_text is provided
        if label_text:
            label = tk.Label(button_frame, text=label_text, bg="white", fg="black", font=("Source Sans 3", 9))
            label.pack(pady=(5, 0))  # Padding to create space above the label

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
        self.create_rounded_button(button_frame, "List of Diseases and Procedures", self.show_topic_list, 0, 0, "Find info about different medical topics", "images_gui/1.jpg")
        self.create_rounded_button(button_frame, "Health Organizations", self.accion_boton_2, 0, 1, "Catalog with different medical organizations", "images_gui/2.jpg")
        self.create_rounded_button(button_frame, "Basic Information about Dataset", self.accion_boton_3, 0, 2, "Amount of health topics, date, and time of generation of the XML file", "images_gui/3.jpg")

        # Create additional buttons in a new row
        self.create_rounded_button(button_frame, "Other languages for data", self.accion_boton_4, 1, 0, "Articles in different languages", "images_gui/4.jpg")
        self.create_rounded_button(button_frame, "Find extra information about a topic", self.accion_boton_5, 1, 1, "Relevant information about various health articles", "images_gui/5.jpg")
        self.create_rounded_button(button_frame, "Data graphs", self.accion_boton_6, 1, 2, "Graphs about medical data", "images_gui/6.jpg")

    def show_topic_list(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        also_called_list = []
        topic_ids = []

        for topic_id, topic_data in diccionary_health_content.items():
            for entry in topic_data:
                elements = entry[6]
                if 'also_called' in elements:
                    for also_called in elements['also_called']:
                        also_called_list.append(also_called)
                        topic_ids.append(topic_id)

        if also_called_list:
            for index, term in enumerate(also_called_list):
                button = ttk.Button(self.main_frame, text=term, command=lambda idx=index: self.show_topic_details(topic_ids[idx]), style="Rounded.TButton")
                button.pack(pady=5)

            back_button = ttk.Button(self.main_frame, text="Go back", command=self.create_main_screen, style="Rounded.TButton")
            back_button.pack(pady=20)
        else:
            messagebox.showinfo("Information", "No names in 'also_called' available.")
            self.create_main_screen()

    def show_topic_details(self, topic_id):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if topic_id in diccionary_health_content:
            topic_data = diccionary_health_content[topic_id]
            details = ""
            sites = []

            for entry in topic_data:
                description, title, url, id, language, date, elements = entry
                details += f"Topic Information\n"
                details += f"Title: {title}, ID: {id}\n"
                details += f"Description: {description}\n"
                details += f"Language: {language}\n"
                details += f"Date: {date}\n"
                
                url_label = tk.Label(self.main_frame, text=url, fg="blue", cursor="hand2", bg=self.main_frame.cget("bg"))
                url_label.pack(pady=5)
                url_label.bind("<Button-1>", lambda e: self.open_url(url))

                if 'full_summary' in elements:
                    details += f"Summary: {' '.join(elements['full_summary'])}\n"
                if 'site' in elements:
                    sites.extend(elements['site'])

            details_text = tk.Text(self.main_frame, wrap=tk.WORD, bg=self.main_frame.cget("bg"), borderwidth=0)
            details_text.insert(tk.END, details)
            details_text.configure(state='disabled')
            details_text.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

            new_view_button = ttk.Button(self.main_frame, text="Find extra info about this topic", command=lambda: self.show_topic_sites(sites), style="Rounded.TButton")
            new_view_button.pack(pady=10)

            back_button = ttk.Button(self.main_frame, text="Go back", command=self.create_main_screen, style="Rounded.TButton")
            back_button.pack(pady=20)

    def show_topic_sites(self, sites):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.main_frame, text="Click here to see related articles from this topic:", font=("Arial", 14), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=20)

        if sites:
            for site in sites:
                site_label = tk.Label(self.main_frame, text=site, bg=self.main_frame.cget("bg"), fg="blue", cursor="hand2")
                site_label.pack(pady=5)
                site_label.bind("<Button-1>", lambda e, url=site: self.open_url(url))

        back_button = ttk.Button(self.main_frame, text="Go Back", command=self.create_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20)

    def show_topic_sites(self, sites):
        # Hide the search and top frame
        self.search_frame.pack_forget()
        self.top_frame.pack_forget()

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.main_frame, text="Click here to see related articles from this topic:", font=("Arial", 14), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=20)

        if sites:
            for site in sites:
                site_label = tk.Label(self.main_frame, text=site, bg=self.main_frame.cget("bg"), fg="blue", cursor="hand2")
                site_label.pack(pady=5)
                site_label.bind("<Button-1>", lambda e, url=site: self.open_url(url))

        back_button = ttk.Button(self.main_frame, text="Go Back", command=self.create_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20)

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def search(self):
        query = self.entry.get()
        print(f"Searching for: {query}")

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

# TO DO: 
# - Buscar manera de insertar una barra para hacer scroll en las ventanas
# - Hacer que todos los botones del nombre de los topics sean del mismo tamaño y ordenarlos alfabéticamente
# - Modificar la función show_topic_site para que muestre bien los datos
# - Agregar las demás funciones de los botones