# h_contextmenu.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def s_transparency():
    print("Transparency Setting selected")

def s_framerate():
    print("Framerate Setting selected")

def s_import_gif():
    print("Import GIF selected")
    
def s_select_gif():
    print("Select GIF selected")

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
