import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

def def_graph():
    house_prices = np.random.normal(200000, 25000, 5000)
    plt.hist(house_prices, 200)
    plt.show()

# Creation of Main Window
root = tk.Tk()
root.title("Prototype: Medical Dictionary")
root.geometry('600x550')

# root.resizable(width=False, height=False) // Command to prevent resizing of window

color_one = "#212E36" # Darker Blue
color_two = "#344956" # Dark Blue
color_three = "#486475" # Lighter Blue
color_four = "#5B7F95" # Dark Orange
color_five = "#7798AC" # Orange
color_six = "#B6C8D3" # Yellow-Orange

# Creates a frame where all widgets will exist. Must be linked to Main Window
main_frame = tk.Frame(root, bg=color_one, pady=40)
# Adds frame to the window
main_frame.pack(fill=tk.BOTH, expand=True)
# Configures the size of the column of the grid where the widgets will be. Weight: Extra space in column
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)

# Creation of Label (text)
label = tk.Label(main_frame,
                text="Search!",
                font=('Arial', 20, 'bold'),
                bg=color_one, # background color
                fg=color_six, # text color
                highlightcolor="WHITE"
                )

# Adds label to the grid (0,0) of the frame
label.grid(column=0, row=0)

# Text box
entry =  tk.Entry(main_frame)
entry.grid(column=0, row=1)

# Button
diseases_button = tk.Button(main_frame,
                    bg=color_four,
                    foreground=color_one,
                    activebackground=color_two, # Works when hovering mouse
                    activeforeground=color_six,
                    highlightthickness=2,
                    highlightbackground=color_five,
                    highlightcolor="WHITE",
                    width=12,
                    height=2,
                    border=0,
                    cursor='hand1', # Works when hovering mouse
                    text="Dictionary",
                    font=('Arial', 16, 'bold')
                    )

diseases_button.grid(column=0, row=2)

dictionary_button = tk.Button(main_frame,
                    bg=color_four,
                    foreground=color_one,
                    activebackground=color_two,
                    activeforeground=color_six,
                    highlightthickness=2,
                    highlightbackground=color_five,
                    highlightcolor="WHITE",
                    width=12,
                    height=2,
                    border=0,
                    cursor='hand1',
                    text="Organizations",
                    font=('Arial', 16, 'bold')
                    )

dictionary_button.grid(column=0, row=3)

organizations_button = tk.Button(main_frame,
                    bg=color_four,
                    foreground=color_one,
                    activebackground=color_two,
                    activeforeground=color_six,
                    highlightthickness=2,
                    highlightbackground=color_five,
                    highlightcolor="WHITE",
                    width=12,
                    height=2,
                    border=0,
                    cursor='hand1',
                    text="Diseases",
                    font=('Arial', 16, 'bold')
                    )

organizations_button.grid(column=0, row=4)

languages_button = tk.Button(main_frame,
                    bg=color_four,
                    foreground=color_one,
                    activebackground=color_two,
                    activeforeground=color_six,
                    highlightthickness=2,
                    highlightbackground=color_five,
                    highlightcolor="WHITE",
                    width=12,
                    height=2,
                    border=0,
                    cursor='hand1',
                    text="Languages",
                    font=('Arial', 16, 'bold')
                    )

languages_button.grid(column=0, row=5)

graph_button = tk.Button(main_frame,
                    bg=color_four,
                    foreground=color_one,
                    activebackground=color_two,
                    activeforeground=color_six,
                    highlightthickness=2,
                    highlightbackground=color_five,
                    highlightcolor="WHITE",
                    width=12,
                    height=2,
                    border=0,
                    cursor='hand1',
                    text="Graph",
                    font=('Arial', 16, 'bold'),
                    command=def_graph
                    )

graph_button.grid(column=0, row=6)

# Loop to start and keep the window running
root.mainloop()