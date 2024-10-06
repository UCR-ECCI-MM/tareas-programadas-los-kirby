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
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title label for the entire section, centered
        title_label = tk.Label(self.main_frame, text="List of all topics", font=("Montserrat", 14, "bold"), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=20, anchor='center')

        # Go back button at the top if list is too long
        back_button = ttk.Button(self.main_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20)

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

            # Create a frame for centering buttons
            button_frame = ttk.Frame(scrollable_frame)
            button_frame.pack(anchor='center')  # Center the frame within the scrollable area

            for index, (term, topic_id) in enumerate(sorted_terms, start=1):
                button_text = f"{index}. {term}"  # Add enumeration
                button = ttk.Button(button_frame, text=button_text, command=lambda id=topic_id: self.show_topic_details(id), style="Rounded.TButton", width=40)  # Fixed width
                button.pack(pady=5, anchor='center')  # Center each button

            back_button = ttk.Button(button_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='center')  # Center the back button
        else:
            messagebox.showinfo("Information", "No names in 'also_called' available.")
            self.create_main_screen()

    def show_topic_details(self, topic_id):
        # Hide the top frame and search bar
        self.clear_top_frame()

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

        title_label = tk.Label(self.main_frame, text="All available sites", font=("Montserrat", 14, "bold"), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=20)

        # Go back button at the top if list is too long
        back_button = ttk.Button(self.main_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20)

        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Extract all sites from the dictionary
        sites = []
        for topic_id, topic_data in diccionary_health_content.items():
            for entry in topic_data:
                elements = entry[6]
                if isinstance(elements, dict) and 'site' in elements:
                    sites.extend(elements['site'])  # Add all sites to the list

        if sites:
            # Sort sites alphabetically by title
            sites.sort(key=lambda x: x.get('title', '').lower())  # Sort by title

            for index, site in enumerate(sites, start=1):
                title = site.get('title', 'No Title')
                title_label = tk.Label(scrollable_frame, text=f"{index}. {title}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                title_label.grid(pady=(10, 5), sticky="ew")  # Expand across center

                url = site.get('url', '#')
                url_label = tk.Label(scrollable_frame, text="Article's URL", fg="blue", cursor="hand2")
                url_label.grid(pady=5, sticky="ew")
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

                organization_content = site.get('organization_content', [])
                if organization_content:
                    org_label = tk.Label(scrollable_frame, text="Article written by: " + ", ".join(organization_content))
                    org_label.grid(pady=5, sticky="ew")

                language_site_url = site.get('language_site_url', None)
                if language_site_url:
                    lang_url_label = tk.Label(scrollable_frame, text="Other language URL", fg="blue", cursor="hand2")
                    lang_url_label.grid(pady=5, sticky="ew")
                    lang_url_label.bind("<Button-1>", lambda e, link=language_site_url: self.open_url(link))

        # Go back button at the bottom
        back_button = ttk.Button(scrollable_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.grid(pady=20, sticky="ew")

    def show_topic_sites(self, sites):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Go back button at the top if list is too long
        back_button = ttk.Button(self.main_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20)

        # Title label for the entire section, centered
        title_label = tk.Label(self.main_frame, text="Related articles from this topic:", font=("Montserrat", 14), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=20)

        # Create a scrollable frame for details
        canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

        # Ensure scrollable_frame can grow
        scrollable_frame.grid_columnconfigure(0, weight=1)

        if sites:
            for index, site in enumerate(sites, start=1):
                # Display the title in larger font, centered
                title = site.get('title', 'No Title')
                title_label = tk.Label(scrollable_frame, text=f"{index}. {title}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                title_label.grid(pady=(10, 5), sticky="ew")  # Expand across center

                # Display the URL as a clickable link, centered
                url = site.get('url', '#')
                url_label = tk.Label(scrollable_frame, text="Article's URL", fg="blue", cursor="hand2")
                url_label.grid(pady=5, sticky="ew")
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

                # Display organization content if available
                organization_content = site.get('organization_content', [])
                if organization_content:
                    org_label = tk.Label(scrollable_frame, text="Article written by: " + ", ".join(organization_content))
                    org_label.grid(pady=5, sticky="ew")

                # Handle language_site_url
                language_site_url = site.get('language_site_url', None)
                if language_site_url:
                    lang_url_label = tk.Label(scrollable_frame, text="Other language URL", fg="blue", cursor="hand2")
                    lang_url_label.grid(pady=5, sticky="ew")
                    lang_url_label.bind("<Button-1>", lambda e, link=language_site_url: self.open_url(link))

        # Center the Go Back button at the bottom
        back_button = ttk.Button(scrollable_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.grid(pady=20, sticky="ew")

    def show_primary_institutes(self):
        # Hide the top frame and search bar
        self.clear_top_frame()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title for the primary institutes
        title_label = tk.Label(self.main_frame, text="Organizations", font=("Montserrat", 14, "bold"), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=10, anchor='center')  # Center the title

        # Go back button at the top if the list is too long
        back_button = ttk.Button(self.main_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20)

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

            # Create a frame for centering content
            content_frame = ttk.Frame(scrollable_frame)
            content_frame.pack(anchor='center')  # Center the frame within the scrollable area

            # Enumerate and display the institutes
            for index, (term, url, topic_id) in enumerate(sorted_terms, start=1):
                # Create a label for each primary institute
                label = tk.Label(content_frame, text=f"{index}. {term}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                label.pack(pady=5, anchor='center')  # Center each label

                # Display the URL as a clickable label below each institute name
                url_label = tk.Label(content_frame, text=url, fg="blue", cursor="hand2")
                url_label.pack(anchor='center')  # Center the URL
                url_label.bind("<Button-1>", lambda e, link=url: self.open_url(link))

            # Go back button at the bottom
            back_button = ttk.Button(content_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='center')  # Center the back button
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
        title_label = tk.Label(self.main_frame, text="Available languages", font=("Montserrat", 14, "bold"), bg=self.main_frame.cget("bg"))
        title_label.pack(pady=10, anchor='center')  # Center the title

        # Go back button at the top if the list is too long
        back_button = ttk.Button(self.main_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20)

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
            # Sort topics alphabetically
            sorted_topics = sorted(topics.items())  # Sort by topic name

            # Create a scrollable frame using the new method
            canvas, scrollable_frame = self.create_scrollable_frame(self.main_frame)

            # Create a frame for centering content
            content_frame = ttk.Frame(scrollable_frame)
            content_frame.pack(anchor='center')  # Center the frame within the scrollable area

            # Enumerate and display the topics
            for index, (topic_name, language_links) in enumerate(sorted_topics, start=1):
                # Display the topic name as a label
                topic_label = tk.Label(content_frame, text=f"{index}. {topic_name}", font=("Montserrat", 12, "bold"), bg=self.main_frame.cget("bg"))
                topic_label.pack(pady=(10, 5), anchor='center')  # Center the topic name

                # Display the URLs as clickable labels below the topic name
                for lang_text, lang_url in language_links:
                    url_label = tk.Label(content_frame, text=lang_text, fg="blue", cursor="hand2")
                    url_label.pack(anchor='center')  # Center the language URL
                    url_label.bind("<Button-1>", lambda e, link=lang_url: self.open_url(link))

            # Go back button at the bottom
            back_button = ttk.Button(content_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton", width=40)  # Fixed width
            back_button.pack(pady=20, anchor='center')  # Center the back button
        else:
            messagebox.showinfo("Information", "No other available languages.")
            self.create_main_screen()

    def return_to_main_screen(self):
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
        title_label = tk.Label(self.main_frame, text="Graphs", font=("Montserrat", 14, "bold"), bg=self.main_frame.cget("bg"))
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
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Create the bar chart
        ax.bar(df['Title'], df['Num_Sites'], color='skyblue')
        ax.set_xlabel('Health Topics')
        ax.set_ylabel('Number of Sites')
        ax.set_title('Top 10 Health Topics with Most Sites')

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

        # Create a DataFrame with the data
        df_lang = pd.DataFrame(language_counts.items(), columns=['Language', 'Count'])

        # Create a Figure for the plot
        fig = Figure(figsize=(10,6))
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
        canvas.get_tk_widget().pack(fill='both', expand=True, side=tk.TOP)

        # Center the Go Back button at the bottom
        back_button = ttk.Button(content_frame, text="Go Back", command=self.return_to_main_screen, style="Rounded.TButton")
        back_button.pack(pady=20, fill='x')  # Use pack for the back button

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def search(self):
        query = self.entry.get()
        print(f"Searching for: {query}")

    def show_data_set_contents(self):
        from parser import health_TOPICS_DATA_GENERATION_XLL
        info_string = ("Total Health Topics: " + health_TOPICS_DATA_GENERATION_XLL[0] + '\n'
        + "Date Generated: " + health_TOPICS_DATA_GENERATION_XLL[1] + '\n' + "Time Generated: "
        + health_TOPICS_DATA_GENERATION_XLL[2])
        messagebox.showinfo("Dataset Information",  message=info_string)

    def create_search_frame(self):
        # Crear el search_frame si no existe
        self.search_frame = tk.Frame(self.top_frame, bg="#232323")
        
        # Título
        title_label = tk.Label(self.search_frame, text="Search for symptoms, diseases and procedures", bg="#232323", fg="white", font=("Montserrat", 14, "bold"))
        title_label.pack(pady=(0, 10))

        # Campo de búsqueda
        self.entry = tk.Entry(self.search_frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))

        # Botón de búsqueda
        search_button = ttk.Button(self.search_frame, text="Search", command=self.search, style="Rounded.TButton", width=11, padding=(6, 0))
        search_button.pack(side=tk.LEFT)

    def clear_results(self):
        if hasattr(self, 'results_frame'):
            for widget in self.results_frame.winfo_children():
                widget.destroy()

    def show_search_results(self, results):
        self.clear_top_frame()
        # Clear the main frame to show results
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create a scrollable frame for the results
        canvas, self.results_frame = self.create_scrollable_frame(self.main_frame)
        self.clear_results()  # Clear previous results

        # Title for the search results
        title_label = tk.Label(self.results_frame, text="Search Results", font=("Montserrat", 14, "bold"), fg="black")
        title_label.pack(pady=10)

        # If no results are found, display a message
        if not results:
            no_results_label = tk.Label(self.results_frame, text="No results found.", font=("Montserrat", 12), fg="black")
            no_results_label.pack(pady=10)
            
            # Go back button
            back_button = ttk.Button(self.results_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
            back_button.pack(pady=20)
            
        else:
            for index, topic in enumerate(results):
                if len(topic) != 7:
                    print(f"Unexpected topic structure: {topic}")
                    continue

                description, title, url, id, language, date, elements = topic

                # Create a label for the enumerated title
                result_label = tk.Label(self.results_frame, text=f"{index + 1}. Title: {title}", font=("Montserrat", 12, "bold"), fg="black")
                result_label.pack(pady=5)

                # Clickable URL label
                url_label = tk.Label(self.results_frame, text=url, font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                url_label.pack(pady=5)

                # Bind the click event to open the URL
                url_label.bind("<Button-1>", lambda e, url=url: self.open_url(url))

                # Show sites if available
                if 'site' in elements:
                    sites_label = tk.Label(self.results_frame, text="Sites:", font=("Montserrat", 12, "bold"), fg="black")
                    sites_label.pack(pady=5)
                    for site in elements['site']:
                        site_title = site.get('title', 'No title')
                        site_url = site.get('url', '')
                        
                        site_label = tk.Label(self.results_frame, text=site_title, font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                        site_label.pack(pady=5)
                        
                        # Bind the click event to open the site URL
                        site_label.bind("<Button-1>", lambda e, url=site_url: self.open_url(url))

                # Show URL for language mapped topic
                if 'language_mapped_topic' in elements:
                    lang_topics = elements['language_mapped_topic']
                    if isinstance(lang_topics, list):
                        for lang_topic in lang_topics:
                            lang_topic_url = lang_topic.get('url', '')
                            lang_topic_text = lang_topic.get('text', 'Language Mapped Topic')

                            lang_label = tk.Label(self.results_frame, text=f"Language Mapped Topic: {lang_topic_text}", font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                            lang_label.pack(pady=5)

                            # Bind the click event to open the language topic URL
                            lang_label.bind("<Button-1>", lambda e, url=lang_topic_url: self.open_url(url))
                    elif isinstance(lang_topics, dict):
                        lang_topic_url = lang_topics.get('url', '')
                        lang_topic_text = lang_topics.get('text', 'Language Mapped Topic')

                        lang_label = tk.Label(self.results_frame, text=f"Language Mapped Topic: {lang_topic_text}", font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                        lang_label.pack(pady=5)

                        # Bind the click event to open the language topic URL
                        lang_label.bind("<Button-1>", lambda e, url=lang_topic_url: self.open_url(url))

                # Show different names for the topic
                if 'related_topic' in elements:
                    related_label = tk.Label(self.results_frame, text="Related Topics:", font=("Montserrat", 12, "bold"), fg="black")
                    related_label.pack(pady=5)
                    for related in elements['related_topic']:
                        related_text = related.get('text', 'Related Topic')
                        related_url = related.get('url', '')

                        related_topic_label = tk.Label(self.results_frame, text=related_text, font=("Montserrat", 12, "underline"), fg="blue", cursor="hand2")
                        related_topic_label.pack(pady=5)

                        # Bind the click event to open the related topic URL
                        related_topic_label.bind("<Button-1>", lambda e, url=related_url: self.open_url(url))

            # Go back button
            back_button = ttk.Button(self.results_frame, text="Go back", command=self.return_to_main_screen, style="Rounded.TButton")
            back_button.pack(pady=20)

    def search(self):
        # Get the query from the entry field
        query = self.entry.get().lower()

        results = []
        # Verifica si la longitud del query es menor a 3 caracteres o si contiene solo espacios en blanco
        if len(query) < 3 or query.isspace():
            # Muestra un mensaje de error o alerta al usuario
            self.show_search_results(results)
            return


        # Itera sobre el diccionario para encontrar el query en los diferentes campos
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

                # Si la consulta se encuentra en alguno de los campos, añade el tema a los resultados
                if query in title or query in description or query in full_summary or query in also_called or query in see_reference:
                    results.append(topic)
                else:
                    # Verifica si el query está en alguno de los sitios
                    sites = elements.get('site', [])
                    for site in sites:
                        site_title = site.get('title', '').lower()
                        if query in site_title:
                            results.append(topic)
                            break

        # Muestra los resultados de búsqueda
        self.show_search_results(results)
 

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
# - Ver si hay opcion de centrar las cosas en la pantalla, si no ponerlo a la izquierda
# - Crear mas graficos para la opcion de Data graphs