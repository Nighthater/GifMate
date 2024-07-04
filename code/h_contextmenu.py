# h_contextmenu.py
# Everything that happens when the right mouse button is clicked on the GIF

import tkinter as tk
from tkinter import ttk, filedialog, Toplevel
import os
from PIL import Image, ImageTk
import imghdr
import h_experimental
import h_giftools


def s_transparency(self):
    h_experimental.show_speech_bubble(self)

    
def s_import_gif(self):
    initial_dir = "/"
    h_giftools.pick_gif(self, initial_dir)


def s_select_gif(self):
    initial_dir = os.getcwd() + '/gifs'
    h_giftools.pick_gif(self, initial_dir)
    

def s_about(root):
    # Create new window
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x200")
    
    # Disable interaction with the main window
    about_window.transient(root)
    about_window.grab_set()
    
    # Add a label in the new window
    label = ttk.Label(about_window, text="GifMate © 2024 Nighthater")
    label.pack(pady=20)
