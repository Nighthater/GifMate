# h_contextmenu.py
# Everything that happens when the right mouse button is clicked on the GIF

import tkinter as tk
from tkinter import ttk, filedialog, Toplevel
import os
from PIL import Image, ImageTk
import imghdr
import h_experimental
import h_giftools
import webbrowser


def s_transparency(self):
    h_experimental.show_speech_bubble(self)

    
def s_import_gif(self):
    initial_dir = "/"
    h_giftools.pick_gif(self, initial_dir)


def s_select_gif(self):
    initial_dir = os.getcwd() + '/gifs'
    h_giftools.pick_gif(self, initial_dir)
    

def s_about(root):
    def open_link(event):
        webbrowser.open_new(r"https://github.com/Nighthater/GifMate")

    about_window = tk.Toplevel(root)
    about_window.title("About")

    # Center the window on the screen
    window_width = 350
    window_height = 250
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    about_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Add content to the about window
    frame = ttk.Frame(about_window, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Title label
    title_label = ttk.Label(frame, text="GifMate", font=("Helvetica", 16, "bold"))
    title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

    # Version label
    version_label = ttk.Label(frame, text="Version 1.0.0", font=("Helvetica", 12))
    version_label.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)

    # Description label
    description_label = ttk.Label(frame, text="Display and interact with GIFs", wraplength=380)
    description_label.grid(row=2, column=0, pady=(0, 10), sticky=tk.W)

    # Author label
    author_label = ttk.Label(frame, text="Developed by: Nighthater\n", font=("Helvetica", 10, "italic"))
    author_label.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)

    # Link label
    link_label = ttk.Label(frame, text="Visit the GitHub repo", foreground="blue", cursor="hand2")
    link_label.grid(row=4, column=0, pady=(0, 10), sticky=tk.W)
    link_label.bind("<Button-1>", open_link)

    # Close button
    close_button = ttk.Button(frame, text="Close", command=about_window.destroy)
    close_button.grid(row=5, column=0, pady=(10, 0), sticky=tk.E)

    # Make the window non-resizable
    about_window.resizable(False, False)
