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
import warnings
warnings.filterwarnings("ignore") # To ignore not found characters in titles of graphs

class MedicalDictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Dictionary")
        self.root.geometry('1980x1080')

        # Background color
        self.bg_color = "#F7F6F6"
        self.root.configure(bg=self.bg_color)

        # Button style
        style = ttk.Style()
        style.configure("Rounded.TButton",  background="white", borderwidth=0, relief="flat", padding=10, font=("Montserrat", 11, "bold"))
        style.map("Rounded.TButton", background=[("active", "white")])  # Active color

        # Create the top frame
        self.top_frame = tk.Frame(self.root, bg="#232323")
        self.top_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))

        # Create the search frame if it doesn't exist
        self.create_search_frame()

        self.current_page_list = 0
        self.items_per_page_list = 30

        self.current_page_sites = 0
        self.items_per_page_sites = 30

        self.current_page_organizations = 0
        self.items_per_page_organizations = 30

        self.current_page_languages = 0
        self.items_per_page_languages = 30

        self.current_page_search = 0
        self.items_per_page_search = 30

        # Create a frame for the main screen
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the main screen
        self.create_main_screen()

    def clear_top_frame(self):
        if hasattr(self, 'top_frame'):
            for widget in self.top_frame.winfo_children():
                widget.destroy()

    def create_rounded_button(self, parent, text, command, row, column, label_text="", image_path=None):
        # Create a frame to simulate rounded corners
        button_frame = tk.Frame(parent, bg="white", padx=5, pady=5)

        # Create a button inside the frame with a fixed width and reduced height
        button = ttk.Button(button_frame, text=text, command=command, style="Rounded.TButton", width=30)  # Ajustar el ancho

        # Load the image if image_path is provided
        if image_path:
            img = Image.open(image_path)  # Open the image file
            img = img.resize((40, 40), Image.LANCZOS)  # Ajustar el tamaño de la imagen
            photo = ImageTk.PhotoImage(img)  # Convertir a PhotoImage
            button.config(image=photo, compound=tk.TOP)  # Establecer imagen encima del texto
            button.image = photo  # Mantener una referencia para evitar la recolección de basura

        button.pack(padx=5, pady=(5, 0), fill=tk.BOTH, expand=True)  # Relleno y expansión ajustados

        # Create a label below the button if label_text is provided
        if label_text:
            label = tk.Label(button_frame, text=label_text, bg="white", fg="black", font=("Source Sans 3", 12))  # Ajustar el tamaño de la fuente
            label.pack(pady=(5, 0))  # Relleno para crear espacio sobre la etiqueta

        # Use grid for the button frame and make it sticky to fill the space
        button_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        # Configure row and column to expand
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(column, weight=1)

    def create_main_screen(self):
        # If top frame is not visible, show it at the top of the screen
        if not hasattr(self, 'top_frame'):
            self.top_frame = tk.Frame(self.root, bg="#232323")
            self.top_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))

        # Verifies if the search frame exists
        if not hasattr(self, 'search_frame'):
            self.create_search_frame()  # Create it if it doesn't exist
        else:
            self.search_frame.pack(pady=20)  # Show the search frame if it exists

        # Create buttons in the bottom frame
        button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)

        # Configure grid rows and columns to have equal weight and height
        for i in range(3):  # Assuming 3 columns
            button_frame.grid_columnconfigure(i, weight=1, uniform="group1")

        # Create rounded buttons with grid positions and corresponding labels
        self.create_rounded_button(button_frame, "List of Diseases and Procedures", self.show_topic_list, 0, 0, "Find info about different medical topics", "images_gui/1.jpg")
        self.create_rounded_button(button_frame, "Health Organizations", self.show_primary_institutes, 0, 1, "Catalog with different medical organizations", "images_gui/2.jpg")
        self.create_rounded_button(button_frame, "Basic Information about Dataset", self.show_data_set_contents, 0, 2, "Amount of health topics, date, and time of generation of the XML file", "images_gui/3.jpg")

        # Create additional buttons in a new row
        self.create_rounded_button(button_frame, "Other languages for data", self.show_language_mapped_topics, 1, 0, "Articles in different languages", "images_gui/4.jpg")
        self.create_rounded_button(button_frame, "Find extra information about a topic", self.show_sites, 1, 1, "Relevant information about various health articles", "images_gui/5.jpg")
        self.create_rounded_button(button_frame, "Data graphs", self.graph_data_window, 1, 2, "Graphs about medical data", "images_gui/6.jpg")

    def show_topic_list(self):
        self.clear_top_frame()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.top_frame, text="List of all topics", font=("Montserrat", 20, "bold"), fg="white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=20, anchor='w')

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
            total_terms = len(sorted_terms)

            # Create a scrollable frame
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            # Create a frame for left-aligned buttons
            button_frame = ttk.Frame(scrollable_frame)
            button_frame.pack(fill='x')

            # Calculate the items to show for the current page
            start_index = self.current_page_list * self.items_per_page_list
            end_index = min(start_index + self.items_per_page_list, total_terms)

            for index in range(start_index, end_index):
                term, topic_id = sorted_terms[index]
                button_text = f"{index + 1}. {term}"
                button = ttk.Button(button_frame, text=button_text, command=lambda id=topic_id: self.show_topic_details(id), style="Rounded.TButton", width=40)
                button.pack(pady=5, anchor='w')

            # Back button
            back_button = ttk.Button(button_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)
            back_button.pack(pady=20, anchor='w')

            # Pagination buttons
            if self.current_page_list > 0:
                prev_button = ttk.Button(button_frame, text="Previous", command=lambda: self.change_page_list(-1), style="Rounded.TButton")
                prev_button.pack(pady=5, anchor='w')
            if end_index < total_terms:
                next_button = ttk.Button(button_frame, text="Next", command=lambda: self.change_page_list(1), style="Rounded.TButton")
                next_button.pack(pady=5, anchor='w')
        else:
            messagebox.showinfo("Information", "No topics available.")
            self.create_main_screen()

    def change_page_list(self, direction):
        # Update current page and refresh the topic list
        self.current_page_list += direction
        self.show_topic_list()

    def change_page_sites(self, direction):
        # Update current page and refresh the site list
        self.current_page_sites += direction
        self.show_sites()

    def change_page_organizations(self, direction):
        # Update current page and refresh the organization list
        self.current_page_organizations += direction
        self.show_primary_institutes()

    def change_page_languages(self, direction):
        # Update current page and refresh the language list
        self.current_page_languages += direction
        self.show_language_mapped_topics()
    
    def change_page_search(self, direction):
        # Update current page and refresh the search results
        self.current_page_search += direction
        self.search_topics()

    def show_topic_details(self, topic_id):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title label for the entire section, centered
        title_label = tk.Label(self.top_frame, text="Summary", font=("Montserrat", 20, "bold"), fg="white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=20, anchor='center')

        if topic_id in diccionary_health_content:
            topic_data = diccionary_health_content[topic_id]
            details = ""
            sites = []

            for entry in topic_data:
                description, title, url, id, language, date, elements = entry
                details += f"•Topic Information\n"
                details += f"•Title: {title}\n"
                details += f"•ID: {id}\n"
                details += f"•Description: {description}\n"
                details += f"•Language: {language}\n"
                details += f"•Date: {date}\n"
                
                # Display URL as a clickable link, centered
                url_label = tk.Label(self.main_frame, text="Main site URL: " + url, fg="blue", cursor="hand2", bg=self.main_frame.cget("bg"))
                url_label.pack(pady=5, anchor='center')  # Center the URL
                url_label.bind("<Button-1>", lambda e: self.open_url(url))

                if 'full_summary' in elements:
                    details += f"•Summary: {' '.join(elements['full_summary'])}\n"
                if 'site' in elements:
                    sites.extend(elements['site'])

            # Create a scrollable frame for details
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)
            scrollable_frame.pack(expand=True, fill=tk.BOTH)
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

    def show_sites(self):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.top_frame, text="All available sites", font=("Montserrat", 20, "bold"), fg="white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=20, anchor='w')

        info_label = tk.Label(self.top_frame, text="Only shows 1 site per topic", font=("Montserrat", 12, "bold"), fg="white", bg=self.top_frame.cget("bg"))
        info_label.pack(pady=5, anchor='w')

        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Extract all sites from the dictionary, limiting to 1 per topic
        sites = []
        for topic_id, topic_data in diccionary_health_content.items():
            count = 0  # Counter to limit the number of sites per topic
            for entry in topic_data:
                elements = entry[6]
                if isinstance(elements, dict) and 'site' in elements:
                    for site in elements['site']:
                        if count < 1:  # Only add up to 1 site per topic
                            sites.append(site)
                            count += 1
                        else:
                            break  # Stop adding more sites for this topic when 1 is added

        if sites:
            total_sites = len(sites)  # Total number of sites
            # Calculate the items to show for the current page
            start_index = self.current_page_sites * self.items_per_page_sites
            end_index = min(start_index + self.items_per_page_sites, total_sites)

            # Sort sites alphabetically by title
            paginated_sites = sorted(sites, key=lambda x: x.get('title', '').lower())[start_index:end_index]

            for index, site in enumerate(paginated_sites, start=start_index + 1):
                title = site.get('title', 'No Title')
                title_label = tk.Label(scrollable_frame, text=f"{index}. {title}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                title_label.pack(pady=20, anchor='w')

                url = site.get('url', '#')
                url_label = tk.Label(scrollable_frame, text="Article's URL", fg="blue", cursor="hand2")
                url_label.pack(pady=5, anchor='w')
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

                organization_content = site.get('organization_content', [])
                if organization_content:
                    org_label = tk.Label(scrollable_frame, text="Article written by: " + ", ".join(organization_content))
                    org_label.pack(pady=5, anchor='w')

                language_site_url = site.get('language_site_url', None)
                if language_site_url:
                    lang_url_label = tk.Label(scrollable_frame, text="Other language URL", fg="blue", cursor="hand2")
                    lang_url_label.pack(pady=5, anchor='w')
                    lang_url_label.bind("<Button-1>", lambda e, link=language_site_url: self.open_url(link))

            # Pagination buttons
            if self.current_page_sites > 0:
                prev_button = ttk.Button(scrollable_frame, text="Previous", command=lambda: self.change_page_sites(-1), style="Rounded.TButton")
                prev_button.pack(pady=5, anchor='w')
            if end_index < total_sites:
                next_button = ttk.Button(scrollable_frame, text="Next", command=lambda: self.change_page_sites(1), style="Rounded.TButton")
                next_button.pack(pady=5, anchor='w')

        else:
            tk.messagebox.showinfo("Information", "No sites available.")
            self.create_main_screen()

        # Go back button at the bottom
        back_button = ttk.Button(scrollable_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, anchor='w')

        # Update the scroll region to fit the content
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_topic_sites(self, sites):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title label for the entire section
        title_label = tk.Label(self.top_frame, text="Related articles from this topic", font=("Montserrat", 20, "bold"), fg="white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=20, anchor='w')

        # Create a scrollable frame for details
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Ensure scrollable_frame can grow
        scrollable_frame.grid_columnconfigure(0, weight=1)

        if sites:
            for index, site in enumerate(sites, start=1):
                # Display the title in larger font
                title = site.get('title', 'No Title')
                title_label = tk.Label(scrollable_frame, text=f"{index}. {title}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                title_label.pack(pady=(10, 5), anchor='w')  # Expand across center

                # Display the URL as a clickable link
                url = site.get('url', '#')
                url_label = tk.Label(scrollable_frame, text="Article's URL", fg="blue", cursor="hand2")
                url_label.pack(pady=5, anchor='w')
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

                # Display organization content if available
                organization_content = site.get('organization_content', [])
                if organization_content:
                    org_label = tk.Label(scrollable_frame, text="Article written by: " + ", ".join(organization_content))
                    org_label.pack(pady=5, anchor='w')

                # Handle language_site_url
                language_site_url = site.get('language_site_url', None)
                if language_site_url:
                    lang_url_label = tk.Label(scrollable_frame, text="Other language URL", fg="blue", cursor="hand2")
                    lang_url_label.pack(pady=5, anchor='w')
                    lang_url_label.bind("<Button-1>", lambda e, link=language_site_url: self.open_url(link))

        # Go Back button at the bottom
        back_button = ttk.Button(scrollable_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, anchor='w')

    def show_primary_institutes(self):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title for the primary institutes
        title_label = tk.Label(self.top_frame, text="Organizations", font=("Montserrat", 20, "bold"), fg="white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=10, anchor='w')

        texts = []  # Store institute names
        urls = []  # Store URLs
        seen_institutes = set()  # Track unique institutes

        # Loop through the dictionary to extract primary institute content
        for topic_id, topic_data in diccionary_health_content.items():
            for entry in topic_data:
                elements = entry[6]
                if 'primary_institute' in elements:
                    for primary_institute in elements['primary_institute']:
                        # Extract 'text' (institute name) and 'url'
                        institute_name = primary_institute['text']
                        institute_url = primary_institute['url']

                        # Append only if the institute is not already added
                        if institute_name not in seen_institutes:
                            texts.append(institute_name)
                            urls.append(institute_url)
                            seen_institutes.add(institute_name)  # Mark this institute as seen

        if texts:
            total_institutes = len(texts)  # Total number of institutes
            # Calculate the items to show for the current page
            start_index = self.current_page_organizations * self.items_per_page_organizations
            end_index = min(start_index + self.items_per_page_organizations, total_institutes)

            # Sort the institutes alphabetically along with their URLs
            sorted_terms = sorted(zip(texts, urls))[start_index:end_index]

            # Create a scrollable frame using the new method
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            content_frame = ttk.Frame(scrollable_frame)
            content_frame.pack(anchor='w')

            # Enumerate and display the institutes
            for index, (term, url) in enumerate(sorted_terms, start=start_index + 1):
                # Create a label for each primary institute
                label = tk.Label(content_frame, text=f"{index}. {term}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                label.pack(pady=5, anchor='w')

                # Display the URL as a clickable label below each institute name
                url_label = tk.Label(content_frame, text="Organization's URL", fg="blue", cursor="hand2")
                url_label.pack(anchor='w')
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

                # Pagination buttons
                if self.current_page_organizations > 0:
                    prev_button = ttk.Button(content_frame, text="Previous", command=lambda: self.change_page_organizations(-1))
                    prev_button.pack(pady=5, anchor='w')
                if end_index < total_institutes:
                    next_button = ttk.Button(content_frame, text="Next", command=lambda: self.change_page_organizations(1))
                    next_button.pack(pady=5, anchor='w')

            # Go back button at the bottom
            back_button = ttk.Button(content_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='w')
        else:
            messagebox.showinfo("Information", "No primary institutes available.")
            self.create_main_screen()


    def show_language_mapped_topics(self):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title for the language mapped topics
        title_label = tk.Label(self.top_frame, text="Available languages", font=("Montserrat", 20, "bold"), fg= "white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=10, anchor='w')

        topics = {}  # Store topics with their URLs

        # Loop through the dictionary to extract language_mapped_topic_content
        for topic_id, topic_data in diccionary_health_content.items():
            for entry in topic_data:
                elements = entry[6]
                topic_name = None  # Variable to hold the topic name

                # Extract language_mapped_topic and get the topic name
                if 'language_mapped_topic' in elements:
                    for language_mapped_topic in elements['language_mapped_topic']:
                        topic_name = language_mapped_topic['text']
                        if topic_name not in topics:
                            topics[topic_name] = []  # Initialize the list for this topic

                # Extract other_language
                if 'other_language' in elements:
                    for other_language in elements['other_language']:
                        if topic_name:
                            topics[topic_name].append((other_language['text'], other_language['url']))

        if topics:
            total_topics = len(topics)  # Total number of topics
             # Calculate the items to show for the current page
            start_index = self.current_page_languages * self.items_per_page_languages
            end_index = min(start_index + self.items_per_page_languages, total_topics)

            # Sort topics alphabetically
            sorted_topics = sorted(topics.items())[start_index:end_index]  # Sort by topic name

            # Create a scrollable frame using the new method
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            content_frame = ttk.Frame(scrollable_frame)
            content_frame.pack(anchor='w') 

            # Enumerate and display the topics
            for index, (topic_name, language_links) in enumerate(sorted_topics, start=start_index + 1):
                # Display the topic name as a label
                topic_label = tk.Label(content_frame, text=f"{index}. {topic_name}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                topic_label.pack(pady=(10, 5), anchor='w')

                # Display the URLs as clickable labels below the topic name
                for lang_text, lang_url in language_links:
                    url_label = tk.Label(content_frame, text=lang_text, fg="blue", cursor="hand2")
                    url_label.pack(anchor='w')
                    url_label.bind("<Button-1>", lambda e, link=lang_url: self.open_url(link))

            # Pagination buttons
            if self.current_page_languages > 0:
                prev_button = ttk.Button(content_frame, text="Previous", command=lambda: self.change_page_languages(-1), style="Rounded.TButton")
                prev_button.pack(pady=5, anchor='w')
            if end_index < total_topics:
                next_button = ttk.Button(content_frame, text="Next", command=lambda: self.change_page_languages(1), style="Rounded.TButton")
                next_button.pack(pady=5, anchor='w')

            # Go back button at the bottom
            back_button = ttk.Button(content_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='w')
        else:
            messagebox.showinfo("Information", "No other available languages.")
            self.create_main_screen()

    def return_to_main_screen(self):
        # Clear the top frame
        self.clear_top_frame()
        # Clear the current main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create top frame for the search area if it doesn't exist
        if not hasattr(self, 'top_frame'):
            self.top_frame = tk.Frame(self.root, bg="#232323")
            self.top_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))

        self.create_search_frame()  # Create it if it doesn't exist

        self.create_main_screen()  # Call to recreate buttons or any additional UI

    def graph_data_window(self):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title label for the entire section, centered
        title_label = tk.Label(self.top_frame, text="Graphs", font=("Montserrat", 14, "bold"), fg= "white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=20, anchor='center')

        # Create a scrollable frame for sites
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Frame to hold content centrally
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.grid_columnconfigure(0, weight=1)  # Allow column to expand

        # Create buttons for graph options
        graph_button_1 = ttk.Button(content_frame, text="Top 10 Health Topics with Most Sites", command=self.graph_data_1, style="Rounded.TButton")
        graph_button_1.grid(row=0, column=0, pady=10, padx=20, sticky="ew")  # Add padx for spacing

        graph_button_2 = ttk.Button(content_frame, text="Most 10 Frequent Languages in Health Topics", command=self.graph_data_2, style="Rounded.TButton")
        graph_button_2.grid(row=1, column=0, pady=10, padx=20, sticky="ew")  # Add padx for spacing

        graph_button_3 = ttk.Button(content_frame, text="Most 10 Frequent Organizations in Health Topics", command=self.graph_data_3, style="Rounded.TButton")
        graph_button_3.grid(row=2, column=0, pady=10, padx=20, sticky="ew")  # Add padx for spacing

        # Pack the content_frame to ensure it's visible
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)  # Center and fill

        # Center content_frame within the scrollable_frame
        scrollable_frame.pack(expand=True, fill=tk.BOTH)

        # Center the "Go back" button
        back_button = ttk.Button(scrollable_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, anchor='center')

    def graph_data_1(self):
        # Hide the top frame and search bar
        self.clear_top_frame()

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

        # Select only the top 10 entries
        df = df.head(10)

        # Create a Figure for the plot
        fig = Figure(figsize=(12, 8))
        ax = fig.add_subplot(111)

        # Create the bar chart
        ax.bar(df['Title'], df['Num_Sites'], color='skyblue')
        ax.set_xlabel('Health Topics')
        ax.set_ylabel('Number of Sites')
        ax.set_title('Top 10 Health Topics with Most Sites')

        # Set ticks and labels
        ax.set_xticks(range(len(df['Title'])))
        ax.set_xticklabels(df['Title'], rotation=45, fontsize=7, ha='right')

        # Display the plot
        canvas = FigureCanvasTkAgg(fig, master=content_frame)  # Create a canvas for the plot
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Center the Go Back button at the bottom
        back_button = ttk.Button(content_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, fill='x')  # Use pack for the back button

    def graph_data_2(self):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create a scrollable frame
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Frame to hold content centrally
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.grid_columnconfigure(0, weight=1)  # Center the column

        # Ensure content_frame is centered within the scrollable_frame
        content_frame.pack(expand=True, padx=20, pady=20)

        # Extract languages
        languages = []
        for topic_info in diccionary_health_content.values():
            # Access the first tuple in the list
            _, _, _, _, language, _, elements = topic_info[0]

            # Add the primary language
            languages.append(language)

            # Add languages from `language_mapped_topic` if it's a dictionary
            if 'language_mapped_topic' in elements:
                mapped_topics = elements['language_mapped_topic']
                if isinstance(mapped_topics, list):
                    for topic in mapped_topics:
                        mapped_language = topic.get('language')  # Access the language key
                        if mapped_language:
                            languages.append(mapped_language)

            # Add languages from `other_language` if it's a list
            if 'other_language' in elements:
                for lang in elements['other_language']:
                    vernacular_name = lang.get('vernacular_name')  # Access the vernacular_name key
                    if vernacular_name:
                        languages.append(vernacular_name)

        # Count the frequency of each language
        language_counts = Counter(languages)

        # Get the 10 most common languages
        top_languages = language_counts.most_common(10)

        # Create a DataFrame with the data
        df_lang = pd.DataFrame(top_languages, columns=['Language', 'Count'])

        # Create a Figure for the plot
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Create the bar chart for language frequencies
        ax.bar(df_lang['Language'], df_lang['Count'], color='lightgreen')
        ax.set_xlabel('Languages')
        ax.set_ylabel('Frequency')
        ax.set_title('Most 10 Frequent Languages in Health Topics')

        # Set ticks and labels
        ax.set_xticks(range(len(df_lang['Language'])))
        ax.set_xticklabels(df_lang['Language'], rotation=45)

        # Display the plot
        canvas = FigureCanvasTkAgg(fig, master=content_frame)  # Create a canvas for the plot
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, side=tk.TOP)

        # Center the Go Back button at the bottom
        back_button = ttk.Button(content_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, fill='x')  # Use pack for the back button

    def graph_data_3(self):
        # Hide the top frame and search bar
        self.clear_top_frame()
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # Create a scrollable frame
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)
        # Frame to hold content centrally
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.pack(expand=True, padx=20, pady=20)
        # Extract organizations
        organizations = []
        for topic_info in diccionary_health_content.values():
            # Access the first tuple in the list
            _, _, _, _, _, _, elements = topic_info[0]
            # Check if 'site' exists in elements
            if 'site' in elements:
                mapped_topics = elements['site']
                if isinstance(mapped_topics, list):  # Ensure it's a list
                    for topic in mapped_topics:
                        # Get organization_content if it's a list
                        mapped_organization_list = topic.get('organization_content')
                        if isinstance(mapped_organization_list, list):  # Ensure it's a list
                            for organization in mapped_organization_list:
                                if organization:  # Check if the organization is not empty
                                    organizations.append(organization)
        # Count the frequency of each organization
        organization_count = Counter(organizations)
        # Get the 10 most common organizations
        top_organizations = organization_count.most_common(10)
        # Create a DataFrame with the data
        df_org = pd.DataFrame(top_organizations, columns=['Organization', 'Count'])
        # Create a Figure for the plot
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        # Create the pie chart for organization frequencies
        ax.pie(df_org['Count'], labels=df_org['Organization'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title('Most 10 Frequent Organizations in Health Topics')
        # Display the plot
        canvas = FigureCanvasTkAgg(fig, master=content_frame)  # Create a canvas for the plot
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, side=tk.TOP)
        # Center the Go Back button at the bottom
        back_button = ttk.Button(content_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, fill='x')  # Use pack for the back button

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def search(self):
        query = self.entry.get()
        # print(f"Searching for: {query}")

    def show_data_set_contents(self):
        from parser import health_TOPICS_DATA_GENERATION_XLL
        info_string = ("Total Health Topics: " + health_TOPICS_DATA_GENERATION_XLL[0] + '\n'
        + "Date Generated: " + health_TOPICS_DATA_GENERATION_XLL[1] + '\n' + "Time Generated: "
        + health_TOPICS_DATA_GENERATION_XLL[2])
        messagebox.showinfo("Dataset Information",  message=info_string)

    def create_search_frame(self):
        # If search frame already exists, return
        self.search_frame = tk.Frame(self.top_frame, bg="#232323")
        
        title_label = tk.Label(self.search_frame, text="Search for symptoms, diseases and procedures", bg="#232323", fg="white", font=("Montserrat", 14, "bold"))
        title_label.pack(pady=(0, 10))

        self.entry = tk.Entry(self.search_frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))

        search_button = ttk.Button(self.search_frame, text="Search", command=self.search, style="Rounded.TButton", width=11, padding=(6, 0))
        search_button.pack(side=tk.LEFT)

    def clear_results(self):
        if hasattr(self, 'results_frame'):
            for widget in self.results_frame.winfo_children():
                widget.destroy()

    def show_search_results(self, results, query):
        self.clear_top_frame()
        # Clear the main frame to show results
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create a scrollable frame for the results
        canvas, self.results_frame = self.create_scrollable_frame(self.main_frame)
        self.clear_results()  # Clear previous results

        # Title for the search results
        title_label = tk.Label(self.top_frame, text=f"Search Results for '{query}'", font=("Montserrat", 20, "bold"), fg="white", bg=self.top_frame.cget("bg"))
        title_label.pack(pady=10, anchor='w')

        # If no results are found, display a message
        if not results:
            no_results_label = tk.Label(self.results_frame, text="No results found.", font=("Montserrat", 12), fg="black")
            no_results_label.pack(pady=10, anchor='w')

            # Go back button
            back_button = ttk.Button(self.results_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
            back_button.pack(pady=20, anchor='w')

            return

        total_results = len(results)  # Total number of results
        # Calculate the items to show for the current page
        start_index = self.current_page_search * self.items_per_page_search
        end_index = min(start_index + self.items_per_page_search, total_results)

        # Display the current page of results
        for index, topic in enumerate(results[start_index:end_index], start=start_index + 1):
            if len(topic) != 7:
                print(f"Unexpected topic structure: {topic}")
                continue

            description, title, url, id, language, date, elements = topic

            # Create a label for the enumerated title
            result_label = tk.Label(self.results_frame, text=f"{index}. Title: {title}", font=("Montserrat", 12, "bold"), fg="black")
            result_label.pack(pady=5, anchor='w')

            # Clickable URL label
            url_label = tk.Label(self.results_frame, text=url, font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
            url_label.pack(pady=5, anchor='w')

            # Bind the click event to open the URL
            url_label.bind("<Button-1>", lambda e, url=url: self.open_url(url))

            # Show sites if available
            if 'site' in elements:
                sites_label = tk.Label(self.results_frame, text="Sites:", font=("Montserrat", 12, "bold"), fg="black")
                sites_label.pack(pady=5, anchor='w')
                for index, site in enumerate(elements['site'], start=1):
                    site_title = site.get('title', 'No title')
                    site_url = site.get('url', '')

                    # Create a frame to hold the index and link
                    frame = tk.Frame(self.results_frame)
                    frame.pack(pady=5, anchor='w')

                    # Create the index label
                    index_label = tk.Label(frame, text=f"{index}. ", font=("Montserrat", 12), fg="black")
                    index_label.pack(side='left')  # Pack index on the left

                    # Create the clickable URL label
                    url_label = tk.Label(frame, text=site_title, font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                    url_label.pack(side='left')  # Pack link right next to the index

                    # Bind the click event to open the site URL
                    url_label.bind("<Button-1>", lambda e, url=site_url: self.open_url(url))

            # Show language mapped topics if available
            if 'language_mapped_topic' in elements:
                lang_topics = elements['language_mapped_topic']
                if isinstance(lang_topics, list):
                    for index, lang_topic in enumerate(lang_topics, start=1):
                        lang_topic_url = lang_topic.get('url', '')
                        lang_topic_text = lang_topic.get('text', 'Language Mapped Topic')

                        # Create a frame for index and link
                        frame = tk.Frame(self.results_frame)
                        frame.pack(pady=5, anchor='w')

                        # Create index label
                        index_label = tk.Label(frame, text=f"{index}. ", font=("Montserrat", 12), fg="black")
                        index_label.pack(side='left')

                        # Create clickable language mapped topic label
                        lang_label = tk.Label(frame, text=lang_topic_text, font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                        lang_label.pack(side='left')

                        # Bind the click event
                        lang_label.bind("<Button-1>", lambda e, url=lang_topic_url: self.open_url(url))

            # Show related topics if available
            if 'related_topic' in elements:
                related_label = tk.Label(self.results_frame, text="Related Topics:", font=("Montserrat", 12, "bold"), fg="black")
                related_label.pack(pady=5, anchor='w')
                for index, related in enumerate(elements['related_topic'], start=1):
                    related_text = related.get('text', 'Related Topic')
                    related_url = related.get('url', '')

                    # Create a frame for index and link
                    frame = tk.Frame(self.results_frame)
                    frame.pack(pady=5, anchor='w')

                    # Create index label
                    index_label = tk.Label(frame, text=f"{index}. ", font=("Montserrat", 12), fg="black")
                    index_label.pack(side='left')

                    # Create clickable related topic label
                    related_topic_label = tk.Label(frame, text=related_text, font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                    related_topic_label.pack(side='left')

                    # Bind the click event
                    related_topic_label.bind("<Button-1>", lambda e, url=related_url: self.open_url(url))

        # Pagination buttons
        if self.current_page_search > 0:
            prev_button = ttk.Button(self.results_frame, text="Previous", command=lambda: self.change_page_search(-1), style="Rounded.TButton")
            prev_button.pack(pady=5, anchor='w')
        if end_index < total_results:
            next_button = ttk.Button(self.results_frame, text="Next", command=lambda: self.change_page_search(1), style="Rounded.TButton")
            next_button.pack(pady=5, anchor='w')

        # Go back button
        back_button = ttk.Button(self.results_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, anchor='w')

    def search(self):
        # Get the query from the entry field
        query = self.entry.get().lower()

        results = []
        # If the query is too short or empty, show an error message
        if len(query) < 3 or query.isspace():
            # Show an error message
            self.show_search_results(results)
            return

        # Search for the query in the dictionary
        for topic_id, topic_list in diccionary_health_content.items():
            for topic in topic_list:
                description, title, url, id, language, date, elements = topic

                title = title.lower() if title else ''
                description = description.lower() if description else ''
                full_summary = ' '.join(elements.get('full_summary', [])).lower() if 'full_summary' in elements else ''

                also_called = elements.get('also_called', [])
                if isinstance(also_called, list):
                    also_called = ' '.join(also_called).lower() 
                else:
                    also_called = also_called.lower() if also_called else ''

                see_reference = elements.get('see_reference', [])
                if isinstance(see_reference, list):
                    see_reference = ' '.join(see_reference).lower()
                else:
                    see_reference = see_reference.lower() if see_reference else ''

                # If the query is found in the title, description, full_summary, also_called, or see_reference, add the topic to the results
                if query in title or query in description or query in full_summary or query in also_called or query in see_reference:
                    results.append(topic)
                else:
                    sites = elements.get('site', [])
                    for site in sites:
                        site_title = site.get('title', '').lower()
                        if query in site_title:
                            results.append(topic)
                            break

        self.show_search_results(results, query)
 
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
# - Ver si hay opcion de centrar las cosas en la pantalla, si no ponerlo a la izquierda ////// NO SE PUDO REALIZAR EL CAMBIO /////
