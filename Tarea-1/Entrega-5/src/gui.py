import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from parser import diccionary_health_content
from tkinter import PhotoImage
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MedicalDictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Dictionary")
        self.root.geometry('1200x600')

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
        self.create_rounded_button(button_frame, "Health Organizations", self.show_primary_institutes, 0, 1, "Catalog with different medical organizations", "images_gui/2.jpg")
        self.create_rounded_button(button_frame, "Basic Information about Dataset", self.accion_boton_3, 0, 2, "Amount of health topics, date, and time of generation of the XML file", "images_gui/3.jpg")

        # Create additional buttons in a new row
        self.create_rounded_button(button_frame, "Other languages for data", self.show_language_mapped_topics, 1, 0, "Articles in different languages", "images_gui/4.jpg")
        self.create_rounded_button(button_frame, "Find extra information about a topic", self.accion_boton_5, 1, 1, "Relevant information about various health articles", "images_gui/5.jpg")
        self.create_rounded_button(button_frame, "Data graphs", self.graph_data_window, 1, 2, "Graphs about medical data", "images_gui/6.jpg")

    def show_topic_list(self):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()

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
            # Sort the terms alphabetically
            sorted_terms = sorted(zip(also_called_list, topic_ids), key=lambda x: x[0])

            # Create a scrollable frame using the new method
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            # Make scrollable_frame fill the entire area and center content
            scrollable_frame.pack(expand=True, fill='both')

            # Create a frame for centering buttons
            button_frame = ttk.Frame(scrollable_frame)
            button_frame.pack(anchor='center')  # Center the frame within the scrollable area

            for term, topic_id in sorted_terms:
                button = ttk.Button(button_frame, text=term, command=lambda id=topic_id: self.show_topic_details(id), style="Rounded.TButton", width=40)  # Fixed width
                button.pack(pady=5, anchor='center')  # Center each button

            back_button = ttk.Button(button_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='center')  # Center the back button
        else:
            messagebox.showinfo("Information", "No names in 'also_called' available.")
            self.create_main_screen()

    def show_topic_details(self, topic_id):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()
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
                
                # Display URL as a clickable link, centered
                url_label = tk.Label(self.main_frame, text=url, fg="blue", cursor="hand2", bg=self.main_frame.cget("bg"))
                url_label.pack(pady=5, anchor='center')  # Center the URL
                url_label.bind("<Button-1>", lambda e: self.open_url(url))

                if 'full_summary' in elements:
                    details += f"Summary: {' '.join(elements['full_summary'])}\n"
                if 'site' in elements:
                    sites.extend(elements['site'])

            # Create a scrollable frame for details
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            # Make sure the scrollable frame expands and is centered
            scrollable_frame.pack(expand=True, fill='both')

            # Center the details text
            details_text = tk.Text(scrollable_frame, wrap=tk.WORD, bg=self.main_frame.cget("bg"), borderwidth=0)
            details_text.insert(tk.END, details)
            details_text.configure(state='disabled')
            details_text.pack(pady=20, padx=10, fill=tk.BOTH, expand=True, anchor='center')  # Center the text box

            # Center the button to find extra info
            new_view_button = ttk.Button(scrollable_frame, text="Find extra info about this topic", command=lambda: self.show_topic_sites(sites), style="Rounded.TButton")
            new_view_button.pack(pady=10, anchor='center')

            # Center the "Go back" button
            back_button = ttk.Button(scrollable_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
            back_button.pack(pady=20, anchor='center')

    def show_topic_sites(self, sites):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title label for the entire section, centered
        title_label = tk.Label(self.main_frame, text="Related articles from this topic:", font=("Montserrat", 14), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=20, anchor='center')

        # Create a scrollable frame for sites
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Frame to hold content centrally
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.grid_columnconfigure(0, weight=1)  # Center column

        # Ensure content_frame is centered within the scrollable_frame
        content_frame.pack(expand=True, padx=20, pady=20)

        if sites:
            for site in sites:
                # Display the title in larger font, centered
                title = site.get('title', 'No Title')
                title_label = tk.Label(content_frame, text=title, font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                title_label.grid(pady=(10, 5), sticky="ew")  # Expand across center

                # Display the URL as a clickable link, centered
                url = site.get('url', '#')
                url_label = tk.Label(content_frame, text=url, bg=self.main_frame.cget("bg"), fg="blue", cursor="hand2")
                url_label.grid(pady=5, sticky="ew")
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

                # Display other content like information, organization, and standard content, centered
                information_content = site.get('information_content', [])
                if information_content:
                    info_label = tk.Label(content_frame, text="Info: " + ", ".join(information_content), bg=self.main_frame.cget("bg"))
                    info_label.grid(pady=5, sticky="ew")

                organization_content = site.get('organization_content', [])
                if organization_content:
                    org_label = tk.Label(content_frame, text="Organization: " + ", ".join(organization_content), bg=self.main_frame.cget("bg"))
                    org_label.grid(pady=5, sticky="ew")

                standard_content = site.get('standard_content', [])
                if standard_content:
                    std_label = tk.Label(content_frame, text="Standard: " + ", ".join(standard_content), bg=self.main_frame.cget("bg"))
                    std_label.grid(pady=5, sticky="ew")

                # Optional: Handle language_site_url (for multilingual support), centered
                language_site_url = site.get('language_site_url', None)
                if language_site_url:
                    lang_url_label = tk.Label(content_frame, text=language_site_url, bg=self.main_frame.cget("bg"), fg="blue", cursor="hand2")
                    lang_url_label.grid(pady=5, sticky="ew")
                    lang_url_label.bind("<Button-1>", lambda e, link=language_site_url: self.open_url(link))

        # Center the Go Back button at the bottom
        back_button = ttk.Button(content_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.grid(pady=20, sticky="ew")

    def show_primary_institutes(self):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        topic_ids = []
        urls = []  # Store URLs
        texts = []  # Store institute names

        # Loop through the dictionary to extract primary institute content
        for topic_id, topic_data in diccionary_health_content.items():
            for entry in topic_data:
                elements = entry[6]
                if 'primary_institute' in elements:
                    for primary_institute in elements['primary_institute']:
                        # Extract 'text' (institute name) and 'url'
                        texts.append(primary_institute['text'])
                        urls.append(primary_institute['url'])
                        topic_ids.append(topic_id)

        if texts:
            # Sort the institutes alphabetically along with their URLs and topic IDs
            sorted_terms = sorted(zip(texts, urls, topic_ids), key=lambda x: x[0])

            # Create a scrollable frame using the new method
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            # Make scrollable_frame fill the entire area and center content
            scrollable_frame.pack(expand=True, fill='both')

            # Create a frame for centering buttons
            button_frame = ttk.Frame(scrollable_frame)
            button_frame.pack(anchor='center')  # Center the frame within the scrollable area

            for term, url, topic_id in sorted_terms:
                # Create a button for each primary institute
                button = ttk.Button(button_frame, text=term, command=lambda id=topic_id: self.show_topic_details(id), style="Rounded.TButton", width=40)  # Fixed width
                button.pack(pady=5, anchor='center')  # Center each button

                # Display the URL as a clickable label below each button
                url_label = tk.Label(button_frame, text=url, fg="blue", cursor="hand2", bg=self.main_frame.cget("bg"))
                url_label.pack(anchor='center')  # Center the URL
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

            # Go back button at the bottom
            back_button = ttk.Button(button_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='center')  # Center the back button
        else:
            messagebox.showinfo("Information", "No primary institutes available.")
            self.create_main_screen()

    def show_language_mapped_topics(self):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        languages = []
        topic_ids = []
        urls = []  # Store URLs
        texts = []  # Store language names

        # Loop through the dictionary to extract language_mapped_topic_content
        for topic_id, topic_data in diccionary_health_content.items():
            for entry in topic_data:
                elements = entry[6]
                if 'language_mapped_topic' in elements:
                    for language_mapped_topic in elements['language_mapped_topic']:
                        # Extract 'text' (language name) and 'url'
                        texts.append(language_mapped_topic['text'])
                        urls.append(language_mapped_topic['url'])
                        topic_ids.append(topic_id)

        if texts:
            # Sort the languages alphabetically along with their URLs and topic IDs
            sorted_terms = sorted(zip(texts, urls, topic_ids), key=lambda x: x[0])

            # Create a scrollable frame using the new method
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            # Make scrollable_frame fill the entire area and center content
            scrollable_frame.pack(expand=True, fill='both')

            # Create a frame for centering buttons
            button_frame = ttk.Frame(scrollable_frame)
            button_frame.pack(anchor='center')  # Center the frame within the scrollable area

            for term, url, topic_id in sorted_terms:
                # Create a button for each language-mapped topic
                button = ttk.Button(button_frame, text=term, command=lambda id=topic_id: self.show_topic_details(id), style="Rounded.TButton", width=40)  # Fixed width
                button.pack(pady=5, anchor='center')  # Center each button

                # Display the URL as a clickable label below each button
                url_label = tk.Label(button_frame, text=url, fg="blue", cursor="hand2", bg=self.main_frame.cget("bg"))
                url_label.pack(anchor='center')  # Center the URL
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

            # Go back button at the bottom
            back_button = ttk.Button(button_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='center')  # Center the back button
        else:
            messagebox.showinfo("Information", "No language-mapped topics available.")
            self.create_main_screen()

    def return_to_main_screen(self):
        # Clear the current main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create top frame for the search area
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        self.search_frame.pack(pady=20)

        # Create a frame for the main screen
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_main_screen()  # Call to recreate buttons or any additional UI
    def graph_data_window(self):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title label for the entire section, centered
        title_label = tk.Label(self.main_frame, text="Graphs", font=("Montserrat", 14), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=20, anchor='center')

        # Create a scrollable frame for sites
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Frame to hold content centrally
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.grid_columnconfigure(0, weight=1)  # Allow column to expand

        # Create buttons for graph options
        graph_button_1 = ttk.Button(content_frame, text="Graph 1", command=self.graph_data_1, style="Rounded.TButton")
        graph_button_1.grid(row=0, column=0, pady=10, padx=20, sticky="ew")  # Add padx for spacing

        graph_button_2 = ttk.Button(content_frame, text="Graph 2", command=self.graph_data_2, style="Rounded.TButton")
        graph_button_2.grid(row=1, column=0, pady=10, padx=20, sticky="ew")  # Add padx for spacing

        # Pack the content_frame to ensure it's visible
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)  # Center and fill

        # Center content_frame within the scrollable_frame
        scrollable_frame.pack(expand=True, fill=tk.BOTH)

        # Center the "Go back" button
        back_button = ttk.Button(scrollable_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, anchor='center')

    def graph_data_1(self):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create a scrollable frame
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Frame to hold content centrally
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.grid_columnconfigure(0, weight=1)  # Center column

        # Ensure content_frame is centered within the scrollable_frame
        content_frame.pack(expand=True, padx=20, pady=20)

        # Extract data for sites by topic
        data = []
        for topic_id, topic_info in diccionary_health_content.items():
            # Access the first tuple in the list
            description, title, url, id, language, date, elements = topic_info[0]

            # Get the number of sites
            num_sites = len(elements.get('site', [])) if isinstance(elements, dict) else 0
            
            data.append({'Title': title, 'Num_Sites': num_sites})

        # Convert to DataFrame for ease of use
        df = pd.DataFrame(data)

        # Sort the DataFrame by number of sites
        df = df.sort_values(by='Num_Sites', ascending=False)

        # Create a Figure for the plot
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Create the bar chart
        ax.bar(df['Title'], df['Num_Sites'], color='skyblue')
        ax.set_xlabel('Health Topics')
        ax.set_ylabel('Number of Sites')
        ax.set_title('Health Topics with Most Sites')

        # Set ticks and labels
        ax.set_xticks(range(len(df['Title'])))
        ax.set_xticklabels(df['Title'], rotation=45, ha='right')

        # Display the plot
        canvas = FigureCanvasTkAgg(fig, master=content_frame)  # Create a canvas for the plot
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Center the Go Back button at the bottom
        back_button = ttk.Button(content_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, fill='x')  # Use pack for the back button

    def graph_data_2(self):
        # Hide the top frame and search bar
        self.top_frame.pack_forget()
        self.search_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create a scrollable frame
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Frame to hold content centrally
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.grid_columnconfigure(0, weight=1)  # Center column

        # Ensure content_frame is centered within the scrollable_frame
        content_frame.pack(expand=True, padx=20, pady=20)

        # Extract languages
        languages = []
        for topic_info in diccionary_health_content.values():
            # Access the first tuple in the list
            _, _, _, _, language, _, _ = topic_info[0]
            languages.append(language)

        # Count the frequency of each language
        language_counts = Counter(languages)

        # Create a DataFrame with the data
        df_lang = pd.DataFrame(language_counts.items(), columns=['Language', 'Count'])

        # Create a Figure for the plot
        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(111)

        # Create the bar chart for language frequencies
        ax.bar(df_lang['Language'], df_lang['Count'], color='lightgreen')
        ax.set_xlabel('Languages')
        ax.set_ylabel('Frequency')
        ax.set_title('Most Frequent Languages in Health Topics')

        # Set ticks and labels
        ax.set_xticks(range(len(df_lang['Language'])))
        ax.set_xticklabels(df_lang['Language'], rotation=45)

        # Display the plot
        canvas = FigureCanvasTkAgg(fig, master=content_frame)  # Create a canvas for the plot
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Center the Go Back button at the bottom
        back_button = ttk.Button(content_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, fill='x')  # Use pack for the back button
        
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def search(self):
        query = self.entry.get()
        print(f"Searching for: {query}")

    def accion_boton_3(self):
        from parser import health_TOPICS_DATA_GENERATION_XLL
        info_string = ("Total Health Topics: " + health_TOPICS_DATA_GENERATION_XLL[0] + '\n'
        + "Date Generated: " + health_TOPICS_DATA_GENERATION_XLL[1] + '\n' + "Time Generated: "
        + health_TOPICS_DATA_GENERATION_XLL[2])
        messagebox.showinfo("Dataset Information",  message=info_string)

    def accion_boton_5(self):
        messagebox.showinfo("Button 5 Clicked", "Action for Find extra information about a topic")

    def create_scrollable_frame(self, parent):
        # Create a canvas
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return canvas, scrollable_frame

def init_gui():
    root = tk.Tk()
    app = MedicalDictionaryApp(root)
    root.mainloop()

# TO DO: 
# - Centrar bien los botones de sites
# - Agregar las demás funciones de los botones (basic info, extra info)
# - Agregar la funcionalidad de búsqueda
# - Cambiar el formato de los botones y datos de language_mapped_topics y primary_institutes para que se vea mejor
# - Revisar porque despues de un Go Back, el frame de search aparece abajo del frame de los botones
# - Revisar si se puede establecer un tamaño de inicio de la pantalla
# - Crear mas graficos para la opcion de Data graphs